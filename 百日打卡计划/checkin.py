"""100天三目标打卡脚本

用法：
    python 百日打卡计划\checkin.py                   交互式打卡（今天）
    python 百日打卡计划\checkin.py --date 2026-05-19 补打卡
    python 百日打卡计划\checkin.py status            查看进度
    python 百日打卡计划\checkin.py report            查看周报
    python 百日打卡计划\checkin.py report --month    查看月报
    python 百日打卡计划\checkin.py chart             打卡热力图
"""

import json
import datetime
import argparse
import sys
from pathlib import Path

# 适配 Windows 终端编码
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA_DIR = Path(__file__).parent
DATA_FILE = DATA_DIR / "data.json"
JS_FILE = DATA_DIR / "data.js"
START_DATE = datetime.date(2026, 5, 18)
TARGET_DAYS = 100
GOALS = ["piano", "weight", "english"]
GOAL_NAMES = {"piano": "钢琴", "weight": "体重", "english": "英语"}

DATA_TEMPLATE = {
    "meta": {"start_date": START_DATE.isoformat(), "target_days": TARGET_DAYS},
    "logs": {},
    "weights": {},
}


def load_data():
    if not DATA_FILE.exists():
        data = dict(DATA_TEMPLATE)
        save_data(data)
        return data
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        sync_js(data)
        return data
    except (json.JSONDecodeError, KeyError):
        bak = DATA_FILE.with_suffix(".json.bak")
        if bak.exists():
            with open(bak, encoding="utf-8") as f:
                data = json.load(f)
            sync_js(data)
            return data
        data = dict(DATA_TEMPLATE)
        save_data(data)
        return data


def sync_js(data):
    """同步生成 data.js 供 dashboard.html 自动加载"""
    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write("window.__DATA__ = ")
        json.dump(data, f, ensure_ascii=False)
        f.write(";\n")


def save_data(data):
    if DATA_FILE.exists():
        import shutil

        shutil.copy2(DATA_FILE, DATA_FILE.with_suffix(".json.bak"))
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    sync_js(data)


def day_number(date_str):
    d = datetime.date.fromisoformat(date_str)
    return (d - START_DATE).days + 1


def today_str():
    return datetime.date.today().isoformat()


def input_int(prompt, default=None, min_val=None, max_val=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            v = int(raw)
            if min_val is not None and v < min_val:
                print(f"最少 {min_val}")
                continue
            if max_val is not None and v > max_val:
                print(f"最多 {max_val}")
                continue
            return v
        except ValueError:
            print("请输入整数")


def input_float(prompt, default=None, min_val=None, max_val=None, decimal_places=1):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return round(default, decimal_places)
        try:
            v = float(raw)
            if min_val is not None and v < min_val:
                print(f"最少 {min_val}")
                continue
            if max_val is not None and v > max_val:
                print(f"最多 {max_val}")
                continue
            return round(v, decimal_places)
        except ValueError:
            print("请输入数字")


def input_yesno(prompt, default="y"):
    while True:
        raw = input(prompt).strip().lower()
        if not raw:
            raw = default
        if raw in ("y", "yes", "是"):
            return True
        if raw in ("n", "no", "否"):
            return False
        print("请输入 y/n")


def do_checkin(date_str):
    data = load_data()
    logs = data.setdefault("logs", {})
    day = day_number(date_str)

    if day < 1 or day > TARGET_DAYS:
        print(f"[ERROR] 日期 {date_str} 不在 100 天范围内（第 1-{TARGET_DAYS} 天）")
        return

    if date_str > today_str():
        print("[ERROR] 不能提前打卡未来日期")
        return

    print(f"\n{'='*40}")
    print(f"  {date_str}  (第 {day}/{TARGET_DAYS} 天)")
    print(f"{'='*40}")

    entry = logs.get(date_str, {})
    changed = False

    for goal in GOALS:
        name = GOAL_NAMES[goal]
        done = entry.get(goal, {}).get("done", False)
        status = "[OK] 已打卡" if done else "[  ] 未打卡"
        print(f"\n--- {name}  [{status}] ---")

        verb = "练琴" if goal == "piano" else "运动" if goal == "weight" else "学英语"
        yn = input_yesno(f"今天{verb}了吗？(Y/n): ")
        goal_entry = entry.setdefault(goal, {})

        if yn:
            goal_entry["done"] = True
            if goal == "piano":
                goal_entry["minutes"] = input_int(
                    "练习了多少分钟？(30-60): ", default=30, min_val=1, max_val=240
                )
            elif goal == "weight":
                goal_entry["exercise_minutes"] = input_float(
                    "运动了多少分钟？(如 30.5): ",
                    default=30.0,
                    min_val=0.5,
                    max_val=240,
                    decimal_places=1,
                )
                etype = input("运动类型（跑步/力量/其他，留空跳过）: ").strip()
                if etype:
                    goal_entry["exercise_type"] = etype
                weigh_in = input_yesno("今天是称重日吗？(y/N): ", default="n")
                if weigh_in:
                    w = input_float(
                        "体重（kg，如 72.55）: ",
                        min_val=20,
                        max_val=300,
                        decimal_places=2,
                    )
                    weights = data.setdefault("weights", {})
                    weights[date_str] = w
                    goal_entry["weight_kg"] = w
            elif goal == "english":
                goal_entry["minutes"] = input_int(
                    "学习了多少分钟？: ", default=30, min_val=1, max_val=480
                )
                goal_entry["words"] = input_int(
                    "学了多少个单词？: ", default=10, min_val=0, max_val=500
                )
        else:
            goal_entry["done"] = False

        note = input("备注（可选，留空跳过）: ").strip()
        if note:
            goal_entry["note"] = note

        changed = True

    if changed:
        logs[date_str] = entry
        save_data(data)
        print(f"\n[OK] {date_str} 打卡完成！继续加油！")
    else:
        print("\n打卡已取消")


def calc_streak(data, goal):
    """计算某个目标的连续打卡天数（从最新日期往前）"""
    logs = data.get("logs", {})
    dates = sorted(logs.keys(), reverse=True)
    streak = 0
    for d in dates:
        entry = logs[d].get(goal, {})
        if entry.get("done"):
            streak += 1
        else:
            break
    return streak


def calc_completion(data, goal):
    """计算某个目标的总体完成率"""
    logs = data.get("logs", {})
    total = 0
    done = 0
    for d, entry in logs.items():
        g = entry.get(goal, {})
        if g.get("done") is not None:
            total += 1
            if g["done"]:
                done += 1
    rate = (done / total * 100) if total > 0 else 0
    return {"done": done, "total": total, "rate": round(rate, 1)}


def calc_overall(data):
    """计算整体完成率（所有目标合并）"""
    logs = data.get("logs", {})
    total_slots = 0
    done_slots = 0
    for d, entry in logs.items():
        for goal in GOALS:
            g = entry.get(goal, {})
            if g.get("done") is not None:
                total_slots += 1
                if g["done"]:
                    done_slots += 1
    rate = (done_slots / total_slots * 100) if total_slots > 0 else 0
    return {"done": done_slots, "total": total_slots, "rate": round(rate, 1)}


def show_status(data):
    today = today_str()
    day_num = day_number(today)
    if day_num < 1:
        day_num = 1
    if day_num > TARGET_DAYS:
        day_num = TARGET_DAYS

    print(f"\n{'='*45}")
    print(f"    [100天三目标计划] 进度概览")
    print(f"    第 {day_num}/{TARGET_DAYS} 天（{START_DATE} -> 今日）")
    print(f"{'='*45}")

    overall = calc_overall(data)
    bar_len = 30
    filled = int(overall["rate"] / 100 * bar_len)
    bar = "#" * filled + "." * (bar_len - filled)
    print(f"\n整体完成率: [{bar}] {overall['rate']}%")
    print(f"总打卡项: {overall['done']}/{overall['total']}")

    print()
    for goal in GOALS:
        name = GOAL_NAMES[goal]
        comp = calc_completion(data, goal)
        streak = calc_streak(data, goal)
        filled = int(comp["rate"] / 100 * bar_len)
        bar = "#" * filled + "." * (bar_len - filled)
        print(f"  {name}")
        print(
            f"    [{bar}] {comp['rate']}%  ({comp['done']}/{comp['total']}天)  连续{streak}天"
        )


def show_report(data, period="week"):
    logs = data.get("logs", {})
    dates = sorted(logs.keys())

    if not dates:
        print("暂无打卡记录")
        return

    if period == "month":
        months = {}
        for d in dates:
            m = d[:7]
            months.setdefault(m, []).append(d)
        print(f"\n{'='*50}")
        print("    [月报]")
        print(f"{'='*50}")
        for m, m_dates in sorted(months.items()):
            print(f"\n--- {m} ---")
            _print_period_summary(data, m_dates)
    else:
        today = today_str()
        week_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
        week_dates = [d for d in dates if d >= week_ago and d <= today]
        if not week_dates:
            week_dates = dates[-7:]
        print(f"\n{'='*50}")
        print("    [周报] 最近7天")
        print(f"{'='*50}")
        _print_period_summary(data, week_dates[-7:])


def _print_period_summary(data, dates):
    if not dates:
        print("  无记录")
        return
    for g in GOALS:
        name = GOAL_NAMES[g]
        done_count = 0
        total_minutes = 0
        day_count = 0
        for d in dates:
            entry = data["logs"].get(d, {}).get(g, {})
            if entry.get("done"):
                done_count += 1
                total_minutes += (
                    entry.get("minutes", 0) or entry.get("exercise_minutes", 0) or 0
                )
                day_count += 1
        avg_min = total_minutes / day_count if day_count else 0
        bar = "#" * done_count + "." * (len(dates) - done_count)
        print(
            f"  {name}: [{bar}] {done_count}/{len(dates)}天  (平均{avg_min:.0f}分钟/天)"
        )

    w_dates = [d for d in dates if d in data.get("weights", {})]
    if w_dates:
        weights = [data["weights"][d] for d in w_dates]
        if len(weights) >= 2:
            change = weights[-1] - weights[0]
            arrow = "↑" if change > 0 else "↓" if change < 0 else "->"
            print(
                f"  体重: {' -> '.join(f'{w:.1f}kg' for w in weights)}  ({arrow}{abs(change):.1f}kg)"
            )
        else:
            print(f"  体重: {weights[0]:.1f}kg")


def do_chart(data):
    """显示打卡热力图（最近30天）"""
    logs = data.get("logs", {})
    dates = sorted(logs.keys())
    if not dates:
        print("暂无数据")
        return

    print(f"\n  打卡热力图 (G=全部完成, Y=部分完成, R=未完成)")
    print(f"  {'='*50}\n")

    recent = dates[-30:]
    for d in recent:
        day = day_number(d)
        done_count = 0
        for g in GOALS:
            entry = logs[d].get(g, {})
            if entry.get("done"):
                done_count += 1
        if done_count == 3:
            mark = "[G]"
        elif done_count > 0:
            mark = "[Y]"
        else:
            mark = "[R]"
        print(f"  {mark} Day {day:>3}  ({d})  {done_count}/3")


def main():
    parser = argparse.ArgumentParser(description="100天三目标打卡")
    parser.add_argument(
        "action",
        nargs="?",
        default="checkin",
        choices=["checkin", "status", "report", "chart"],
        help="操作：checkin=打卡, status=进度, report=周报, chart=热力图",
    )
    parser.add_argument("--date", help="打卡日期（YYYY-MM-DD），用于补打卡")
    parser.add_argument("--month", action="store_true", help="月报模式")
    args = parser.parse_args()

    data = load_data()

    if args.action == "status":
        show_status(data)
    elif args.action == "report":
        show_report(data, "month" if args.month else "week")
    elif args.action == "chart":
        do_chart(data)
    else:
        date = args.date or today_str()
        do_checkin(date)


if __name__ == "__main__":
    main()

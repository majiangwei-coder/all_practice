"""
第九章：标准库精选示例代码
配合 08_标准库精选/ 目录下的 Markdown 文档学习
包含：collections、itertools、datetime、pathlib
"""

# ====================
# collections
# ====================

print("=" * 50)
print("collections")
print("=" * 50)

from collections import deque, defaultdict, Counter, OrderedDict, namedtuple, ChainMap

# deque - 双端队列
print("--- deque ---")
dq = deque([1, 2, 3, 4, 5])
print(f"初始: {dq}")

dq.append(6)
dq.appendleft(0)
print(f"append/appendleft: {dq}")

dq.pop()
dq.popleft()
print(f"pop/popleft: {dq}")

# 固定长度 deque
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
print(f"maxlen=3: {recent}")

# rotate
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)
print(f"rotate(2): {dq}")

# defaultdict
print("\n--- defaultdict ---")
dd = defaultdict(int)
dd["a"] += 1
print(f"dd (int): {dict(dd)}")

dd2 = defaultdict(list)
dd2["fruits"].append("apple")
dd2["fruits"].append("banana")
print(f"dd2 (list): {dict(dd2)}")

# 分组示例
words = ["apple", "banana", "apricot", "blueberry"]
by_first = defaultdict(list)
for word in words:
    by_first[word[0]].append(word)
print(f"按首字母分组: {dict(by_first)}")

# Counter
print("\n--- Counter ---")
cnt = Counter("abracadabra")
print(f"Counter: {cnt}")
print(f"most_common(3): {cnt.most_common(3)}")

# 计数更新
cnt.update(["a", "b", "c"])
print(f"update 后: {cnt}")

# Counter 运算
cnt1 = Counter(['a', 'b', 'c'])
cnt2 = Counter(['b', 'c', 'd'])
print(f"cnt1 + cnt2: {cnt1 + cnt2}")  # 加法
print(f"cnt1 - cnt2: {cnt1 - cnt2}")  # 减法（只保留正数）

# OrderedDict
print("\n--- OrderedDict ---")
od = OrderedDict()
od['z'] = 1
od['a'] = 2
od['m'] = 3
print(f"OrderedDict keys: {list(od.keys())}")

# namedtuple
print("\n--- namedtuple ---")
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 5)
print(f"Point: {p}")
print(f"p.x: {p.x}, p[0]: {p[0]}")
print(f"_asdict: {p._asdict()}")
print(f"_fields: {p._fields}")

p2 = Point._make([7, 9])
print(f"_make: {p2}")

p3 = p._replace(x=10)
print(f"_replace: {p3}")

# ChainMap
print("\n--- ChainMap ---")
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 100, 'c': 3}
cm = ChainMap(dict1, dict2)
print(f"ChainMap: {dict(cm)}")
print(f"cm['a']: {cm['a']}")  # 1 (第一个字典)
print(f"cm['b']: {cm['b']}")  # 2 (第一个字典优先)
print(f"cm['c']: {cm['c']}")  # 3


# ====================
# itertools 与 functools
# ====================

print("\n" + "=" * 50)
print("itertools 与 functools")
print("=" * 50)

import itertools
import functools

# itertools.count
print("--- itertools.count ---")
counter = itertools.count(1, 2)  # 1, 3, 5...
print(f"next 3次: {next(counter)}, {next(counter)}, {next(counter)}")

# itertools.cycle
print("\n--- itertools.cycle ---")
cycler = itertools.cycle([1, 2])
print(f"next 4次: {next(cycler)}, {next(cycler)}, {next(cycler)}, {next(cycler)}")

# itertools.chain
print("\n--- itertools.chain ---")
chained = list(itertools.chain([1, 2], ['a', 'b'], [True]))
print(f"chain: {chained}")

# itertools.islice
print("\n--- itertools.islice ---")
print(f"islice(range(10), 3): {list(itertools.islice(range(10), 3))}")
print(f"islice(range(10), 2, 8, 2): {list(itertools.islice(range(10), 2, 8, 2))}")

# permutations / combinations
print("\n--- permutations / combinations ---")
print(f"permutations([1,2,3], 2): {list(itertools.permutations([1, 2, 3], 2))}")
print(f"combinations([1,2,3], 2): {list(itertools.combinations([1, 2, 3], 2))}")
print(f"product([1,2], repeat=2): {list(itertools.product([1, 2], repeat=2))}")

# groupby
print("\n--- groupby ---")
data = [1, 1, 1, 2, 2, 1]
for key, group in itertools.groupby(data):
    print(f"{key}: {list(group)}")

# functools.lru_cache
print("\n--- functools.lru_cache ---")

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

import time
start = time.perf_counter()
result = fibonacci(30)
elapsed = time.perf_counter() - start
print(f"fibonacci(30) = {result}, 耗时 {elapsed:.6f}s (带缓存)")

# functools.partial
print("\n--- functools.partial ---")
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)
print(f"square(5): {square(5)}")
print(f"cube(5): {cube(5)}")

# functools.singledispatch
print("\n--- functools.singledispatch ---")

@functools.singledispatch
def process(data):
    return str(data)

@process.register(int)
def _(data):
    return f"整数: {data * 2}"

@process.register(str)
def _(data):
    return f"字符串: {data.upper()}"

print(f"process(42): {process(42)}")
print(f"process('hello'): {process('hello')}")
print(f"process(True): {process(True)}")

# functools.reduce
print("\n--- functools.reduce ---")
result = functools.reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
print(f"reduce sum: {result}")

result = functools.reduce(lambda x, y: x * y, [1, 2, 3, 4], start=2)
print(f"reduce累乘(带初始值): {result}")


# ====================
# datetime 与 time
# ====================

print("\n" + "=" * 50)
print("datetime 与 time")
print("=" * 50)

from datetime import datetime, date, time, timedelta, timezone

# datetime
print("--- datetime ---")
now = datetime.now()
print(f"now(): {now}")
print(f"year: {now.year}, month: {now.month}, day: {now.day}")
print(f"hour: {now.hour}, minute: {now.minute}, second: {now.second}")

# 创建特定 datetime
dt = datetime(2024, 12, 25, 9, 30, 0)
print(f"datetime(2024, 12, 25): {dt}")

# strftime - datetime -> 字符串
print(f"strftime('%Y-%m-%d %H:%M:%S'): {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"strftime('%B %d, %Y'): {now.strftime('%B %d, %Y')}")

# strptime - 字符串 -> datetime
dt = datetime.strptime("2024-03-15", "%Y-%m-%d")
print(f"strptime: {dt}")

# datetime 运算
print("\n--- datetime 运算 ---")
dt1 = datetime(2024, 3, 15)
dt2 = datetime(2024, 3, 20)
diff = dt2 - dt1
print(f"datetime 差值: {diff.days} 天")

# timedelta
delta = timedelta(days=5, hours=3, minutes=30)
print(f"timedelta: {delta}")

dt = datetime(2024, 3, 15) + timedelta(days=10)
print(f"datetime + timedelta: {dt}")

# date
print("\n--- date ---")
today = date.today()
print(f"date.today(): {today}")

# time
t = time(14, 30, 45)
print(f"time(14, 30, 45): {t}")
print(f"time.strftime('%H:%M:%S'): {t.strftime('%H:%M:%S')}")

# 时区
print("\n--- timezone ---")
utc_now = datetime.now(timezone.utc)
print(f"UTC now: {utc_now}")

tz = timezone(timedelta(hours=8))
bj_time = datetime(2024, 3, 15, 10, 30, tzinfo=tz)
print(f"北京时间: {bj_time}")

# 转换时区
utc_time = bj_time.astimezone(timezone.utc)
print(f"转UTC: {utc_time}")

# time 模块
print("\n--- time 模块 ---")
import time

print(f"time.time(): {time.time()}")
print(f"time.ctime(): {time.ctime()}")

# 人性化时间
print("\n--- 人性化时间展示 ---")
def humanize_time(dt):
    now = datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "刚刚"
    elif seconds < 3600:
        return f"{int(seconds / 60)}分钟前"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}小时前"
    elif seconds < 604800:
        return f"{int(seconds / 86400)}天前"
    else:
        return dt.strftime("%Y-%m-%d")

past = datetime.now() - timedelta(hours=3)
print(f"3小时前: {humanize_time(past)}")

past = datetime.now() - timedelta(days=10)
print(f"10天前: {humanize_time(past)}")


# ====================
# pathlib
# ====================

print("\n" + "=" * 50)
print("pathlib")
print("=" * 50)

from pathlib import Path

# 创建路径
print("--- 基本路径 ---")
p = Path("folder") / "subfolder" / "file.txt"
print(f"Path / 拼接: {p}")

print(f"name: {p.name}")
print(f"stem: {p.stem}")
print(f"suffix: {p.suffix}")
print(f"parent: {p.parent}")
print(f"parent.parent: {p.parent.parent}")

# 路径检查
print("\n--- 路径检查 ---")
p = Path("test_path.txt")
print(f"exists(): {p.exists()}")
print(f"is_file(): {p.is_file()}")
print(f"is_dir(): {p.is_dir()}")

# 创建测试文件
p.write_text("Hello, pathlib!")
print(f"写入后 exists(): {p.exists()}")
print(f"read_text(): {p.read_text()}")

# 遍历目录
print("\n--- 遍历目录 ---")
current = Path(".")
for item in current.iterdir():
    if item.is_file():
        print(f"文件: {item.name}")
    else:
        print(f"目录: {item.name}/")

# glob
print("\n--- glob ---")
py_files = list(Path(".").glob("*.py"))
print(f"当前目录 .py 文件数量: {len(py_files)}")

# 路径解析
print("\n--- 路径解析 ---")
p = Path("/home/user/docs/report.pdf")
print(f"name: {p.name}")
print(f"stem: {p.stem}")
print(f"suffix: {p.suffix}")
print(f"parent: {p.parent}")

# with_name / with_suffix
print("\n--- with_name / with_suffix ---")
p = Path("file.txt")
print(f"with_name('new.txt'): {p.with_name('new.txt')}")
print(f"with_suffix('.md'): {p.with_suffix('.md')}")

# 创建目录
print("\n--- 创建目录 ---")
new_dir = Path("test_dir/subdir")
new_dir.mkdir(parents=True, exist_ok=True)
print(f"mkdir parents=True: {new_dir.exists()}")
new_dir.rmdir()  # 删除空目录

# 清理测试文件
if p.exists():
    p.unlink()
    print(f"已删除测试文件: {p}")

Path("test_dir").rmdir()
print("已删除 test_dir")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("标准库示例执行完毕")
    print("=" * 50)

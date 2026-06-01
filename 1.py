"""
Python 不常见关键字 / 语法精讲
每个关键字配有"不用它时怎么写 → 用它后怎么写"的对比
"""

# ============================================================
# 1. for...else / while...else —— 没被 break 打断才走 else
# ============================================================

print("=" * 50)
print("1. for...else / while...else")
print("=" * 50)

# --- 不用 else：需要额外的标记变量 ---
numbers = [3, 7, 2, 9, 5]
target = 6

found = False
for n in numbers:
    if n == target:
        print("找到了！")
        found = True
        break
if not found:
    print("没找到（标记变量版）")

# --- 用 else：干净直接 ---
for n in numbers:
    if n == target:
        print("找到了！")
        break
else:
    print("没找到（else版）")

# --- while...else ---
n = 5
while n > 0:
    print(n, end=" ")
    n -= 1
else:
    print("→ 倒计时结束！")

# 中途 break 则不会走 else
n = 5
while n > 0:
    if n == 3:
        print("\n中途 break 了，else 不会执行")
        break
    n -= 1
else:
    print("这行不会输出")


# ============================================================
# 2. try...else —— 没异常才走的分支
# ============================================================

print("\n" + "=" * 50)
print("2. try...else")
print("=" * 50)

# --- 不推荐：安全代码也塞进 try 里 ---
try:
    result = 10 / 2
    print(f"结果：{result}")  # 这行其实不危险，却被包在 try 里了
except ZeroDivisionError:
    print("除数不能为0")

# --- 推荐：try 只放危险语句，else 放依赖成功的后续 ---
try:
    result = 10 / 2
except ZeroDivisionError:
    print("除数不能为0")
else:
    print(f"结果：{result}（来自 else）")  # 没异常才执行

# 有异常时 else 不会执行
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")
else:
    print("这行不会输出，因为异常了")


# ============================================================
# 3. nonlocal —— 修改外层函数的变量（不是全局）
# ============================================================

print("\n" + "=" * 50)
print("3. nonlocal")
print("=" * 50)

# --- 不用 nonlocal：报错 ---
# def make_counter():
#     count = 0
#     def increment():
#         count += 1   # ❌ UnboundLocalError
#         return count
#     return increment

# --- 用 nonlocal：正确 ---
def make_counter():
    count = 0
    def increment():
        nonlocal count       # 👈 告诉 Python：用外层函数的 count
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3

# --- nonlocal vs global 对比 ---
x = "全局X"

def outer():
    x = "外层X"

    print(f"outer 里的 x 一开始是：{x}")
    # nonlocal 用法：在 inner 里写 `nonlocal x` 后再赋值，改的是 outer 的 x
    # global  用法：在 inner 里写 `global x` 后再赋值，改的是模块最外层的 x

outer()


# ============================================================
# 4. yield from —— 委托给另一个生成器
# ============================================================

print("\n" + "=" * 50)
print("4. yield from")
print("=" * 50)

# --- 不用 yield from：手动双层 for ---
def flatten_manual(matrix):
    for row in matrix:
        for item in row:
            yield item

# --- 用 yield from：内层 for 变一行 ---
def flatten(matrix):
    for row in matrix:
        yield from row          # 等于 for item in row: yield item

matrix = [[1, 2], [3, 4], [5]]
print(list(flatten(matrix)))    # [1, 2, 3, 4, 5]

# --- 嵌套生成器场景 ---
def sub_task(name):
    yield f"{name}-步骤1"
    yield f"{name}-步骤2"

def main_task():
    yield "主任务-开始"
    yield from sub_task("A")
    yield from sub_task("B")
    yield "主任务-结束"

for step in main_task():
    print(step)
# 输出：
# 主任务-开始
# A-步骤1
# A-步骤2
# B-步骤1
# B-步骤2
# 主任务-结束


# ============================================================
# 5. raise X from Y —— 保留异常链
# ============================================================

print("\n" + "=" * 50)
print("5. raise ... from")
print("=" * 50)

# --- 不用 from：底层信息丢失 ---
try:
    int("abc")
except ValueError as e:
    print("包装异常时，原始 ValueError 信息容易丢失")

# --- 用 from：完整保留因果链 ---
try:
    int("abc")
except ValueError as e:
    print("raise RuntimeError from e：异常链完整保留")
    # raise RuntimeError("配置值必须是数字") from e
    # 上面这行被注释掉，否则程序会终止

# --- from None：显式隐藏原因 ---
try:
    int("abc")
except ValueError:
    print("raise RuntimeError from None：显式切断了异常链")
    # raise RuntimeError("配置值必须是数字") from None


# ============================================================
# 6. assert —— 开发期"不许错"（线上可能被跳过）
# ============================================================

print("\n" + "=" * 50)
print("6. assert")
print("=" * 50)

def remove_last(lst):
    """去掉列表最后一个元素，要求列表非空"""
    assert len(lst) > 0, "不能对空列表执行 pop"
    return lst.pop()

print(remove_last([1, 2, 3]))  # 3

# remove_last([])  # 这行会触发 AssertionError

# ⚠️ assert 不能用于业务校验！
# 用 python -O 运行时所有 assert 会被跳过

# ✅ 业务校验用 raise
def apply_discount(price):
    if price <= 0:
        raise ValueError("价格必须为正")
    return price * 0.9

print(f"打折后：{apply_discount(100)}")  # 90.0


# ============================================================
# 7. match / case —— 模式匹配（Python 3.10+）
# ============================================================

print("\n" + "=" * 50)
print("7. match / case")
print("=" * 50)

# --- 基础：匹配值 ---
status = 404

match status:
    case 200 | 201 | 204:          # | 就是"或"
        print("HTTP 成功")
    case 301 | 302:
        print("HTTP 重定向")
    case 404:
        print("HTTP 未找到")        # 👈 匹配这个
    case _:                         # _ 匹配任意值，相当于 else
        print("其他状态码")

# --- 进阶：拆解元组结构 ---
response = ("error", "数据库连接超时")

match response:
    case ("ok", data):
        print(f"成功，数据：{data}")
    case ("error", msg):
        print(f"失败，原因：{msg}")   # 👈 匹配这个
    case _:
        print("未知格式")

# --- 守卫条件 ---
point = (3, 7)

match point:
    case (x, y) if x == y:
        print(f"在对角线上：({x}, {y})")
    case (x, y) if x + y == 10:
        print(f"和为10：({x}, {y})")   # 👈 匹配这个
    case (x, y):
        print(f"普通点：({x}, {y})")

# --- 拆解列表 ---
command = ["go", "north"]

match command:
    case ["quit"]:
        print("退出")
    case ["go", direction]:
        print(f"向{direction}移动")   # 👈 匹配这个
    case _:
        print("未知命令")


# ============================================================
# 8. del —— 删键、删元素、删变量
# ============================================================

print("\n" + "=" * 50)
print("8. del")
print("=" * 50)

# 删字典的键
cache = {"a": 1, "b": 2, "c": 3}
del cache["b"]
print(f"删键后：{cache}")    # {'a': 1, 'c': 3}

# 删列表元素
items = [10, 20, 30, 40, 50]
del items[1]                # 删索引1
print(f"删索引1后：{items}")  # [10, 30, 40, 50]

# 切片删除
items = [10, 20, 30, 40, 50]
del items[1:3]              # 删索引1到2
print(f"切片删除后：{items}")  # [10, 40, 50]

# 删变量（通常不需要，仅做演示）
temp = "这条数据用完可以删"
print(temp)
del temp
# print(temp)  # ❌ NameError: name 'temp' is not defined


# ============================================================
# 9. async for / async with —— 异步迭代与上下文
# ============================================================

print("\n" + "=" * 50)
print("9. async for / async with")
print("=" * 50)

import asyncio

# --- async for ---
async def event_stream():
    """模拟异步数据源，每隔 0.1 秒产出一个事件"""
    for i in range(3):
        await asyncio.sleep(0.1)
        yield f"事件{i}"

async def consumer():
    async for event in event_stream():  # 👈 async for
        print(f"收到：{event}")

print("运行 async for 示例：")
asyncio.run(consumer())

# --- async with ---
class AsyncLock:
    """模拟一个异步锁"""
    async def __aenter__(self):
        print("  🔒 锁已获取")
        return self

    async def __aexit__(self, *_):
        print("  🔓 锁已释放")

async def critical_section():
    async with AsyncLock():            # 👈 async with
        print("  执行关键代码...")

print("\n运行 async with 示例：")
asyncio.run(critical_section())


# ============================================================
# 速查对照表
# ============================================================
print("\n" + "=" * 50)
print("速查表")
print("=" * 50)
print("""
for...else      → 循环没被 break 就执行
while...else    → 同上
try...else      → 没异常就执行
nonlocal        → 改外层函数（非全局）的变量
yield from      → 把产出委托给另一个生成器
raise X from Y  → 抛 X 的同时保留原始异常 Y
assert          → 开发期检查，线上 python -O 会跳过
match/case      → 模式匹配，能拆元组/列表/对象
del             → 删键、删元素、删变量
async for       → 异步迭代
async with      → 异步上下文管理
""")

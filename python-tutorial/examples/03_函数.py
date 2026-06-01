"""
第三章：函数 示例代码
配合 03_函数/ 目录下的 Markdown 文档学习
"""

# ====================
# 01 函数定义与调用
# ====================

print("=" * 50)
print("01 函数定义与调用")
print("=" * 50)

# 函数是对象
def greet():
    return "hello"

print(f"greet: {greet}")
print(f"greet(): {greet()}")

f = greet  # 赋值给变量
print(f"f(): {f()}")

# 参数传递
def modify_int(x):
    x = 10

a = 5
modify_int(a)
print(f"不可变 int: a={a}")  # a 不变

def modify_list(lst):
    lst.append(4)

my_list = [1, 2, 3]
modify_list(my_list)
print(f"可变 list: my_list={my_list}")  # 被修改

# 默认值陷阱
def bad_append(item, target=[]):
    target.append(item)
    return target

print(f"bad_append(1)={bad_append(1)}")  # [1]
print(f"bad_append(2)={bad_append(2)}")  # [1, 2] ← 预期 [2]!

# 正确做法
def good_append(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target

print(f"good_append(1)={good_append(1)}")  # [1]
print(f"good_append(2)={good_append(2)}")  # [2]


# ====================
# 02 参数详解
# ====================

print("\n" + "=" * 50)
print("02 参数详解")
print("=" * 50)

# *args 可变位置参数
def sum_all(*args):
    return sum(args)

print(f"sum_all(1,2,3) = {sum_all(1, 2, 3)}")

# **kwargs 可变关键字参数
def print_info(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")

print_info(name="Alice", age=30)

# 解包传参
nums = [1, 2, 3]
print(f"*解包: {sum_all(*nums)}")

info = {"name": "Bob", "city": "NYC"}
print_info(**info)

# 关键字-only 参数
def greet(name, *, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", greeting="Hi"))

# 组合使用
def func(pos1, pos2, *args, kw_only="default", **kwargs):
    print(f"pos={pos1},{pos2}, args={args}, kw={kw_only}, kwargs={kwargs}")

func(1, 2, 3, 4, kw_only="custom", extra="value")


# ====================
# 03 lambda 与闭包
# ====================

print("\n" + "=" * 50)
print("03 lambda 与闭包")
print("=" * 50)

# lambda 基础
square = lambda x: x ** 2
print(f"lambda square(5) = {square(5)}")

# lambda 用于排序
words = ["apple", "banana", "cherry", "date"]
words.sort(key=lambda x: len(x))
print(f"按长度排序: {words}")

# 闭包：计数器
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
print(f"计数器: {c()}, {c()}, {c()}")

# 闭包陷阱
def create_funcs():
    funcs = []
    for i in range(3):
        funcs.append(lambda i=i: i)  # 用默认参数绑定当前值
    return funcs

for f in create_funcs():
    print(f"闭包陷阱修复: {f()}", end=" ")
print()


# ====================
# 04 装饰器
# ====================

print("\n" + "=" * 50)
print("04 装饰器")
print("=" * 50)

import functools
import time

# 简单装饰器
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("调用前")
        result = func(*args, **kwargs)
        print("调用后")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("hello!")

say_hello()

# 带参数的装饰器
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(times=3)
def say_hi():
    print("hi!")

say_hi()

# 计时装饰器
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 耗时 {elapsed:.6f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.1)

slow_function()

# 叠加装饰器
def decorator1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("1 start")
        result = func(*args, **kwargs)
        print("1 end")
        return result
    return wrapper

def decorator2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("2 start")
        result = func(*args, **kwargs)
        print("2 end")
        return result
    return wrapper

@decorator1
@decorator2
def greet():
    print("hello")

greet()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

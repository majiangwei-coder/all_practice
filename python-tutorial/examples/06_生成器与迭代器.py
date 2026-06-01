"""
第六章：生成器与迭代器 示例代码
配合 06_进阶主题/ 目录下的 Markdown 文档学习
"""

# ====================
# 迭代器协议
# ====================

print("=" * 50)
print("迭代器协议")
print("=" * 50)

# 迭代器协议
my_iter = iter([1, 2, 3])
print(f"iter([1,2,3]): {my_iter}")
print(f"next(my_iter): {next(my_iter)}")
print(f"next(my_iter): {next(my_iter)}")
print(f"next(my_iter): {next(my_iter)}")

# 可迭代对象 vs 迭代器
print("\n--- 可迭代对象 vs 迭代器 ---")
lst = [1, 2, 3]
print(f"list 是可迭代对象: {hasattr(lst, '__iter__')}")
print(f"iter(list) 是迭代器: {hasattr(iter(lst), '__next__')}")

# ====================
# 生成器函数
# ====================

print("\n" + "=" * 50)
print("生成器函数")
print("=" * 50)

def count_up_to(n):
    """生成 1 到 n 的生成器"""
    i = 1
    while i <= n:
        yield i
        i += 1

# 使用生成器
print("--- count_up_to ---")
for num in count_up_to(5):
    print(f"生成: {num}", end=" ")
print()

# 生成器对象
generator = count_up_to(3)
print(f"\n生成器对象: {generator}")
print(f"类型: {type(generator)}")

# ====================
# 生成器表达式
# ====================

print("\n" + "=" * 50)
print("生成器表达式")
print("=" * 50)

# 列表推导式（立即求值）
list_comp = [x ** 2 for x in range(5)]
print(f"列表推导式: {list_comp}")

# 生成器表达式（惰性求值）
gen_exp = (x ** 2 for x in range(5))
print(f"生成器表达式: {gen_exp}")
print(f"next(gen_exp): {next(gen_exp)}")
print(f"next(gen_exp): {next(gen_exp)}")

# 转换为列表
print(f"list(gen_exp): {list(gen_exp)}")

# ====================
# itertools 模块
# ====================

print("\n" + "=" * 50)
print("itertools 模块")
print("=" * 50)

import itertools

# count - 无限计数器
print("--- count ---")
counter = itertools.count(start=1, step=2)  # 1, 3, 5, 7...
print(f"next(counter): {next(counter)}")  # 1
print(f"next(counter): {next(counter)}")  # 3

# cycle - 无限循环
print("\n--- cycle ---")
cycler = itertools.cycle([1, 2, 3])
for _ in range(7):
    print(f"next(cycle): {next(cycler)}", end=" ")
print()

# repeat - 重复
print("\n--- repeat ---")
rep = itertools.repeat("x", 3)
print(f"list(repeat('x', 3)): {list(rep)}")

# accumulate - 累加
print("\n--- accumulate ---")
import operator
acc = itertools.accumulate([1, 2, 3, 4, 5])
print(f"累加: {list(acc)}")  # [1, 3, 6, 10, 15]

acc_mul = itertools.accumulate([1, 2, 3, 4], operator.mul)
print(f"累乘: {list(acc_mul)}")  # [1, 2, 6, 24]

# chain - 连接
print("\n--- chain ---")
chained = itertools.chain([1, 2], ['a', 'b'], [True, False])
print(f"chain: {list(chained)}")

# compress - 按掩码筛选
print("\n--- compress ---")
data = ['a', 'b', 'c', 'd']
selectors = [1, 0, 1, 0]
print(f"compress: {list(itertools.compress(data, selectors))}")

# dropwhile / takewhile
print("\n--- dropwhile / takewhile ---")
print(f"dropwhile(x<3): {list(itertools.dropwhile(lambda x: x < 3, [1, 2, 3, 4, 1, 2]))}")
print(f"takewhile(x<3): {list(itertools.takewhile(lambda x: x < 3, [1, 2, 3, 4, 1, 2]))}")

# islice - 切片
print("\n--- islice ---")
print(f"islice(range(10), 3): {list(itertools.islice(range(10), 3))}")
print(f"islice(range(10), 2, 8, 2): {list(itertools.islice(range(10), 2, 8, 2))}")

# permutations - 排列
print("\n--- permutations ---")
print(f"permutations([1,2,3]): {list(itertools.permutations([1, 2, 3]))}")
print(f"permutations([1,2,3], 2): {list(itertools.permutations([1, 2, 3], 2))}")

# combinations - 组合
print("\n--- combinations ---")
print(f"combinations([1,2,3], 2): {list(itertools.combinations([1, 2, 3], 2))}")

# combinations_with_replacement
print("\n--- combinations_with_replacement ---")
print(f"combinations_with_replacement([1,2], 3): {list(itertools.combinations_with_replacement([1, 2], 3))}")

# product - 笛卡尔积
print("\n--- product ---")
print(f"product([1,2], ['a','b']): {list(itertools.product([1, 2], ['a', 'b']))}")

# groupby - 分组
print("\n--- groupby ---")
data = [1, 1, 1, 2, 2, 1]
for key, group in itertools.groupby(data):
    print(f"{key}: {list(group)}")

# zip_longest
print("\n--- zip_longest ---")
a = [1, 2, 3]
b = ['a', 'b']
print(f"zip_longest: {list(itertools.zip_longest(a, b, fillvalue=None))}")

# ====================
# 生成器实际应用
# ====================

print("\n" + "=" * 50)
print("生成器实际应用")
print("=" * 50)

# 斐波那契（无限序列）
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print("--- 斐波那契 ---")
fibs = fibonacci()
for _ in range(10):
    print(next(fibs), end=" ")
print()

# 管道处理
def filter_positive(numbers):
    for n in numbers:
        if n > 0:
            yield n

def square(numbers):
    for n in numbers:
        yield n ** 2

def take(n, iterable):
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item

print("\n--- 管道处理 ---")
pipeline = square(filter_positive([-2, -1, 0, 1, 2, 3]))
print(f"管道 (filter -> square -> take 3): {list(take(3, pipeline))}")

# send() 与生成器
print("\n--- send() 方法 ---")
def counter():
    count = 0
    while True:
        increment = yield count
        if increment is not None:
            count += increment
        else:
            count += 1

c = counter()
print(f"next(c): {next(c)}")    # 0 (启动)
print(f"c.send(5): {c.send(5)}")  # 5 (发送 5，count+=5)
print(f"next(c): {next(c)}")    # 6 (increment is None, count+=1)

# yield from
print("\n--- yield from ---")
def gen1():
    yield 1
    yield 2

def gen2():
    yield from gen1()
    yield 3

print(f"gen2 with yield from: {list(gen2())}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

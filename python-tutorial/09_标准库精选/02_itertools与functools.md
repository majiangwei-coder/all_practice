# itertools 与 functools

## itertools：迭代器工具

### 无限迭代器

```python
import itertools

# count(start=0, step=1) - 无限计数器
counter = itertools.count(start=1, step=2)  # 1, 3, 5, 7...
print(next(counter))  # 1
print(next(counter))  # 3

# cycle(iterable) - 无限循环
cycler = itertools.cycle([1, 2, 3])  # 1, 2, 3, 1, 2, 3...
print(next(cycler))  # 1

# repeat(elem, times=None) - 重复
rep = itertools.repeat("x", 3)  # x, x, x
print(list(rep))  # ['x', 'x', 'x']
```

### 有限迭代器

```python
# accumulate(iterable, func=operator.add)
import itertools
import operator

acc = itertools.accumulate([1, 2, 3, 4, 5])
print(list(acc))  # [1, 3, 6, 10, 15]  (累加)

acc2 = itertools.accumulate([1, 2, 3, 4], operator.mul)
print(list(acc2))  # [1, 2, 6, 24]  (累乘)

# chain(*iterables) - 连接多个迭代器
combined = itertools.chain([1, 2], ['a', 'b'], [True, False])
print(list(combined))  # [1, 2, 'a', 'b', True, False]

# chain.from_iterable - 展平
flattened = itertools.chain.from_iterable([[1, 2], [3, 4]])
print(list(flattened))  # [1, 2, 3, 4]

# compress(data, selectors) - 按掩码选择
data = ['a', 'b', 'c', 'd']
selectors = [1, 0, 1, 0]
print(list(itertools.compress(data, selectors)))  # ['a', 'c']

# dropwhile(predicate, iterable) - 条件为真时丢弃
print(list(itertools.dropwhile(lambda x: x < 3, [1, 2, 3, 4, 1, 2])))
# [3, 4, 1, 2]

# takewhile - 条件为真时保留
print(list(itertools.takewhile(lambda x: x < 3, [1, 2, 3, 4, 1, 2])))
# [1, 2]

# filterfalse - 保留条件为假的
print(list(itertools.filterfalse(lambda x: x % 2, [1, 2, 3, 4, 5])))
# [2, 4]  (偶数)

# islice(iterable, stop) / islice(iterable, start, stop, step)
print(list(itertools.islice(range(10), 3)))      # [0, 1, 2]
print(list(itertools.islice(range(10), 2, 8, 2))) # [2, 4, 6]
```

### 排列组合迭代器

```python
# permutations - 排列
print(list(itertools.permutations([1, 2, 3])))
# [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

print(list(itertools.permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# combinations - 组合（不考虑顺序）
print(list(itertools.combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]

# combinations_with_replacement - 带重复组合
print(list(itertools.combinations_with_replacement([1, 2], 3)))
# [(1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2)]

# product - 笛卡尔积
print(list(itertools.product([1, 2], ['a', 'b'])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

print(list(itertools.product([0, 1], repeat=3)))
# [(0, 0, 0), (0, 0, 1), (0, 1, 0), ...] (8 个)
```

### 分组迭代

```python
# groupby(iterable, key=None) - 相邻元素分组
from itertools import groupby

data = [1, 1, 1, 2, 2, 1]
for key, group in groupby(data):
    print(f"{key}: {list(group)}")
# 1: [1, 1, 1]
# 2: [2, 2]
# 1: [1]

# 配合 key 函数
data = ["apple", "apricot", "banana", "blueberry"]
for key, group in groupby(data, key=len):
    print(f"{key}: {list(group)}")
# 5: ['apple', 'apricot']
# 6: ['banana']
# 9: ['blueberry']
```

### zip_longest

```python
from itertools import zip_longest

a = [1, 2, 3]
b = ['a', 'b']
print(list(zip_longest(a, b, fillvalue=None)))
# [(1, 'a'), (2, 'b'), (3, None)]
```

## functools：函数式工具

### lru_cache：记忆化

```python
import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 不再重复计算，大幅加速
print(fibonacci(100))  # 很快
```

### cache (Python 3.9+)

```python
@functools.cache  # 无大小限制，等价于 lru_cache(maxsize=None)
def heavy_computation(n):
    return n ** 2
```

### wraps：保留函数元数据

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def original():
    """原始文档"""
    pass

print(original.__name__)  # 'original' (否则是 'wrapper')
print(original.__doc__)   # '原始文档'
```

### partial：偏函数

```python
import functools

# 固定函数的部分参数
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# 带位置参数
def greet(greeting, name):
    return f"{greeting}, {name}!"

hello = functools.partial(greet, "Hello")
print(hello("Alice"))  # "Hello, Alice!"
```

### singledispatch：函数重载

```python
import functools

@functools.singledispatch
def process(data):
    """默认处理"""
    return str(data)

@process.register(int)
def _(data):
    return f"整数: {data * 2}"

@process.register(str)
def _(data):
    return f"字符串: {data.upper()}"

@process.register(list)
def _(data):
    return f"列表: {len(data)} 项"

print(process(42))        # 整数: 84
print(process("hello"))   # 字符串: HELLO
print(process([1, 2, 3])) # 列表: 3 项
print(process(True))      # 默认处理: True
```

### cmp_to_key：自定义排序

```python
import functools

# 将比较函数转换为 key 函数
def compare_length(a, b):
    return len(a) - len(b)

sorted_words = sorted(["apple", "hi", "banana"], key=functools.cmp_to_key(compare_length))
print(sorted_words)  # ['hi', 'apple', 'banana']
```

### reduce

```python
import functools

# Python 3 中 reduce 在 functools
result = functools.reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
print(result)  # 15

# 带初始值
result = functools.reduce(lambda x, y: x * y, [1, 2, 3, 4], start=2)
print(result)  # 48
```

### total_ordering：自动生成比较方法

```python
import functools

@functools.total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        return self.grade == other.grade

    def __lt__(self, other):
        return self.grade < other.grade

# 自动生成 <=, >, >=

s1 = Student("Alice", 90)
s2 = Student("Bob", 85)
print(s1 > s2)   # True
print(s1 <= s2)  # False
```

## 实际应用示例

### 1. 生成密码组合

```python
import itertools

chars = "abcdefghijklmnopqrstuvwxyz0123456789"
for combination in itertools.product(chars, repeat=3):
    print(''.join(combination))
```

### 2. 快速查找

```python
import itertools

# 找第一个满足条件的组合
for combo in itertools.product(range(10), repeat=2):
    if combo[0] * combo[1] == 24:
        print(f"找到: {combo}")  # (4, 6) 或 (6, 4)
        break
```

### 3. 批量处理大数据

```python
import itertools

def process_batch(items):
    return [item * 2 for item in items]

batch_size = 1000
large_dataset = range(10000)

batches = itertools.batched(large_dataset, batch_size)
for batch in batches:
    results = process_batch(batch)
    save_to_database(results)
```

## 小结

### itertools

| 函数 | 用途 |
|------|------|
| `count/cycle/repeat` | 无限迭代器 |
| `chain` | 连接多个迭代器 |
| `islice` | 切片迭代器 |
| `takewhile/dropwhile` | 条件筛选 |
| `permutations/combinations` | 排列组合 |
| `groupby` | 分组 |
| `zip_longest` | 配对（不等长） |

### functools

| 函数 | 用途 |
|------|------|
| `@lru_cache` | 记忆化缓存 |
| `@wraps` | 保留函数元数据 |
| `partial` | 偏函数 |
| `@singledispatch` | 函数重载 |
| `cmp_to_key` | 比较函数转 key |
| `reduce` | 聚合 |
| `@total_ordering` | 自动比较方法 |

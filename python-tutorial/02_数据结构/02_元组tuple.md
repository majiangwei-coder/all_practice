# 元组 tuple

## 本质：不可变的顺序表

tuple 是**不可变的序列**，一旦创建不能修改。

```python
t = (1, 2, 3)
t[0] = 10   # TypeError: 'tuple' object does not support item assignment
```

## 创建

```python
# 基本创建
empty = ()              # 空元组
single = (42,)          # 单元素元组（逗号必须有！）
t = (1, 2, 3)           # 多元素

# 构造器
tuple("abc")            # ('a', 'b', 'c')
tuple([1, 2, 3])        # (1, 2, 3)
tuple(range(3))         # (0, 1, 2)

# 打包 vs 解包
point = (3, 5)          # 打包 (packing)
x, y = point            # 解包 (unpacking)
```

## 解包详解

```python
# 基本解包
a, b, c = (1, 2, 3)     # a=1, b=2, c=3

# 交换变量（无需临时变量）
a, b = 1, 2
a, b = b, a             # a=2, b=1

# 用 * 收集剩余元素
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5

# 嵌套解包
(a, b), (c, d) = [(1, 2), (3, 4)]
# a=1, b=2, c=3, d=4

# _ 占位符（不关心的值）
a, _, c = (1, 2, 3)     # a=1, c=3，2被丢弃
```

## tuple 的"可变"假象

```python
# 外层不可变，但内层可变
t = ([1, 2], [3, 4])
t[0].append(99)         # 合法！t=([1,2,99], [3,4])

# 不能替换元素
t[0] = [5, 6]           # TypeError！
```

### 图示

```
tuple 的"不变性"：
  t = ([1,2], [3,4])
       ↓       ↓
      [1,2]   [3,4]    ← 这两个列表对象本身可变
       ↑       ↑
  t[0] ────── t[1]     ← 元组持有的是引用，不能改变

但不能做：
  t[0] = [5, 6]         # 试图改变元组中的引用 → 报错
```

## 为什么 tuple 不可变还要它？

### 1. 安全：防止意外修改

```python
# 函数返回坐标，调用者不能修改
def get_position():
    return (100, 200)

pos = get_position()
pos[0] = 50   # 报错，保证数据不被篡改
```

### 2. 性能：内部优化

```python
import sys

# tuple 比 list 占用更少内存
lst = [1, 2, 3]
tup = (1, 2, 3)
print(sys.getsizeof(lst))  # 64 (或更大)
print(sys.getsizeof(tup))  # 56 (更小)

# 元组创建更快
import timeit
timeit.timeit('(1,2,3)', number=10000000)   # 更快
timeit.timeit('[1,2,3]', number=10000000)   # 稍慢
```

### 3. 可作为 dict 的 key 和 set 的元素

```python
# dict key 必须是不可变类型
d = {(1, 2): "点A", (3, 4): "点B"}  # OK
d = {[1, 2]: "点A"}                 # 报错！list 不可哈希

# set 元素必须是不可变类型
s = {1, 2, (3, 4)}   # OK
s = {1, 2, [3, 4]}   # 报错！
```

### 4. 协程和生成器的原生支持

```python
# 多返回值本质是 tuple
def divide(a, b):
    return a // b, a % b

quotient, remainder = divide(10, 3)  # 解包
result = divide(10, 3)              # result 是 tuple
```

## namedtuple：带名字的元组

```python
from collections import namedtuple

# 创建命名元组类型
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 5)

# 既可以用索引，也可以用名字访问
print(p[0], p.x)        # 3 3
print(p[1], p.y)        # 5 5

# 元组特性：不可变
p.x = 10   # AttributeError

# 方法
p._fields   # ('x', 'y')
p._asdict() # {'x': 3, 'y': 5}
```

## 常用操作

```python
t = (1, 2, 3, 2, 1)

t.index(2)      # 1   (第一个 2 的位置)
t.count(2)      # 2   (2 出现的次数)
2 in t          # True
len(t)          # 5
max(t), min(t)  # 3, 1
t + (4, 5)      # (1,2,3,2,1,4,5) (拼接，不修改原tuple)
t * 2           # (1,2,3,2,1,1,2,3,2,1) (重复)
```

## tuple vs list 选择

| 场景 | 选 tuple |
|------|----------|
| 数据不应改变 | tuple |
| 作为字典 key | tuple |
| 作为 set 元素 | tuple |
| 追求性能 | tuple |
| 需要修改 | list |
| 需要频繁增删 | list |

## 小结

1. **不可变**：tuple 创建后不能修改元素
2. **可哈希**：元素都是不可变时，tuple 可作 dict key / set 元素
3. **性能优于 list**：更小、更快
4. **解包**是强大特性：`*rest`、`a, b = pair`
5. **namedtuple** 提供命名字段，适合表示结构化数据

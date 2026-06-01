# 列表 list

> 列表是 Python 最常用的数据结构之一。本章详细讲解列表的创建、操作、性能特点，以及常见误区。

---

## 1. 列表是什么

列表是 Python 的**有序、可变序列**。

- **有序**：元素有顺序，可以通过索引访问
- **可变**：创建后可以添加、删除、修改元素
- **序列**：成员有序排列，支持索引和切片

```python
# 创建一个列表
fruits = ["apple", "banana", "cherry"]
print(fruits)  # ['apple', 'banana', 'cherry']

# 列表可以包含任意类型
mixed = [1, "hello", 3.14, True, None]
print(mixed)  # [1, 'hello', 3.14, True, None]

# 列表可以嵌套
matrix = [[1, 2], [3, 4], [5, 6]]
print(matrix)  # [[1, 2], [3, 4], [5, 6]]
```

---

## 2. 创建列表

### 多种创建方式

```python
# ========== 方式1：直接创建 ==========
empty = []              # 空列表
numbers = [1, 2, 3]    # 有初始值
mixed = [1, "a", True] # 混合类型

# ========== 方式2：list() 构造函数 ==========
# 从字符串创建（把字符串的每个字符变成列表元素）
chars = list("hello")
print(chars)  # ['h', 'e', 'l', 'l', 'o']

# 从元组创建
lst = list((1, 2, 3))
print(lst)  # [1, 2, 3]

# 从 range 创建
lst = list(range(5))
print(lst)  # [0, 1, 2, 3, 4]

# ========== 方式3：列表推导式（后面章节详讲）==========
squares = [x ** 2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]
```

---

## 3. 索引与切片

### 索引（从 0 开始）

```python
lst = [10, 20, 30, 40, 50]

# 正向索引：从左边开始，0 是第一个
print(lst[0])   # 10  ← 第一个元素
print(lst[1])   # 20  ← 第二个元素
print(lst[2])   # 30  ← 第三个元素

# 负向索引：从右边开始，-1 是最后一个
print(lst[-1])   # 50  ← 最后一个元素
print(lst[-2])   # 40  ← 倒数第二个元素
print(lst[-3])   # 30  ← 倒数第三个元素

# 越界会报错！
# print(lst[10])   # IndexError: list index out of range
```

### 图解索引

```
列表:   [  10,   20,   30,   40,   50  ]
索引:      0     1     2     3     4
负索引:   -5    -4    -3    -2    -1
```

### 切片（截取子列表）

```python
lst = [10, 20, 30, 40, 50]

# 基本语法：lst[起始:结束] （注意：不包含结束位置！）
print(lst[1:4])   # [20, 30, 40]  ← 索引1到3，不包含4

# 省略起始：从头开始
print(lst[:3])    # [10, 20, 30]  ← 从0到2

# 省略结束：到末尾
print(lst[3:])    # [40, 50]     ← 从3到末尾

# 负数切片
print(lst[:-1])   # [10, 20, 30, 40]  ← 最后一个不要
print(lst[-3:])   # [30, 40, 50]       ← 最后三个

# 切片是副本（创建新列表，不影响原列表）
original = [1, 2, 3]
copied = original[:]  # 切片复制
copied.append(4)
print(original)  # [1, 2, 3]  ← 原列表不变！
print(copied)    # [1, 2, 3, 4]
```

### 切片高级用法

```python
lst = [10, 20, 30, 40, 50]

# 步长切片：lst[起始:结束:步长]
print(lst[::2])    # [10, 30, 50]  ← 每隔一个取一个
print(lst[1::2])   # [20, 40]     ← 从索引1开始，每隔一个

# 反转列表
print(lst[::-1])   # [50, 40, 30, 20, 10]  ← 倒序

# 复制列表（等价于 lst[:]）
print(lst[::])     # [10, 20, 30, 40, 50]  ← 完整副本
```

---

## 4. 添加元素

### append() - 末尾追加（最常用）

```python
lst = [1, 2, 3]
lst.append(4)      # 在末尾添加单个元素
print(lst)         # [1, 2, 3, 4]

# append 一次只加一个元素
lst.append([5, 6])
print(lst)         # [1, 2, 3, 4, [5, 6]]  ← 列表作为整体被添加！
```

### extend() - 合并列表

```python
lst = [1, 2, 3]
lst.extend([4, 5, 6])  # 合并另一个列表
print(lst)             # [1, 2, 3, 4, 5, 6]

# extend 和 += 是等价的
lst += [7, 8]
print(lst)             # [1, 2, 3, 4, 5, 6, 7, 8]
```

### insert() - 任意位置插入

```python
lst = [1, 2, 3]
lst.insert(1, 100)  # 在索引1的位置插入100
print(lst)          # [1, 100, 2, 3]
```

**注意**：insert 操作涉及元素移动，**头部插入效率低**，末尾追加效率高。

---

## 5. 删除元素

```python
lst = [1, 2, 3, 4, 3]

# remove() - 删除第一个匹配的元素
lst.remove(3)     # 删除第一个3
print(lst)         # [1, 2, 4, 3]

# remove() 如果元素不存在会报错
# lst.remove(99)   # ValueError: list.remove(x): x not in list

# pop() - 弹出末尾元素（并返回）
last = lst.pop()
print(last)         # 3
print(lst)          # [1, 2, 4]

# pop(i) - 弹出指定索引的元素
second = lst.pop(1)
print(second)       # 2
print(lst)          # [1, 4]

# del - 删除指定位置（不返回）
lst = [1, 2, 3, 4]
del lst[0]
print(lst)          # [2, 3, 4]

# del 也可以删除切片
del lst[1:3]
print(lst)          # [2]

# clear() - 清空列表
lst.clear()
print(lst)          # []
```

---

## 6. 查找与统计

```python
lst = [1, 2, 3, 4, 3]

# index() - 查找元素位置（第一个匹配的）
pos = lst.index(3)
print(pos)          # 2 ← 3 第一次出现在索引2

# index() 可以指定搜索范围
pos = lst.index(3, 3)  # 从索引3开始找
print(pos)          # 4 ← 在索引4找到了

# count() - 统计元素出现次数
cnt = lst.count(3)
print(cnt)          # 2 ← 3出现了2次

# in - 判断元素是否存在
print(3 in lst)     # True
print(99 in lst)    # False
```

---

## 7. 排序与反转

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# sort() - 原地排序（修改原列表）
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# 降序排序
numbers.sort(reverse=True)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]

# sorted() - 返回新列表（不修改原列表）
numbers = [3, 1, 4, 1, 5]
sorted_nums = sorted(numbers)
print(numbers)     # [3, 1, 4, 1, 5]  ← 原列表不变
print(sorted_nums)  # [1, 1, 3, 4, 5]  ← 新列表

# reverse() - 原地反转
numbers.reverse()
print(numbers)  # [5, 1, 4, 1, 3]

# 按长度排序（key 参数）
words = ["apple", "hi", "banana"]
words.sort(key=len)  # 按字符串长度排序
print(words)  # ['hi', 'apple', 'banana']

# 按长度降序
words.sort(key=len, reverse=True)
print(words)  # ['banana', 'apple', 'hi']
```

---

## 8. 复制的坑（重要！）

这是 Python 新手最常犯的错误之一：

```python
# 浅拷贝的问题
a = [[1, 2], [3, 4]]
b = a            # 错误！这不是复制，是同一引用
c = a.copy()    # 浅拷贝：外层是新对象，但内层还是共享的
d = list(a)     # 同上
e = a[:]         # 同上

# 验证
b.append(5)     # b 和 a 都会变
print(a)         # [[1, 2], [3, 4], 5]  ← 变了！

c[0].append(99)  # 修改内层列表，a 也会变！
print(a)           # [[1, 2, 99], [3, 4], 5]  ← 内层变了！

# 深拷贝（完全独立）
import copy
f = copy.deepcopy(a)  # 完全独立的副本
f[0].append(100)
print(a)  # 不变！ ← 真正的独立副本
```

### 图解浅拷贝 vs 深拷贝

```
浅拷贝：
    a ──┬──→ [[1,2], [3,4]] ←── c
        │         ↑
        └─────────┘ (内层列表是共享的)

深拷贝：
    a ───→ [[1,2], [3,4]] ←── f (完全独立)
```

---

## 9. 性能特点

理解性能特点，写出高效代码：

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `lst[i]` | O(1) | 随机访问，极快 |
| `lst.append()` | O(1) | 末尾追加，均摊 |
| `lst.pop()` | O(1) | 末尾弹出 |
| `lst.insert(0, x)` | O(n) | **头部插入，很慢！** |
| `lst.remove(x)` | O(n) | 按值删除，需遍历 |
| `x in lst` | O(n) | 成员测试，需遍历 |
| `lst.pop(0)` | O(n) | 头部弹出，需移动所有元素 |

### 性能建议

```python
# ❌ 低效：在头部频繁插入
lst = []
for i in range(10000):
    lst.insert(0, i)  # 每次都移动所有元素，O(n²)

# ✅ 高效：使用 deque（在头部插入也是 O(1)）
from collections import deque
dq = deque()
for i in range(10000):
    dq.appendleft(i)  # O(1)，很快
```

---

## 10. 列表的替代品

### deque - 双端队列

当需要频繁在头部插入/删除时，用 `deque`：

```python
from collections import deque

dq = deque([1, 2, 3])

# 两端操作都是 O(1)
dq.append(4)       # 右端添加
dq.appendleft(0)   # 左端添加 ← 列表做不到！
dq.pop()           # 右端弹出
dq.popleft()       # 左端弹出 ← 列表做不到！

print(dq)  # deque([1, 2, 3, 4])
```

---

## 11. 小结

### 必须掌握

1. **索引从 0 开始**：第一个元素是 `lst[0]`，最后一个是 `lst[-1]`
2. **切片是副本**：`lst[:]` 返回新列表，不影响原列表
3. **append vs extend**：`append` 加一个元素，`extend` 合并列表
4. **浅拷贝的坑**：`.copy()`、`list()`、`[:]` 都是浅拷贝，内层对象共享
5. **性能注意**：末尾操作 O(1)，头部操作 O(n)

### 常见错误

```python
# 错误1：混淆 append 和 extend
lst = [1, 2]
lst.append([3, 4])   # [1, 2, [3, 4]] ← 不是你想要的！
lst.extend([3, 4])    # [1, 2, 3, 4] ← 正确

# 错误2：以为 copy() 是深拷贝
a = [[1, 2], [3, 4]]
b = a.copy()
b[0].append(99)   # a 也变了！← 需要 deepcopy

# 错误3：在循环中用 remove 遍历删除
lst = [1, 2, 2, 3, 2, 4]
for x in lst:
    if x == 2:
        lst.remove(x)  # 危险！可能跳过元素

# 正确做法：
lst = [x for x in lst if x != 2]  # 列表推导式
```

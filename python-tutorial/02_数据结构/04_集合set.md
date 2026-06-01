# 集合 set

## 本质：哈希表（无值）

set 是**无值的哈希表**，只有 key，没有 value。

- **唯一性**：自动去重
- **无序**：Python 3.7+ 不保证顺序（但实现上是哈希表）
- **可变**：可以添加/删除元素
- **元素必须可哈希**：int, str, tuple 等

```python
s = {1, 2, 3, 3, 3}
print(s)   # {1, 2, 3}  (自动去重)
```

## 创建

```python
# 基本
empty = set()          # 注意：{} 是空字典，不是空集合
s = {1, 2, 3}

# 构造器
set([1, 2, 2, 3])      # {1, 2, 3}
set("abc")              # {'a', 'b', 'c'}
set(range(5))           # {0, 1, 2, 3, 4}

# 集合推导式
{x * 2 for x in range(5)}  # {0, 2, 4, 6, 8}
```

## 常用操作

### 添加/删除

```python
s = {1, 2, 3}

s.add(4)       # {1, 2, 3, 4}  (添加一个)
s.update([5, 6]) # {1, 2, 3, 4, 5, 6} (添加多个)

s.remove(3)     # {1, 2}  (删除，不存在则 KeyError)
s.discard(10)   # {1, 2}  (删除，不存在不报错)
s.pop()         # 随机弹出一个 (set 无序，通常弹出第一个)
s.clear()       # set()
```

### 集合运算

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# 并集
a | b            # {1, 2, 3, 4, 5, 6}
a.union(b)       # 同上

# 交集
a & b            # {3, 4}
a.intersection(b) # 同上

# 差集 (a 有 b 没有)
a - b            # {1, 2}
a.difference(b)  # 同上

# 对称差集 (a b 互没有的)
a ^ b            # {1, 2, 5, 6}
a.symmetric_difference(b) # 同上

# 子集判断
{1, 2} <= {1, 2, 3}   # True (子集)
{1, 2} < {1, 2, 3}   # True (真子集)
{1, 2, 3} >= {1, 2}   # True (超集)

# 不相交
{1, 2}.isdisjoint({3, 4})  # True
{1, 2}.isdisjoint({2, 3})  # False
```

### 成员测试

```python
s = {1, 2, 3}

2 in s           # True (O(1))
10 not in s      # True
```

## 性能特点

| 操作 | 时间复杂度 |
|------|-----------|
| 成员测试 `x in s` | O(1) |
| 添加 `s.add(x)` | O(1) |
| 删除 `s.remove(x)` | O(1) |
| 集合运算 `\| & -` | O(min(len(s), len(t))) |

## 实际应用

### 去重

```python
# 列表去重（保持顺序用 dict 或 pandas）
lst = [1, 2, 2, 3, 1, 4, 3]
unique = list(set(lst))  # [1, 2, 3, 4] (顺序可能不同)
```

### 判断唯一性

```python
# 检查所有字符是否唯一
def all_unique(s):
    return len(s) == len(set(s))

all_unique("abc")   # True
all_unique("aba")   # False
```

### 两点间的共同爱好

```python
user1_likes = {"apple", "banana", "cherry"}
user2_likes = {"banana", "cherry", "date"}

# 共同爱好（交集）
common = user1_likes & user2_likes  # {'banana', 'cherry'}

# 独有爱好（对称差集）
unique_to_one = user1_likes ^ user2_likes
# {'apple', 'date'}
```

### 高效过滤

```python
# 从列表中筛选出在另一个集合中的元素
all_ids = {1, 5, 10, 15}
records = [1, 2, 5, 7, 10, 15, 20]

# 方式1：列表推导
filtered = [r for r in records if r in all_ids]  # [1, 5, 10, 15]

# 方式2：集合运算（更快）
filtered = list(set(records) & all_ids)
```

## frozenset：不可变集合

```python
# set 可变，不能用作 dict key 或 set 元素
# s = {[1, 2]}  # TypeError

# frozenset 不可变，可以哈希
fs = frozenset([1, 2, 3])

# 可以作为 set 的元素
s = {fs, frozenset([4, 5])}
# {{1, 2, 3}, {4, 5}}

# 可以作为 dict key
d = {fs: "集合1"}
```

## set 的复制

```python
original = {1, 2, 3}

copy1 = original.copy()
copy2 = set(original)

# 浅拷贝：内容是共享的（但 set 元素不可变，没问题）
```

## 与 list 的选择

| 场景 | 用 set | 用 list |
|------|--------|---------|
| 需要唯一性 | set 自动去重 | list 可能有重复 |
| 频繁成员测试 | O(1) | O(n) |
| 集合运算 | 原生支持 | 需要手动实现 |
| 保持顺序 | 否 | 是 |
| 可哈希 | 否 | 否 |

## 小结

1. **唯一性**：自动去重，元素不重复
2. **O(1) 查找**：`in` 操作极快
3. **集合运算**：`|` 并集、`&` 交集、`-` 差集、`^` 对称差集
4. **元素必须可哈希**：不能用 list/dict/set 作为元素
5. **frozenset**：不可变版本，可作 dict key / set 元素

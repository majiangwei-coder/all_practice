# 字典 dict

## 本质：哈希表

dict 是**哈希表**实现， key 必须是**可哈希**的类型。

| 可哈希（可用作 key） | 不可哈希 |
|---------------------|----------|
| int, float, str | list |
| tuple (元素也需可哈希) | dict |
| bytes | set |
| None | 自定义对象（除非实现了 `__hash__`） |

```python
# 合法 key
d = {1: "int", "a": "str", (1, 2): "tuple"}

# 非法 key
d = {[1, 2]: "list"}      # TypeError
d = {{}: "dict"}          # TypeError
```

## 创建

```python
# 基本
empty = {}
d = {"a": 1, "b": 2}

# 构造器
dict(a=1, b=2)             # {'a': 1, 'b': 2}
dict([("a", 1), ("b", 2)]) # {'a': 1, 'b': 2}
dict.fromkeys(["a", "b"], 0) # {'a': 0, 'b': 0}

# 字典推导式
{k: v for k, v in [("a", 1), ("b", 2)]}  # {'a': 1, 'b': 2}
{k: len(k) for k in ["apple", "banana"]}  # {'apple': 5, 'banana': 6}
```

## 访问

```python
d = {"a": 1, "b": 2}

# 取值
d["a"]           # 1
d.get("a")       # 1
d.get("c")       # None (不报错)
d.get("c", 0)     # 0 (默认值)

# 赋值/更新
d["a"] = 10      # {'a': 10, 'b': 2}
d["c"] = 3       # 新增键值对

# 删除
del d["a"]       # {'b': 2}
value = d.pop("b") # 2, d={}
```

## 常用方法

```python
d = {"a": 1, "b": 2}

# 查看
"a" in d              # True (检查 key)
d.keys()              # dict_keys(['a', 'b'])
d.values()            # dict_values([1, 2])
d.items()             # dict_items([('a', 1), ('b', 2)])

# 获取并删除
d.popitem()           # ('b', 2), d={'a': 1}  (LIFO)
d.setdefault("a", 0)  # 若存在则返回现有值，否则设置并返回
d.setdefault("c", 3)  # 3, d={'a': 1, 'c': 3}

# 更新合并
d.update({"c": 4})    # {'a': 1, 'c': 4} (覆盖存在的key)

# 清空
d.clear()             # {}
```

## 遍历

```python
d = {"a": 1, "b": 2, "c": 3}

# 遍历 key（最常用）
for key in d:
    print(key)

for key in d.keys():
    print(key)

# 遍历 value
for value in d.values():
    print(value)

# 遍历 key-value
for key, value in d.items():
    print(f"{key}: {value}")
```

## 性能特点

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 访问 `d[key]` | O(1) | 哈希查找 |
| 赋值 `d[key] = val` | O(1) | 哈希查找+插入 |
| 查找 `key in d` | O(1) | 哈希查找 |
| 删除 `del d[key]` | O(1) | 哈希查找+删除 |

**最坏情况 O(n)**：当 key 哈希冲突严重时。

## 哈希冲突与扩容

```python
# Python dict 内部机制：
# 1. 初始容量 8，负载因子 2/3
# 2. 当利用率 > 2/3，扩容 4 倍
# 3. 扩容后重新哈希（rehash）
```

## 字典的"有序性"

**Python 3.7+**：dict 保持**插入顺序**

```python
d = {}
d["z"] = 1
d["a"] = 2
d["m"] = 3
print(list(d.keys()))  # ['z', 'a', 'm'] (保持插入顺序)
```

**但不是排序**，只是按插入顺序。

## defaultdict：默认值字典

```python
from collections import defaultdict

# 普通 dict 访问不存在的 key 会报错
# d["c"]  # KeyError

# defaultdict 自动创建默认值
dd = defaultdict(list)  # 默认值是空列表
dd[" fruits"].append("apple")
dd[" fruits"].append("banana")
# {'fruits': ['apple', 'banana']}

# 统计计数
counter = defaultdict(int)
for word in ["apple", "banana", "apple", "cherry", "banana", "apple"]:
    counter[word] += 1
# {'apple': 3, 'banana': 2, 'cherry': 1}
```

## Counter：计数器

```python
from collections import Counter

# 统计元素出现次数
cnt = Counter(["apple", "banana", "apple", "cherry"])
# Counter({'apple': 2, 'banana': 1, 'cherry': 1})

# most_common
cnt.most_common(2)  # [('apple', 2), ('banana', 1)]

# 更新计数
cnt["apple"] += 1
cnt.update(["apple", "date"])
```

## OrderedDict vs dict

**Python 3.7+**：普通 `dict` 已保证有序，`OrderedDict` 基本没必要了。

```python
from collections import OrderedDict

# 历史遗留：Python 2/3.6 之前的 dict 是无序的
# 现在直接用 dict 即可
```

## 字典的复制

```python
original = {"a": 1, "b": {"x": 10}}

# 浅拷贝
copy1 = original.copy()
copy2 = dict(original)
copy3 = {**original}

# 深拷贝
import copy
deep = copy.deepcopy(original)
```

## 与 list 的选择

| 场景 | 用 dict | 用 list |
|------|---------|---------|
| 通过 key 查找 | O(1) 快速 | O(n) 需遍历 |
| 保持顺序 | Python 3.7+ 自动 | 列表本身有序 |
| 键值映射 | 原生支持 | 需用两个 list |
| 内存 | 更大 | 更小 |

## 小结

1. **key 必须是可哈希的**：不能用 list/dict/set
2. **O(1) 访问**：哈希表实现，key in dict 很快
3. **Python 3.7+ 有序**：按插入顺序，不是排序
4. **get vs []**：`get` 不存在的 key 返回 None（可选默认值），`[]` 抛 KeyError
5. **defaultdict**：访问不存在的 key 自动创建默认值

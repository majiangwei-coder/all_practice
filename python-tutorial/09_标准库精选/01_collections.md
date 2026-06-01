# collections 容器数据类型

## 概览

collections 模块提供专门的容器数据类型，是对内置类型的补充。

## deque：双端队列

```python
from collections import deque

dq = deque([1, 2, 3, 4, 5])

# 两端操作 O(1)
dq.append(6)       # 右端添加
dq.appendleft(0)    # 左端添加
dq.pop()           # 右端弹出
dq.popleft()       # 左端弹出

print(dq)  # deque([1, 2, 3, 4, 5])
```

### 常用用法

```python
# 1. 队列（先进先出）
queue = deque()
queue.append("task1")
queue.append("task2")
queue.appendleft("urgent")  # 优先任务
while queue:
    task = queue.popleft()
    print(f"执行: {task}")

# 2. 固定长度 deque（自动丢弃旧元素）
recent = deque(maxlen=5)
for i in range(10):
    recent.append(i)
print(recent)  # deque([5, 6, 7, 8, 9])

# 3. 最近访问历史
history = deque(maxlen=100)
```

### rotate

```python
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)   # 向右旋转 2 位
print(dq)      # deque([4, 5, 1, 2, 3])

dq.rotate(-2)  # 向左旋转 2 位
print(dq)      # deque([1, 2, 3, 4, 5])
```

## defaultdict：默认值字典

```python
from collections import defaultdict

# 访问不存在的 key 自动创建默认值
dd = defaultdict(int)  # 默认值 0
dd["a"] += 1
print(dd)  # {'a': 1}

dd2 = defaultdict(list)  # 默认值空列表
dd2["fruits"].append("apple")
print(dd2)  # {'fruits': ['apple']}

# 常用场景：分组
words = ["apple", "banana", "apricot", "blueberry"]
by_first = defaultdict(list)
for word in words:
    by_first[word[0]].append(word)
print(by_first)  # {'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry']}
```

## Counter：计数器

```python
from collections import Counter

# 创建
cnt = Counter("abracadabra")
print(cnt)  # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# from iterable
cnt = Counter([1, 2, 2, 3, 3, 3])
print(cnt)  # Counter({3: 3, 2: 2, 1: 1})
```

### 常用方法

```python
cnt = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])

cnt.most_common(2)     # [('blue', 3), ('red', 2)] - 最常见的 2 个
cnt.most_common()      # 所有，按出现次数排序

list(cnt.elements())   # ['red', 'red', 'blue', 'blue', 'blue', 'green']

cnt.total()            # 6 - 总数 (Python 3.10+)

cnt.subtract(['red', 'blue'])  # 减去计数
```

### 更新计数

```python
cnt = Counter(a=3, b=1)
cnt.update(['a', 'b', 'c'])
print(cnt)  # Counter({'a': 4, 'b': 2, 'c': 1})

cnt['a'] += 1  # 直接增加
```

## OrderedDict：有序字典

```python
from collections import OrderedDict

# Python 3.7+ 普通 dict 已保证顺序
# OrderedDict 在早期版本有用，或需要特定顺序保证时

od = OrderedDict()
od['z'] = 1
od['a'] = 2
od['m'] = 3
print(list(od.keys()))  # ['z', 'a', 'm']

# move_to_end：移动到末尾
od.move_to_end('z')
print(list(od.keys()))  # ['a', 'm', 'z']

# popitem(last=False) 从开头弹出
od.popitem(last=False)  # ('a', 2)
```

## namedtuple：命名元组

```python
from collections import namedtuple

# 定义
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 5)

# 访问
print(p.x, p.y)       # 3, 5
print(p[0], p[1])     # 3, 5（可用索引）
```

### 常用方法

```python
p = Point(x=3, y=5)

p._asdict()           # {'x': 3, 'y': 5}
p._fields             # ('x', 'y')
p._replace(x=10)      # Point(x=10, y=5) - 创建新实例

# 从序列创建
p2 = Point._make([7, 9])  # Point(x=7, y=9)
```

### 继承问题

namedtuple 不支持直接继承实例属性：

```python
# 解决方案：用 dataclass 或 typing.NamedTuple
```

## ChainMap：链接字典

```python
from collections import ChainMap

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 100, 'c': 3}

cm = ChainMap(dict1, dict2)
print(cm['a'])  # 1 (第一个字典)
print(cm['b'])  # 2 (第一个字典优先)
print(cm['c'])  # 3

# 查找是按顺序搜索
print(list(cm.keys()))  # ['a', 'b', 'c']
```

### 用途：模拟作用域

```python
local_vars = {'x': 1, 'y': 2}
global_vars = {'x': 10, 'z': 3}
scope = ChainMap(local_vars, global_vars)

print(scope['x'])  # 1 (local 优先)
print(scope['z'])  # 3
```

## UserDict / UserList / UserString

面向对象的包装器，可以继承并扩展：

```python
from collections import UserDict

class MyDict(UserDict):
    def __setitem__(self, key, value):
        if not isinstance(value, str):
            raise TypeError("值必须是字符串")
        super().__setitem__(key, value)

d = MyDict()
d['name'] = 'Alice'  # OK
# d['age'] = 30      # TypeError
```

## 小结

| 类型 | 用途 |
|------|------|
| `deque` | 双端队列，头尾高效操作 |
| `defaultdict` | 自动创建默认值的字典 |
| `Counter` | 元素计数统计 |
| `OrderedDict` | 保证顺序的字典（Python 3.7+ 普通 dict 已保证） |
| `namedtuple` | 带字段名的轻量元组 |
| `ChainMap` | 多个字典的逻辑组合 |
| `UserDict/List/String` | 可继承扩展的包装器 |

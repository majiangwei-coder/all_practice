# 序列化和数据转换

## 序列化概述

序列化：将对象转换为可存储/传输的格式
反序列化：从格式恢复对象

| 方式 | 用途 | 特点 |
|------|------|------|
| pickle | Python 对象 | Python 专用，可序列化任意对象 |
| json | JSON 格式 | 跨语言，结构简单 |
| csv | 表格数据 | 轻量，Excel 兼容 |
| marshal | Python internal | 用于 .pyc 文件，内部使用 |

## pickle

### 序列化（dump/dumps）

```python
import pickle

data = {"name": "Alice", "scores": [95, 88, 76], "active": True}

# 序列化为 bytes
bytes_data = pickle.dumps(data)
print(type(bytes_data))  # <class 'bytes'>

# 序列化到文件
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)
```

### 反序列化（load/loads）

```python
# 从 bytes 恢复
restored = pickle.loads(bytes_data)

# 从文件恢复
with open("data.pkl", "rb") as f:
    restored = pickle.load(f)
```

### pickle 协议

```python
# 不同协议
pickle.dumps(data, protocol=0)  # 文本格式，兼容性好
pickle.dumps(data, protocol=1)  # 旧二进制格式
pickle.dumps(data, protocol=2)  # Python 2.3+ 默认
pickle.dumps(data, protocol=3)  # Python 3.0+（默认）
pickle.dumps(data, protocol=4)  # Python 3.4+（更高效）
pickle.dumps(data, protocol=5)  # Python 3.8+（带外缓冲区）

# 高效：指定最高协议
pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
```

### pickle 注意事项

```python
# 1. 不安全！不要反序列化不可信的数据
# pickle.loads(untrusted_data)  # 可能执行任意代码

# 2. 不能序列化 lambda、生成器等某些类型
# 3. 类对象序列化后，反序列化时类定义必须存在
```

### 应用场景

```python
# 缓存复杂对象
import pickle
import diskcache

cache = diskcache.Cache("./cache")
cache.set("key", complex_object)
restored = cache.get("key")

# 深拷贝
copied = pickle.loads(pickle.dumps(original))
```

## JSON

### 基本使用

```python
import json

# Python 对象 → JSON 字符串
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data)
print(json_str)  # '{"name": "Alice", "age": 30}'

# JSON 字符串 → Python 对象
parsed = json.loads(json_str)

# 格式化（人类可读）
json_str = json.dumps(data, indent=2, sort_keys=True)
```

### 格式化输出

```python
data = {
    "name": "Alice",
    "skills": ["Python", "JavaScript"],
    "address": {"city": "NYC", "zip": "10001"}
}

# 缩进
print(json.dumps(data, indent=2))
# {
#   "name": "Alice",
#   "skills": ["Python", "JavaScript"],
#   "address": {"city": "NYC", "zip": "10001"}
# }

# 按 key 排序
print(json.dumps(data, indent=2, sort_keys=True))
```

### JSON 文件操作

```python
# 写入
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 自定义序列化

```python
from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {"event": "conference", "date": datetime.now()}
json_str = json.dumps(data, cls=DateTimeEncoder)
```

### 反序列化自定义

```python
from datetime import datetime
import json

def datetime_parser(dct):
    for key, value in dct.items():
        if key == "date":
            dct[key] = datetime.fromisoformat(value)
    return dct

parsed = json.loads(json_str, object_hook=datetime_parser)
```

### JSON vs pickle

| 特性 | JSON | pickle |
|------|------|--------|
| 跨语言 | 是 | 否 |
| 安全性 | 安全 | 不安全 |
| 数据类型 | 基础类型 | 任意 Python 对象 |
| 文件扩展名 | .json | .pkl/.pickle |
| 可读性 | 人类可读 | 二进制 |

## CSV

见文件与 IO 章节。

## 其他序列化格式

### msgpack

```python
import msgpack

# 更紧凑的二进制格式
packed = msgpack.packb({"key": "value"})
unpacked = msgpack.unpackb(packed, raw=False)
```

### shelve

类似持久化字典：

```python
import shelve

# 打开数据库（文件式存储）
with shelve.open("mydata") as db:
    db["user"] = {"name": "Alice", "age": 30}
    db["config"] = [1, 2, 3]

# 读取
with shelve.open("mydata") as db:
    print(db["user"])
```

## 数据类 dataclass (Python 3.7+)

方便的类定义，自动生成方法：

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Person:
    name: str
    age: int
    scores: List[int] = field(default_factory=list)

    def average_score(self) -> float:
        return sum(self.scores) / len(self.scores)

p = Person("Alice", 30, [95, 88, 76])
print(p)
# Person(name='Alice', age=30, scores=[95, 88, 76])
print(p.average_score())  # 86.33
```

### dataclass 选项

```python
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Card:
    rank: int
    suit: str

    def __post_init__(self):
        if not (1 <= self.rank <= 13):
            raise ValueError("Invalid rank")

# order=True: 生成 __lt__ 等比较方法
# frozen=True: 实例不可变
# __post_init__: 初始化后验证
```

## 小结

1. **pickle**：Python 对象序列化，二进制，不安全但功能强大
2. **json**：跨语言数据交换，文本格式，安全
3. **dataclass**：便捷的类定义，减少样板代码
4. **shelve**：持久化字典，简易键值存储
5. **不要反序列化不可信数据**：pickle 有安全风险

# Python 禅与编码规范

## PEP 8 编码规范

PEP 8 是 Python 的官方编码风格指南。

### 代码布局

```python
# 缩进：4 空格（不用 Tab）
def func():
    if True:
        pass

# 行长度：不超过 79 字符
# 长行可使用反斜杠换行
long_line = "这是很长的行" + \
            "需要分成多行"

# 空行：函数间 2 空行，类间 1 空行
class MyClass:
    pass


def func1():
    pass


def func2():
    pass
```

### 导入

```python
# 标准库 → 第三方 → 本地
import os
import sys

import第三方

from mymodule import MyClass
from mypackage import something

# 按字母排序
import collections
import os
import sys
```

### 命名约定

```python
# 变量/函数：snake_case
user_name = "Alice"
def get_user():
    pass

# 类：CapWords
class UserProfile:
    pass

# 常量：UPPER_SNAKE_CASE
MAX_SIZE = 100
PI = 3.14159

# 私有属性：_leading_underscore
def _private_func():
    pass

class MyClass:
    def __init__(self):
        self._private = 1
```

### 注释

```python
# 单行注释
x = x + 1  # 补偿边界

# 文档字符串
def func(arg):
    """
    函数的简要说明。

    更详细的说明（如果需要）。

    Args:
        arg: 参数说明

    Returns:
        返回值说明

    Raises:
        ValueError: 什么时候抛出
    """
    pass
```

### 其他规则

```python
# 等号周围空格
x = 1          # 赋值
y = x + 1     # 表达式（两侧空格）
y = x * 2     # 操作符两侧空格

# 关键字参数周围无空格
func(a=1, b=2)

# 函数调用括号内无空格
func(a, b, c)

# 不要使用：
# x=1         # 不要紧贴
# func( a )   # 括号内不要空格
```

## Python 之禅 (The Zen of Python)

```python
import this
```

```
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the tempting temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

## 核心原则

### 1. 简洁优于复杂

```python
# 不好：过度设计
class Car:
    def __init__(self):
        self wheels = []
        for i in range(4):
            self.wheels.append(Wheel())

# 好：直接
wheels = [Wheel() for _ in range(4)]
```

### 2. 显式优于隐式

```python
# 不好：隐式返回
def process():
    result = do_something()
    # 忘记返回值

# 好：显式
def process():
    return do_something()
```

### 3. EAFP vs LBYL

Python 风格是 EAFP (Easier to Ask Forgiveness than Permission)：

```python
# LBYL (Look Before You Leap) - 先检查
if key in my_dict:
    value = my_dict[key]
else:
    value = None

# EAFP (Easier to Ask Forgiveness than Permission) - 先尝试
try:
    value = my_dict[key]
except KeyError:
    value = None

# 对于可哈希的键，get 更好
value = my_dict.get(key, None)
```

### 4. 不要使用裸 except

```python
# 不好：捕获所有异常
try:
    do_something()
except:
    pass

# 好：指定具体异常
try:
    do_something()
except ValueError:
    pass
except (TypeError, KeyError):
    pass
except Exception as e:
    raise  # 重新抛出其他异常
```

## 常见反模式

### 1. 避免 from module import *

```python
# 不好
from os import *

# 好
import os
from os import path
```

### 2. 避免 eval

```python
# 不好：有安全风险
code = "2 + 3"
result = eval(code)  # 危险！

# 好：使用 ast.literal_eval 安全解析
import ast
result = ast.literal_eval("2 + 3")
```

### 3. 避免 mutable 默认参数

```python
# 不好
def func(items=[]):  # 危险！
    items.append(1)
    return items

# 好
def func(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

### 4. 避免全局变量

```python
# 不好
total = 0
def add(n):
    global total  # 难以追踪
    total += n

# 好
def add(n, total=0):
    return total + n
```

### 5. 避免长参数列表

```python
# 不好
def create_user(first_name, last_name, email, phone, address, city, state, zip_code):
    pass

# 好：使用 dataclass 或字典
from dataclasses import dataclass

@dataclass
class Address:
    city: str
    state: str
    zip_code: str

@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Address
```

## 工具

### Black - 代码格式化

```bash
pip install black
black mycode.py
```

### flake8 - 代码检查

```bash
pip install flake8
flake8 mycode.py
```

### mypy - 类型检查

```bash
pip install mypy
mypy mycode.py
```

### isort - import 排序

```bash
pip install isort
isort mycode.py
```

## 小结

1. **遵循 PEP 8**：代码风格统一
2. **Python 之禅**：简洁、显式、优美
3. **EAFP 风格**：先尝试再捕获
4. **避免反模式**：mutable 默认参数、裸 except、eval
5. **使用工具**：black/flake8/mypy 提升代码质量
6. **写好注释和文档**：代码即文档

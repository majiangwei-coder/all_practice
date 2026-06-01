# 字符串 str

## 不可变序列

str 是**不可变的 Unicode 字符序列**，一旦创建不能修改。

```python
s = "hello"
s[0] = "H"   # TypeError: 'str' object does not support item assignment

# 正确做法：创建新字符串
s = "H" + s[1:]  # "Hello"
```

## 创建

```python
# 基本
s1 = "hello"
s2 = 'world'
s3 = """多行
字符串"""

# 转义
s4 = "line1\nline2"
s5 = r"raw\nstring"  # 不转义

# 构造器
str(42)           # "42"
str(b"abc")       # "b'abc'" (bytes 转 str 不是解码)
str([], 'utf-8')  # ""
```

## 索引与切片

```python
s = "Hello"

# 索引 (O(1))
s[0]    # 'H'
s[-1]   # 'o'

# 切片 (返回新字符串)
s[1:4]    # 'ell'
s[::2]    # 'Hlo' (步长2)
s[::-1]   # 'olleH' (反转)
```

## 常用方法

### 大小写

```python
"hello".upper()      # 'HELLO'
"HELLO".lower()      # 'hello'
"hello".capitalize() # 'Hello' (首字母大写)
"hello world".title() # 'Hello World' (每个词首字母大写)
"HELLO".swapcase()   # 'hello'
```

### 查找与替换

```python
s = "hello world"

s.find("lo")       # 3 (子串位置，找不到返回 -1)
s.rfind("o")       # 7 (从右边找)
s.index("lo")      # 3 (同 find，但找不到抛 ValueError)
s.count("l")       # 3 (出现次数)

s.replace("world", "python")  # 'hello python'
s.replace("l", "L", 1)       # 'heLlo world' (替换1次)
```

### 分割与连接

```python
# 分割
"a,b,c".split(",")      # ['a', 'b', 'c']
"a\nb\nc".splitlines()  # ['a', 'b', 'c']
"hello".split()         # ['hello'] (默认空格)
"  hello  ".strip()    # 'hello' (去首尾空格)

# rsplit 从右边分割
"a:b:c".rsplit(":", 1)  # ['a:b', 'c']

# 连接
",".join(["a", "b", "c"])  # 'a,b,c'
" ".join(["hello", "world"]) # 'hello world'
```

### 判断

```python
s = "Hello123"

s.startswith("Hel")    # True
s.endswith("23")        # True
s.isalpha()             # False (含数字)
s.isdigit()             # False
s.isalnum()             # True (字母或数字)
s.isupper()             # False
s.islower()             # False
s.isspace()             # False
s.isnumeric()           # False
```

### 格式化

```python
# format 方法
"hello {}".format("world")         # 'hello world'
"{} {}".format("a", "b")           # 'a b'
"{1} {0}".format("x", "y")         # 'y x' (位置参数)
"{name}".format(name="Alice")      # 'Alice' (关键字参数)

# f-string (Python 3.6+)
name = "Bob"
f"Hello {name}"                    # 'Hello Bob'
f"{2 ** 3}"                        # '8' (表达式)
f"{name.upper()}"                  # 'BOB' (方法调用)
```

### 编码转换

```python
# str → bytes
"hello".encode("utf-8")   # b'hello'
"你好".encode("utf-8")    # b'\xe4\xb8\xad\xe5\x9b\xbd'

# bytes → str
b'hello'.decode("utf-8")  # 'hello'
```

## 字符串拼接性能

```python
# 多次拼接：不要用 +
result = ""
for i in range(1000):
    result += str(i)    # O(n²) 每次创建新字符串

# 正确方式：join
parts = []
for i in range(1000):
    parts.append(str(i))
result = "".join(parts)  # O(n)

# 或列表推导
result = "".join(str(i) for i in range(1000))
```

**原因**：`+` 每次都创建新字符串并复制，join 一次性分配。

## 字符串驻留 (Interning)

```python
# 短字符串（通常 < 20 字符）会被驻留
a = "hello"
b = "hello"
print(a is b)   # True (同一个对象)

# 长字符串不驻留
a = "a" * 100
b = "a" * 100
print(a is b)   # 可能 False

# 编译时常量会被驻留
s = "hi"
```

**不要依赖此行为**做逻辑判断，用 `==` 比较值。

## 原始字符串

```python
# Windows 路径问题
path = "C:\new\folder"   # \n 会被解释为换行！

# 解决方案
path = r"C:\new\folder"  # 原始字符串，不转义
path = "C:\\new\\folder" # 双反斜杠转义
```

## 字符串是不可变的

```python
s = "hello"
id(s)                 # 某个地址
s = s + " world"      # 创建新字符串
id(s)                 # 新地址（变了）
```

这意味着：
- **安全**：字符串不会被意外修改
- **性能**：相同内容的字符串共享内存

## 正则表达式支持

```python
import re

s = "price: $99.99"

# re.search 查找第一个匹配
match = re.search(r'\d+\.\d+', s)
if match:
    print(match.group())   # '99.99'

# re.findall 找所有匹配
re.findall(r'\d+', s)      # ['99', '99']

# re.sub 替换
re.sub(r'\d+', '0', s)     # 'price: $0.0'
```

## bytes vs str

```python
# str: Unicode 字符
# bytes: 原始字节

# 编码：str → bytes
s = "你好"
b = s.encode("utf-8")  # b'\xe4\xb8\xad\xe5\x9b\xbd'

# 解码：bytes → str
b.decode("utf-8")      # '你好'

# 长度不同
len("你好")   # 2 (字符数)
len(b)        # 6 (字节数)
```

## 小结

1. **不可变**：字符串创建后不能修改
2. **索引切片**：`s[0]`、`s[1:3]`，返回新字符串
3. **常用方法**：split/join/find/replace/strip/format/f-string
4. **拼接用 join**：`+` 多次拼接 O(n²)，join O(n)
5. **bytes vs str**：str 是 Unicode，bytes 是字节，需要编解码转换

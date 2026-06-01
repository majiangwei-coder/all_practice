# lambda 与闭包

## lambda 匿名函数

```python
# 基本语法
lambda 参数: 表达式

# 示例
square = lambda x: x ** 2
square(5)   # 25

add = lambda a, b: a + b
add(1, 2)   # 3
```

**限制**：lambda 只能是**单个表达式**，不能包含语句（if/for/while 等）。

## lambda vs def

```python
# 等价写法

# def
def square(x):
    return x ** 2

# lambda
square = lambda x: x ** 2
```

### 何时用 lambda

```python
# 1. 短的、一次性的函数
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort(key=lambda x: -x)   # 降序排列

# 2. 高阶函数的参数
list(map(lambda x: x * 2, [1, 2, 3]))        # [2, 4, 6]
list(filter(lambda x: x > 2, [1, 2, 3, 4]))   # [3, 4]
list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, [1,2,3,4])))
# [4, 16]

# 3. 返回简单函数
def make_power(exp):
    return lambda base: base ** exp

square = make_power(2)
cube = make_power(3)
square(5)   # 25
cube(5)     # 125
```

## 闭包 (Closure)

**闭包**：一个函数记住它创建时所在作用域的变量。

```python
def outer():
    x = 10

    def inner():
        print(x)   # 引用外层 x

    return inner

func = outer()
func()   # 10 (即使 outer 已经返回)
```

### 闭包是如何工作的

```python
# Python 的函数对象包含 __closure__ 属性
def outer():
    x = 10

    def inner():
        print(x)

    return inner

func = outer()
print(func.__closure__)    # (<cell at ...: int object at ...>,)
print(func.__closure__[0].cell_contents)  # 10
```

### 闭包的经典用法：计数器

```python
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

counter = make_counter()
counter()   # 1
counter()   # 2
counter()   # 3
```

### 闭包的坑

```python
# 错误：闭包捕获的是变量，不是值
def create_funcs():
    funcs = []
    for i in range(3):
        funcs.append(lambda: i)  # 所有 lambda 都引用同一个 i
    return funcs

f0, f1, f2 = create_funcs()
print(f0())   # 2 (预期 0)
print(f1())   # 2 (预期 1)
print(f2())   # 2

# 修复：立即绑定当前值
def create_funcs():
    funcs = []
    for i in range(3):
        funcs.append(lambda i=i: i)  # 默认参数立即绑定
    return funcs

f0, f1, f2 = create_funcs()
print(f0())   # 0
print(f1())   # 1
print(f2())   # 2
```

## nonlocal 声明

```python
def outer():
    x = 10

    def inner():
        nonlocal x   # 声明使用外层的 x
        x = 20       # 修改外层 x

    inner()
    print(x)         # 20

outer()
```

### global vs nonlocal

| 声明 | 作用范围 |
|------|----------|
| `global x` | 声明使用全局变量 x |
| `nonlocal x` | 声明使用**最近外层函数**的变量 x |

```python
x = "global"

def outer():
    x = "outer"

    def inner():
        global x      # 修改全局 x
        x = "modified global"

    def inner2():
        nonlocal x    # 修改 outer 的 x
        x = "modified outer"

    inner()
    inner2()
    print(x)          # "modified outer"

outer()
print(x)              # "modified global"
```

## lambda 与闭包结合

```python
# 创建多个函数，每个记住不同的参数
def make_multiplier(factor):
    return lambda x: x * factor

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))   # 10
print(triple(5))   # 15

# 闭包记忆外层参数
def make_power(exp):
    return lambda base: base ** exp
```

## LEGB 法则回顾

```python
x = "global"

def outer():
    x = "outer"

    def inner():
        x = "inner"          # Local
        print(x)

    def inner_no_local():
        print(x)             # Enclosed (outer)

    def builtin_lookalike():
        print(x)            # Global

    inner()          # "inner"
    inner_no_local() # "outer"
    builtin_lookalike() # "global"

outer()
```

## 小结

1. **lambda**：单表达式匿名函数，适合简短一次性的函数
2. **闭包**：函数记住创建时的外部变量
3. **闭包陷阱**：循环中创建 lambda 时，用默认参数 `lambda i=i: i` 绑定当前值
4. **nonlocal**：修改外层函数的变量（非全局）
5. **闭包用途**：工厂函数、计数器、回调函数等

## 实战练习

### 练习1：用闭包实现缓存

```python
def memoize():
    """创建一个带缓存的函数"""
    cache = {}

    def wrapper(n):
        if n not in cache:
            # 模拟耗时计算
            cache[n] = n ** 2
            print(f"计算 {n} -> {cache[n]}")
        else:
            print(f"从缓存取 {n} -> {cache[n]}")
        return cache[n]

    return wrapper

calc = memoize()
calc(5)  # 计算 5 -> 25
calc(5)  # 从缓存取 5 -> 25
calc(10) # 计算 10 -> 100
```

### 练习2：用闭包实现简单的验证器

```python
def create_validator(min_val, max_val):
    """创建一个范围验证器"""
    def validator(value):
        if not (min_val <= value <= max_val):
            raise ValueError(f"值 {value} 不在范围 [{min_val}, {max_val}]")
        return value
    return validator

age_validator = create_validator(0, 150)
score_validator = create_validator(0, 100)

age_validator(30)    # OK
# score_validator(150)  # ValueError!
```

### 练习3：理解闭包的 `__closure__`

```python
def outer(x, y):
    def inner():
        return x + y
    return inner

f = outer(10, 20)
# f 的 __closure__ 存储了 x=10, y=20
print(f.__closure__)  # (<cell ...: int object>, <cell ...: int object>)
print(f.__closure__[0].cell_contents)  # 10
print(f.__closure__[1].cell_contents)  # 20
print(f())  # 30

# 注意：只有被 inner 引用的外部变量才会进 __closure__
def outer2(x, y):
    def inner():
        return x  # 只用了 x
    return inner

f2 = outer2(1, 2)
print(len(f2.__closure__))  # 1（只有 x，y 被丢弃了）
```

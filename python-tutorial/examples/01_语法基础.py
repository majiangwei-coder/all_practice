"""
第一章：语法基础 示例代码
配合 01_语法基础/ 目录下的 Markdown 文档学习
"""

# ====================
# 01 变量与数据类型
# ====================

print("=" * 50)
print("01 变量与数据类型")
print("=" * 50)

# 一切皆对象
a = 42
print(f"id: {id(a)}, type: {type(a)}, value: {a}")

# 变量是引用
a = [1, 2, 3]
b = a
b.append(4)
print(f"a={a}, b={b}")  # a 和 b 指向同一个对象

# is vs ==
a = [1, 2, 3]
b = [1, 2, 3]
print(f"a == b: {a == b}")  # True，值相同
print(f"a is b: {a is b}")  # False，不是同一个对象

# 整数缓存
a = 256
b = 256
print(f"256 is 256: {a is b}")  # True（小整数缓存）
a = 257
b = 257
print(f"257 is 257: {a is b}")  # False（超过缓存范围）

# None 是单例
a = None
b = None
print(f"None is None: {a is b}")  # True

# 类型转换
print(f"int('42') = {int('42')}")
print(f"float('3.14') = {float('3.14')}")
print(f"str(42) = {str(42)}")
print(f"bool(0) = {bool(0)}, bool(1) = {bool(1)}")
print(f"bool('') = {bool('')}, bool(' ') = {bool(' ')}")
print(f"bool([]) = {bool([])}, bool([1]) = {bool([1])}")


# ====================
# 02 运算符与表达式
# ====================

print("\n" + "=" * 50)
print("02 运算符与表达式")
print("=" * 50)

# 整除的坑
print(f"-3 // 2 = {-3 // 2}")  # -2 (向下取整)
print(f"3 // -2 = {3 // -2}")
print(f"-3 % 2 = {-3 % 2}")    # 1 (与除数同号)

# 链式比较
x = 5
print(f"1 < x < 10: {1 < x < 10}")

# 短路求值
print(f"0 and 2 = {0 and 2}")   # 0
print(f"1 and 2 = {1 and 2}")   # 2
print(f"0 or 2 = {0 or 2}")    # 2
print(f"1 or 2 = {1 or 2}")    # 1

# 位运算判断奇偶
n = 5
print(f"{n} 是奇数: {bool(n & 1)}")
n = 4
print(f"{n} 是偶数: {bool(n & 1 == 0)}")

# 三元表达式
age = 20
status = "成年" if age >= 18 else "未成年"
print(f"age={age}: {status}")


# ====================
# 03 控制流
# ====================

print("\n" + "=" * 50)
print("03 控制流")
print("=" * 50)

# if 语句
x = 10
if x > 0:
    print("正数")
elif x < 0:
    print("负数")
else:
    print("零")

# for 循环
for i in range(5):
    if i == 2:
        continue  # 跳过 2
    if i == 4:
        break  # 提前结束
    print(i, end=" ")
print()  # 换行

# while + else（else 在循环正常结束时执行）
i = 1
while i < 3:
    print(i)
    i += 1
else:
    print("while 正常结束")

# 列表推导式
squares = [x**2 for x in range(5)]
print(f"[x**2 for x in range(5)] = {squares}")

evens = [x for x in range(10) if x % 2 == 0]
print(f"偶数: {evens}")

# 字典推导式
d = {x: x**2 for x in range(3)}
print(f"字典推导式: {d}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

"""
第二章：数据结构 示例代码
配合 02_数据结构/ 目录下的 Markdown 文档学习
"""

# ====================
# 01 列表 list
# ====================

print("=" * 50)
print("01 列表 list")
print("=" * 50)

lst = [1, 2, 3, 4, 5]

# 索引与切片
print(f"lst[0] = {lst[0]}")
print(f"lst[-1] = {lst[-1]}")
print(f"lst[1:4] = {lst[1:4]}")
print(f"lst[::2] = {lst[::2]}")
print(f"lst[::-1] = {lst[::-1]}")  # 反转

# 切片是副本
original = [1, 2, 3]
copied = original[:]
copied.append(4)
print(f"original={original}, copied={copied}")

# 添加元素
lst = [1, 2]
lst.append(3)       # 末尾追加
lst.insert(1, 9)    # 指定位置插入
lst.extend([4, 5])  # 合并
print(f"after append/insert/extend: {lst}")

# 删除元素
lst = [1, 2, 3, 2]
lst.remove(2)       # 删除第一个匹配的
print(f"after remove(2): {lst}")
print(f"pop(): {lst.pop()}")
print(f"after pop(): {lst}")

# 栈与队列
stack = []
stack.append(1)
stack.append(2)
print(f"栈 pop: {stack.pop()}")  # LIFO

# 高效队列
from collections import deque
dq = deque()
dq.append(1)
dq.append(2)
print(f"队列 popleft: {dq.popleft()}")  # FIFO

# 复制的坑
a = [[1, 2], [3, 4]]
b = a.copy()        # 浅拷贝，内层列表共享
c = a[:]            # 同上
import copy
d = copy.deepcopy(a)  # 深拷贝，完全独立
print(f"a={a}, b={b}")


# ====================
# 02 元组 tuple
# ====================

print("\n" + "=" * 50)
print("02 元组 tuple")
print("=" * 50)

# 创建
t = (1, 2, 3)
single = (42,)  # 单元素元组，逗号必须有
print(f"t={t}, single={single}")

# 解包
a, b, c = (1, 2, 3)
print(f"a={a}, b={b}, c={c}")

# * 收集
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

# tuple 不可变，但内部可变元素可修改
t = ([1, 2], [3, 4])
t[0].append(99)
print(f"修改可变元素: {t}")

# namedtuple
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 5)
print(f"Point: {p}, p.x={p.x}, p[0]={p[0]}")


# ====================
# 03 字典 dict
# ====================

print("\n" + "=" * 50)
print("03 字典 dict")
print("=" * 50)

d = {"a": 1, "b": 2}

# 访问
print(f"d['a'] = {d['a']}")
print(f"d.get('c') = {d.get('c')}")
print(f"d.get('c', 0) = {d.get('c', 0)}")

# 遍历
for key, value in d.items():
    print(f"{key}: {value}")

# defaultdict
from collections import defaultdict
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
print(f"defaultdict: {dd}")

# Counter
from collections import Counter
cnt = Counter(["apple", "banana", "apple", "cherry"])
print(f"Counter: {cnt}")
print(f"most_common(2): {cnt.most_common(2)}")


# ====================
# 04 集合 set
# ====================

print("\n" + "=" * 50)
print("04 集合 set")
print("=" * 50)

s = {1, 2, 3, 3, 3}
print(f"自动去重: {s}")

# 集合运算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"a | b (并集): {a | b}")
print(f"a & b (交集): {a & b}")
print(f"a - b (差集): {a - b}")
print(f"a ^ b (对称差集): {a ^ b}")

# 判断子集
print(f"{{1,2}} <= {{1,2,3}}: {{1,2}} <= {{1,2,3}}")

# 去重
lst = [1, 2, 2, 3, 1, 4, 3]
print(f"去重: {list(set(lst))}")

# frozenset
fs = frozenset([1, 2, 3])
s = {fs}  # 可以作为 set 元素
print(f"frozenset 作为 set 元素: {s}")


# ====================
# 05 字符串 str
# ====================

print("\n" + "=" * 50)
print("05 字符串 str")
print("=" * 50)

s = "Hello, World!"

# 索引切片
print(f"s[0]={s[0]}, s[-1]={s[-1]}")
print(f"s[7:12]={s[7:12]}")
print(f"s[::-1]={s[::-1]}")

# 常用方法
print(f"upper(): {s.upper()}")
print(f"lower(): {s.lower()}")
print(f"split(','): {s.split(',')}")
print(f"replace('World', 'Python'): {s.replace('World', 'Python')}")

# f-string
name = "Alice"
age = 30
print(f"f-string: {name} is {age} years old")
print(f"表达式: {2 ** 3}")

# 拼接性能
parts = ["a"] * 1000
result = "".join(parts)  # 正确方式
# 不推荐：result = ""
# for p in parts:
#     result += p  # O(n²)

# 编码
s = "你好"
b = s.encode("utf-8")
print(f"encode: {b}")
print(f"decode: {b.decode('utf-8')}")
print(f"len('你好')={len('你好')}, len(b)={len(b)}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

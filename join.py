print("|".join("杨家有女初长成"))      # 杨|家|有|女|初|长|成

print("|".join("杨家有女初长成").split("|"))   # ['杨', '家', '有', '女', '初', '长', '成']

print("杨家有女初长成杨家有女初长成杨家有女初长成".count("女"))  # 3

a = [3.14, 6.28, 9.42]
b = [1, 2, 3]

print(list(map(lambda x, y: x + y, a, b)))
for item in enumerate(a):
    print(item)

# 列表是可迭代对象，但不是迭代器
my_list = [1, 2, 3]

# 通过 iter() 函数获取迭代器
my_iter = iter(my_list)

print(next(my_iter))  # 输出: 1
print(next(my_iter))  # 输出: 2
print(next(my_iter))  # 输出: 3
# print(next(my_iter))  # 抛出 StopIteration 异常

# 类似列表推导式，但使用圆括号
gen_exp = (x**2 for x in range(5))
print((next(gen_exp)))
print((next(gen_exp)))
print((next(gen_exp)))
print((next(gen_exp)))
print((next(gen_exp)))



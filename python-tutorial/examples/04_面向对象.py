"""
第四章：面向对象 示例代码
配合 04_面向对象/ 目录下的 Markdown 文档学习
"""

# ====================
# 01 类与实例
# ====================

print("=" * 50)
print("01 类与实例")
print("=" * 50)

class Dog:
    species = "Canis familiaris"  # 类属性

    def __init__(self, name, age):
        self.name = name  # 实例属性
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

    def __str__(self):
        return f"{self.name}, {self.age}岁"

my_dog = Dog("Buddy", 3)
print(f"Dog: {my_dog}")
print(f"species: {my_dog.species}")
print(f"bark(): {my_dog.bark()}")

# 类属性 vs 实例属性
your_dog = Dog("Max", 5)
Dog.species = "Felis catus"  # 修改类属性
print(f"my_dog.species: {my_dog.species}")  # 受影响
print(f"your_dog.species: {your_dog.species}")

# 实例方法、类方法、静态方法
class MyClass:
    class_attr = "类属性"

    def __init__(self, value):
        self.value = value

    def instance_method(self):
        return f"实例方法: {self.value}"

    @classmethod
    def class_method(cls):
        return f"类方法: {cls.class_attr}"

    @staticmethod
    def static_method():
        return "静态方法"

obj = MyClass(42)
print(MyClass.class_method())
print(obj.class_method())
print(MyClass.static_method())

# 私有属性约定
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # 受保护
        self.__pin = "1234"     # 私有

account = BankAccount(1000)
print(f"访问受保护属性: {account._balance}")
print(f"访问私有属性(改名后): {account._BankAccount__pin}")


# ====================
# 02 继承与多态
# ====================

print("\n" + "=" * 50)
print("02 继承与多态")
print("=" * 50)

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

animals = [Dog("Buddy"), Cat("Whiskers"), Dog("Rex")]
for animal in animals:
    print(animal.speak())

# 多继承
class Flyer:
    def fly(self):
        return "flying"

class Swimmer:
    def swim(self):
        return "swimming"

class Duck(Animal, Flyer, Swimmer):
    pass

duck = Duck("Donald")
print(f"Duck: {duck.speak()}, {duck.fly()}, {duck.swim()}")

# MRO
print(f"Duck MRO: {Duck.__mro__}")

# super()
class Child(Dog):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类 __init__
        self.breed = breed

    def speak(self):
        return f"{self.name} ({self.breed}) says woof!"

child_dog = Child("Rex", "Golden Retriever")
print(f"super() 示例: {child_dog}")
print(f"speak: {child_dog.speak()}")

# isinstance / issubclass
print(f"isinstance(child_dog, Dog): {isinstance(child_dog, Dog)}")
print(f"isinstance(child_dog, Animal): {isinstance(child_dog, Animal)}")

# 抽象基类
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

rect = Rectangle(3, 4)
print(f"矩形面积: {rect.area()}")


# ====================
# 03 魔术方法
# ====================

print("\n" + "=" * 50)
print("03 魔术方法")
print("=" * 50)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age}岁"

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

p1 = Person("Alice", 30)
p2 = Person("Bob", 25)
print(f"str: {str(p1)}")
print(f"repr: {repr(p1)}")
print(f"p1 == p2: {p1 == p2}")
print(f"p1 < p2: {p1 < p2}")

# 算术运算符
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 * 3 = {v1 * 3}")

# __call__：像函数一样调用
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return self.n + x

add5 = Adder(5)
print(f"add5(10) = {add5(10)}")

# 索引访问
class MyList:
    def __init__(self, data):
        self.data = list(data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

lst = MyList([1, 2, 3, 4, 5])
print(f"lst[0] = {lst[0]}")
print(f"lst[1:3] = {lst[1:3]}")
print(f"len(lst) = {len(lst)}")

# 上下文管理器
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False

import os
if not os.path.exists('test.txt'):
    with FileManager('test.txt') as f:
        f.write("Hello!")
    print("文件写入成功")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

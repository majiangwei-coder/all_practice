"""
装饰器：（装饰器的原理就是将原有的函数名重新定义为以原函数为参数的闭包）
含义：装饰器本质上就是一个闭包函数，它的好处就是在不修改原有代码的基础上，增加额外功能。

闭包函数的三个条件
1.函数嵌套
2.内函数要使用外函数的局部变量
3.外函数的返回值是内函数的函数名
"""


# # 标准版装饰器
#
# # 被装饰的函数
# def send():
#     print("正在发送消息~")
#
#
# def send2():
#     print("转账520~")
#
#
# # 装饰器函数
# def outer(fn):  # 外层函数： fn 是形参，但是往里面传入的是被装饰的函数名
#     # 既包含原有功能，又包含新功能
#     def inner():  # 内函数
#         print("登录~")
#         # 执行被装饰的函数
#         fn()  # 而内函数的函数体包含了外函数被传入的参数，也就是被装饰的原函数（send()），实现了不改动原函数代码，还执行了原函数和新增的函数体
#
#     return inner  # 外函数的返回值是一个引用，引用内函数，于是再去调用内函数
#
#
# print(outer(send))
# # ot = outer(send)
# # ot()  # 正在发送消息~
# outer(send)()  # 登录~ 正在发送消息~
# outer(send2)()  # 登录~ 转账520~


# # 语法糖
# # 格式：@装饰器名称
# def outer(fn):
#     def inner():
#         print("登录~")
#         # 执行被装饰的函数
#         fn()
#
#     return inner
#
#
# # 在被装饰的函数头上写下："@外函数名"，是装饰器的引用，后无括号（有括号是在调用执行函数，返回该函数实际会返回的值）意为下面的函数将被作为外函数的参数传入闭包
# # 注意顶格写，并写在被装饰的函数上一行
# @outer
# def send():
#     print("发送消息：笑死我了~")
#
#
# @outer
# def send2():
#     print("发送消息：呵呵呵~")
#
#
# send()  # 被装饰过的函数，在单独调用它时，就已经会被传入闭包，而非单纯执行该原函数
# send2()

import functools
# 被装饰的函数有参数
def outer(fn):
    @functools.wraps(fn)
    def inner(name):  # 内函数：有形参 name
        print(f"{name}是inner函数中的参数")
        fn(name)

    return inner


@outer
def func(name):  # 被装饰函数的形参要与内函数形参一致：因为被装饰函数有形参，又被内函数调用，所以只能通过内函数去传递
    print("这是被装饰的函数~")


func(
    "bingbing")  # 被装饰过的函数，就已经被替换增强（关键点是`@outer`装饰器。`@outer`等价于`func = outer(func)`。所以，装饰后，`func`实际上被替换成了`outer(func)`返回的函数，也就是`inner`函数）
outer(func)("SUSU")
outer(func.__wrapped__)("SUSU")     #绕过装饰器时：用 functools.wraps 保留原函数，并通过 原函数.__wrapped__ 访问（安全且可读）

"""
bingbing是inner函数中的参数
这是被装饰的函数~                   # 单层装饰：一层内函数

SUSU是inner函数中的参数
SUSU是inner函数中的参数
这是被装饰的函数~                   # 双层装饰：双层内函数

SUSU是inner函数中的参数
这是被装饰的函数~                   # 取消双层装饰：导入 functools 模块，在闭包内函数前使用 @functools.wraps(func) 保留原函数，并通过 func.__wrapped__ 来访问
"""


"""
对比`func("bingbing")`的输出：
```
bingbing是inner函数中的参数
这是被装饰的函数~
```
而`outer(func)("SUSU")`输出：
```
SUSU是inner函数中的参数
SUSU是inner函数中的参数
这是被装饰的函数~
```
确实不同，因为`outer(func)("SUSU")`导致了两次`inner`函数的调用：一次是新的`inner2`，一次是旧的`inner`。
总结原因：
- 当使用`@outer`装饰`func`时，`func`被替换为`outer(func)`返回的`inner`函数。
- 然后调用`outer(func)`，这里的`func`已经是装饰后的版本（即`inner`函数），所以`outer(func)`返回一个新的`inner`函数（`inner2`），它包裹了旧的`inner`。
- 调用`inner2("SUSU")`时，它先打印一次，然后调用旧的`inner("SUSU")`，旧的`inner`又打印一次并调用原始函数。
因此，输出多了一行打印。
在代码中，`outer(func)("SUSU")`相当于手动应用了装饰器两次，而`func("bingbing")`只应用了一次。
所以，最终输出不同是因为`outer(func)("SUSU")`对已经装饰过的函数再次应用装饰器，导致嵌套调用。

双重装饰导致嵌套调用：
outer(func) 将已装饰的func（即inner函数）作为参数传入outer，生成一个新的装饰层。
调用时，先执行新inner的打印，再执行旧inner的打印，最后执行原始函数。
这种行为突显了装饰器的本质——通过闭包嵌套修改函数行为，重复装饰会叠加效果。
"""

# # 被装饰的函数有可变参数 *args、**kwargs
# # 被装饰的函数
# def func(*args, **kwargs):
#     print(args)
#     print(kwargs)
#
#
# func(1, 3, "fsahdfkhajs", ({"我是：": "天下第一"}), name="bingbing")
#
#
# # 装饰器函数
# def outer(fn):
#     def inner(*args, **kwargs):
#         print(fn(*args, **kwargs))
#
#     return inner
#
#
# outer(func)(2, 4, "susu", True, {"键": "值"}, 键="值")

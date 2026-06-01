# class pet:
#     def eat(self):
#         return "宠物吃东西"
#
# class dog(pet):
#     def eat(self):
#         return "狗狗吃狗粮"
#
# class cat(pet):
#     def eat(self):
#         return "猫猫吃猫粮"
#
# class master:
#     def feed(self,a):
#         print(f"主人正在喂{a.eat()}")
#
# dog = dog()
# cat = cat()
# chicken = pet()
# master = master()
# master.feed(dog)
# master.feed(cat)
# master.feed(chicken)

import time
import threading

# def sing(name):
#     print(f'{name}开始唱歌')
#     time.sleep(3)
#     print(f'{name}唱完歌了')
#
#
# def dance(name):
#     print(f'{name}开始跳舞')
#     time.sleep(3)
#     print(f'{name}跳完舞了')
#
#
# if __name__ == "__main__":
#     # 创建子线程(注意：子线程的个数没有限制，而且子线程之间互相独立)
#     # target: 线程执行的函数名，不加小括号。（传入的是函数名，不是函数调用；小括号代表函数调用，函数调用会立即执行这个函数）
#     t1 = threading.Thread(target=sing, args=("susu",))  # 唱歌子线程
#     t2 = threading.Thread(target=dance, kwargs={'name':'bingbing'})  # 跳舞子线程
#     print(t1)
#     print(t2)
#     t1.start()
#     t2.start()


# def task():
#     time.sleep(1)
#     print("当前线程是：", threading.current_thread().name)  # 显示当前线程名称
#
#
# if __name__ == "__main__":
#    for i in range(5):
#        t = threading.Thread(target=task)
#        t.start()

# # 全局变量
# li = []
#
#
# # 写入数据
# def write_data():
#     for i in range(5):
#         li.append(i)
#         time.sleep(1)
#     print("写入的数据是：", li)
#
#
# # 读取数据
# def read_data():
#     print("读取的数据是：", li)
#
#
# # 主程序入口
# if __name__ == "__main__":
#     # 创建子线程
#     wd = threading.Thread(target=write_data)
#     rd = threading.Thread(target=read_data)
#
#     # 开启子线程
#     wd.start()
#
#     # 阻塞主线程：主线程等待写入线程执行完成以后代码再继续执行
#     wd.join()
#
#     rd.start()
#
#     rd.join()
#
#     print("这是最后一行")


# # 全局变量
# a = 0
#
#
# def add():
#     for i in range(10000000):
#         global a  # 声明全局变量
#         a += 1
#     print("第一次", a)
#
#
# def add2():
#     for i in range(10000000):
#         global a  # 声明全局变量
#         a += 1
#     print("第二次", a)
#
#
# # 主程序入口
# if __name__ == "__main__":
#     first = threading.Thread(target=add)
#     second = threading.Thread(target=add2)
#
#     # 开启子线程
#     first.start()
#
#     # 线程等待 join
#     first.join()
#
#     second.start()

# # 全局变量
# a = 0
#
# # 创建全局互斥锁
# lock = threading.Lock()
#
#
# def add():
#     # 上锁
#     lock.acquire()
#     for i in range(10000000):
#         global a  # 声明全局变量
#         a += 1
#     print("第一次", a)
#     # 释放锁
#     lock.release()
#
#
# def add2():
#     # 上锁
#     lock.acquire()
#     for i in range(10000000):
#         global a  # 声明全局变量
#         a += 1
#     print("第二次", a)
#
#
# # 主程序入口
# if __name__ == "__main__":
#     first = threading.Thread(target=add)
#     second = threading.Thread(target=add2)
#
#     # 开启子线程
#     first.start()
#     #
#     # # 线程等待 join
#     # first.join()
#     #
#     second.start()


# 导入模块
from multiprocessing import Process, Queue, Pool
import os

#
# # 唱歌任务
# def sing(name):
#     print(f"{name}在唱歌")
#     # 访问父进程编号
#     print(f"sing子进程id：{os.getpid()}，父进程id：{os.getppid()}")
#
# # 跳舞人物
# def dance(name):
#     print(f"{name}在跳舞")
#     # 访问父进程编号
#     print(f"dance子进程id：{os.getpid()}，父进程id：{os.getppid()}")     # sing 和 dance 的父进程编号将是同一个，这是因为这同属一个.py文件下，当前.py文件默认有一个主进程，所以父进程编号对应的就是.py文件主进程的进程编号
#
#
# # 主程序入口
# if __name__ == '__main__':
#     # 创建子进程
#     p1 = Process(target=sing,name="P1", args=("bingbing",))
#     p2 = Process(target=dance, name="P2",kwargs={"name": "susu"})
#
#     # 开启子进程
#     p1.start()
#
#     # 主进程等待子进程执行结束再执行
#     p1.join()
#
#     p2.start()
#
#     # 主进程等待子进程执行结束再执行
#     p2.join()
#
#     # 修改子进程名
#     p1.name = "Pro1"
#     p2.name = "Pro2"
#
#     # 访问name属性：通过进程对象名.name
#     print("p1的子进程名：", p1.name)
#     print("p2的子进程名：", p2.name)
#
#     # 查看子进程的进程编号
#     print("p1子进程编号：", p1.pid)
#     print("p2子进程编号：", p2.pid)
#
#     # 查看主进程及其父进程编号
#     print(f"主进程id：{os.getpid()}，父进程id：{os.getppid()}")
#
#     # 检查子进程是否仍然在运行
#     print("p1是否存活：", p1.is_alive())
#     print("p2是否存活：", p2.is_alive())


# # 定义全局变量
# li = []
#
#
# # 写入数据任务
# def write_data():
#     for i in range(5):
#         li.append(i)
#         time.sleep(1)
#     print("写入的数据是：", li)
#
#
# # 读取数据任务
# def read_data():
#     print("读取的数据是：", li)
#
#
# # 主程序入口
# if __name__ == "__main__":
#     # 创建子进程
#     wp = Process(target=write_data)
#     rp = Process(target=read_data)
#
#     # 开启子进程
#     wp.start()
#
#     # 主进程等待子进程执行结束
#     wp.join()       # 等数据写入完成再去读取
#
#     rp.start()
#
#     # 结果：写入的数据是： [0, 1, 2, 3, 4]，读取的数据是： []。
#     # 为什么先写完再读取，读取到的数据仍然是空列表，why？ 因为  *******  进 程 之 间 资 源 是 不 共 享 的   ！  *******


# # 实例化队列对象
# q = Queue(3)    # 这个队列对象最多可接收 3 条消息，没写或是负值代表没有上限
#
# # 放入数据
# q.put("今天平安夜")
# q.put("要回家吃苹果了")    # 放入两条消息
#
# # 判断队列是否已满
# print(q.full())     # False
#
# q.put("好开心哦~")        # 再放入一条消息
#
# # 判断队列是否已满
# print(q.full())     # True
#
# # 查看数据数量
# print("消息数量一：", q.qsize())  # 3
#
# # 取出数据
# print(q.get())
# print(q.get())      #取出了两条数据
#
# # 判断队列是否为空
# print(q.empty())    # False
#
# print(q.get())      # 再取出一条
#
# print(q.empty())    # True
#
# # 查看数据数量
# print("消息数量二：", q.qsize())


# # 定义全局变量
# li = ["张三", "李四", "王五", "赵六"]
#
#
# # 写入数据任务
# def write_data(q):
#     # 将列表中的数据依次放入队列中
#     for i in li:
#         print(f"{i}已经被放入~")
#         q.put(i)
#         time.sleep(0.5)
#
#
# # 读取数据任务
# def read_data(q):
#     # 只要队列中有消息就取出来
#     while True:
#         # 判断队列是否为空
#         if q.empty():
#             break
#         # 不为空就取出消息
#         else:
#             print("从队列中取出消息", q.get())
#
#
# # 主程序入口
# if __name__ == "__main__":
#     # 创建队列对象
#     q = Queue()  # 不确定有多少条数据，就省略里面的参数，没有大小限制
#     # 创建子进程
#     wp = Process(target=write_data, args=(q,))
#     rp = Process(target=read_data, args=(q,))
#
#     # 开启子进程
#     wp.start()
#
#     # 让主进程等待子进程执行结束
#     wp.join()   # 等待队列中的数据放入完成
#
#     rp.start()

# # 任务
# def task(num):
#     print("圣诞节快到了，还在上班！")
#     time.sleep(2)
#     return num * 3
#
#
# # 主程序入口
# if __name__ == "__main__":
#     # 实例化一个进程池对象，最大进程数是 3
#     p = Pool(3)
#
#     # 定义一个空列表
#     li = []
#     # 循环
#     for i in range(7):
#         # 执行：apply_async(调用的目标方法, 参数)
#         # 异步：进程不需要一直等待下去，而是继续执行下面的操作，不管其他进程的状态。举例：先煮面，再吃面，最后洗碗（必须先后执行），这就是同步；一边泡面一边听音乐（同时执行），这就是异步，
#         res = p.apply_async(task, args=(i,))
#         print(res)
#         # 将返回数值结果放进列表中
#         li.append(res)
#
#     # 关闭进程池
#     p.close()
#
#     # 等待进程池中的所有子进程执行完毕，必须放在close()后面
#     p.join()
#
#     # 使用 get 方法来获取 apply_async() 的结果
#     for i in li:
#         print(i.get())


# # 协程
# # 生成器函数：函数中有 yield 关键字

from greenlet import greenlet

# def task1():
#     while True:
#         yield 123   # yield作用：返回123，并暂停函数，在此处挂起，使用 next() 再次调用生成器时，再从此处恢复执行
#     # yield "bingbing"
#
# def task2():
#     while True:
#         yield 456
#     # yield "susu"
#
# # 出程序入口
# if __name__ =="__main__":
#     # 调用函数
#     t1 = task1()    # 调用生成器函数
#     # print(t1)       # 返回生成器对象 <generator object task1 at 0x000002741A157530>
#     t2 = task2()
#
#     # # 获取值
#     # print(next(t1))
#     # print(next(t2))
#     # print(next(t1))
#     # print(next(t2))
#
#     # for i in range(2):    # 只有两次，取完就走，体现不出 StopIteration（停止迭代）
#     #     print(next(t1))
#     #     print(next(t2))
#
#     while True:             # StopIteration（停止迭代）
#         print(next(t2))
#         print(next(t1))     # 自行决定任务的执行顺序


# # 唱歌任务
# def sing():
#     print("在唱歌")
#     g2.switch()     # "在唱歌" 执行完后切换到 g2 中运行去了，下一句 "唱完歌了"是不会执行的，因为没有切换回来，所以仍需要在 g2 中切换回来
#     print("唱完歌了")
#
# # 跳舞任务
# def dance():
#     print("在跳舞")
#     print("跳完舞了")
#     g1.switch()     # 在唱歌-在跳舞-跳完舞了-唱完歌了
#
# # sing()
# # dance()
#
# # 主程序入口
# if __name__ == "__main__":
#     # 实例化一个协程对象：greenlet(任务名)
#     g1 = greenlet(sing)
#     g2 = greenlet(dance)
#
#     g1.switch()  # 切换到 g1 中执行
#     # g2.switch()     # 此时 dance() 就不会运行
#     g2.switch()  # 切换到 g2 中执行
#     g1.switch()  # 切换到 g1 中执行
#     g2.switch()  # 切换到 g2 中执行

import gevent  # gevent 自带 gevent.sleep() 耗时函数，请勿使用 time 模块中的 time.sleep()
import time
from gevent import monkey

# # 唱歌任务
# def sing():
#     print("在唱歌")
#     gevent.sleep(2)     # 模拟的是 gevent 可以识别的 IO 阻塞
#     print("唱完歌了")
#
#
# # 跳舞任务
# def dance():
#     print("在跳舞")
#     gevent.sleep(2)     # 顺序一样，但时间差变了
#     print("跳完舞了")
#
#
# # 主程序入口
# if __name__ == "__main__":
#     # 创建协程对象
#     g1 = gevent.spawn(sing)
#     g2 = gevent.spawn(dance)
#     # 阻塞，等待协程执行完毕
#     g1.join()   # 等待 g1 对象执行结束
#     g2.join()   # 等待 g2 对象执行结束


monkey.patch_all()   # 将用到的time.sleep() 替换为 gevent里面自己实现耗时操作的 gevent.sleep()
# 注意： monkey.patch_all() 必须放在被打补丁者的前面
# 唱歌任务
def sing(name):
    for i in range(1, 4):
        print(f"{name}在唱歌，被送走的第{i}次")
        # gevent.sleep(1)     # 可识别的 IO 阻塞操作
        time.sleep(1)

# 主程序入口
if __name__ == "__main__":
    # 等待所有协程都执行完毕
    gevent.joinall([
        gevent.spawn(sing, "bingbing"),
        gevent.spawn(sing, "冰冰")
    ])
    # # 创建协程对象
    # g1 = gevent.spawn(sing, "bingbing")
    # g2 = gevent.spawn(sing,"冰冰")
    # gevent.joinall([g1, g2])
            # 注意：如果没有遇到可识别的 IO 操作，不会进行任务切换，无法实现并发效果。



















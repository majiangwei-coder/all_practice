"""
第八章：并发编程示例代码
配合 07_并发编程/ 目录下的 Markdown 文档学习
包含：多线程、多进程、asyncio
"""

# ====================
# 多线程
# ====================

print("=" * 50)
print("多线程")
print("=" * 50)

import threading
import time
from concurrent.futures import ThreadPoolExecutor

# 基本线程创建
print("--- 基本线程 ---")
def task(n):
    print(f"任务 {n} 开始")
    time.sleep(0.5)
    print(f"任务 {n} 完成")

threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("所有线程结束")

# ThreadPoolExecutor
print("\n--- ThreadPoolExecutor ---")
def task(n):
    return n * 2

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, i) for i in range(5)]
    for f in futures:
        print(f"结果: {f.result()}")

# Lock 互斥锁
print("\n--- Lock ---")
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"counter 最终值 (应该=200000): {counter}")

# Semaphore 信号量
print("\n--- Semaphore ---")
semaphore = threading.Semaphore(2)

def access_resource(n):
    semaphore.acquire()
    print(f"线程 {n} 获取信号")
    time.sleep(0.5)
    semaphore.release()
    print(f"线程 {n} 释放信号")

threads = [threading.Thread(target=access_resource, args=(i,)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Event 事件
print("\n--- Event ---")
event = threading.Event()

def waiter():
    print("等待信号...")
    event.wait()
    print("收到信号!")

def setter():
    time.sleep(1)
    event.set()

t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)
t1.start()
t2.start()
t1.join()
t2.join()

# Queue 队列
print("\n--- Queue ---")
import queue

def producer(q):
    for i in range(5):
        q.put(i)
        time.sleep(0.1)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"消费: {item}")
        q.task_done()

q = queue.Queue()
t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))
t1.start()
t2.start()
t1.join()
q.put(None)
t2.join()


# ====================
# 多进程
# ====================

print("\n" + "=" * 50)
print("多进程")
print("=" * 50)

import multiprocessing as mp

# 注意：Windows 需要在 if __name__ == "__main__" 下运行
# 下面演示的是 Linux/Mac 的多进程模式

# Pool.map
print("--- Pool.map ---")
def square(n):
    return n * n

with mp.Pool(4) as pool:
    results = pool.map(square, range(5))
    print(f"square results: {results}")

# Pool.starmap
print("\n--- Pool.starmap ---")
def power(base, exp):
    return base ** exp

with mp.Pool(4) as pool:
    params = [(2, 1), (2, 2), (2, 3)]
    results = pool.starmap(power, params)
    print(f"power results: {results}")

# 进程间通信 - Queue
print("\n--- 进程 Queue ---")

def producer(q):
    for i in range(5):
        q.put(i)
    q.put(None)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"消费: {item}")

if __name__ == "__main__":
    # Windows 兼容
    queue = mp.Queue()
    p1 = mp.Process(target=producer, args=(queue,))
    p2 = mp.Process(target=consumer, args=(queue,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

# 共享内存
print("\n--- 共享内存 ---")
shared_counter = mp.Value('i', 0)

def increment(shared):
    with shared.get_lock():
        shared.value += 1

if __name__ == "__main__":
    processes = [mp.Process(target=increment, args=(shared_counter,)) for _ in range(10)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(f"shared_counter: {shared_counter.value}")


# ====================
# asyncio 异步
# ====================

print("\n" + "=" * 50)
print("asyncio 异步")
print("=" * 50)

import asyncio

# 基础协程
print("--- 基础协程 ---")

async def greet():
    return "Hello!"

async def main():
    result = await greet()
    print(f"协程结果: {result}")

asyncio.run(main())

# asyncio.sleep (非阻塞等待)
print("\n--- asyncio.sleep ---")

async def demo_sleep():
    print("开始睡眠 0.5 秒")
    await asyncio.sleep(0.5)
    print("睡眠结束")

asyncio.run(demo_sleep())

# 并发执行 - gather
print("\n--- asyncio.gather ---")

async def task(n):
    await asyncio.sleep(n * 0.1)
    return n

async def main_gather():
    results = await asyncio.gather(
        task(1),
        task(2),
        task(0.5)
    )
    print(f"gather 结果: {results}")

asyncio.run(main_gather())

# create_task
print("\n--- create_task ---")

async def main_task():
    task1 = asyncio.create_task(task(1))
    task2 = asyncio.create_task(task(2))

    print("任务已创建，等待完成...")
    results = await asyncio.gather(task1, task2)
    print(f"任务结果: {results}")

asyncio.run(main_task())

# asyncio.Queue
print("\n--- asyncio.Queue ---")

async def async_producer(queue, n):
    for i in range(n):
        await queue.put(i)
        await asyncio.sleep(0.1)

async def async_consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"消费: {item}")
        queue.task_done()

async def main_queue():
    queue = asyncio.Queue()
    await asyncio.gather(
        async_producer(queue, 5),
        async_consumer(queue)
    )

asyncio.run(main_queue())

# 超时控制
print("\n--- wait_for 超时 ---")

async def long_task():
    await asyncio.sleep(10)
    return "done"

async def with_timeout():
    try:
        result = await asyncio.wait_for(long_task(), timeout=1)
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("任务超时!")

asyncio.run(with_timeout())

# 并发限制 - Semaphore
print("\n--- Semaphore 并发限制 ---")

async def limited_task(semaphore, n):
    async with semaphore:
        await asyncio.sleep(0.5)
        return n

async def main_semaphore():
    semaphore = asyncio.Semaphore(2)  # 最多同时2个
    tasks = [limited_task(semaphore, i) for i in range(4)]
    results = await asyncio.gather(*tasks)
    print(f"结果: {results}")

asyncio.run(main_semaphore())

print("\n" + "=" * 50)
print("并发编程示例执行完毕")
print("=" * 50)

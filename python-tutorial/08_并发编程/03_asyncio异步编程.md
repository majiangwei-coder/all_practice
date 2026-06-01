# asyncio 异步编程

> 本章讲解 Python 异步编程的核心概念：协程、事件循环、async/await。

---

## 1. 同步 vs 异步

### 同步方式

```python
# 同步：每个请求必须等待完成才能处理下一个
import requests

def fetch_all(urls):
    results = []
    for url in urls:
        resp = requests.get(url)  # 阻塞等待！
        results.append(resp.text)
    return results

# 3个请求，每个1秒 → 总共3秒
```

### 异步方式

```python
# 异步：发起请求后不等待，立即处理下一个
# 等待时可以做其他事
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# 3个请求同时发起 → 总共1秒（理论上）
```

### 图解

```
同步（串行）：
  请求1 ████████ 3秒
  请求2          ████████ 3秒
  请求3                   ████████ 3秒
  总计：9秒

异步（并行）：
  请求1 ████████████████
  请求2 ████████████████
  请求3 ████████████████
  总计：3秒
```

---

## 2. 协程（Coroutine）基础

### 协程是什么

**协程**是一种比线程更轻量的并发方式。在 Python 中，协程是特殊的函数。

```python
# 普通函数：调用会阻塞，直到返回
def normal_func():
    return "Hello!"

# 协程函数：调用返回协程对象，不执行
async def coro_func():
    return "Hello!"

# 调用协程
result = coro_func()
print(result)  # <coroutine object> ← 不是字符串！
```

### 运行协程

```python
import asyncio

async def greet():
    return "Hello!"

# 方式1：asyncio.run()（推荐）
asyncio.run(greet())  # "Hello!"

# 方式2：旧版事件循环（了解即可）
# loop = asyncio.get_event_loop()
# loop.run_until_complete(greet())
```

---

## 3. await 关键字

`await` 用于**等待协程执行完成**：

```python
import asyncio

async def step1():
    print("步骤1开始")
    await asyncio.sleep(1)  # 等待1秒（不阻塞其他任务）
    print("步骤1完成")
    return "结果1"


async def step2():
    print("步骤2开始")
    await asyncio.sleep(0.5)
    print("步骤2完成")
    return "结果2"


async def main():
    # 顺序执行：step1 然后 step2
    result1 = await step1()
    result2 = await step2()
    print(f"全部完成: {result1}, {result2}")


asyncio.run(main())
# 顺序执行：~1.5秒
```

---

## 4. 并发执行：asyncio.gather

同时执行多个协程：

```python
import asyncio
import time

async def task(n):
    await asyncio.sleep(n * 0.1)
    return n


async def main():
    start = time.time()

    # 并发执行3个任务
    results = await asyncio.gather(
        task(1),
        task(2),
        task(3)
    )

    elapsed = time.time() - start
    print(f"结果: {results}")  # [1, 2, 3]
    print(f"耗时: {elapsed:.2f}秒")  # ~0.3秒（并行）


asyncio.run(main())
```

### gather vs 顺序 await

```python
# 顺序执行
await task1()  # 1秒
await task2()  # 1秒
# 总计：2秒

# gather 并发执行
await asyncio.gather(task1(), task2())  # 1秒
# 总计：1秒
```

---

## 5. create_task 任务管理

`create_task` 创建任务，立即开始执行：

```python
import asyncio

async def task(n):
    await asyncio.sleep(1)
    return n


async def main():
    # 创建任务（立即开始执行）
    t1 = asyncio.create_task(task(1))
    t2 = asyncio.create_task(task(2))

    print("任务已创建，do something...")
    await asyncio.sleep(0.5)
    print("做完了...")
    # 等待任务完成
    results = await asyncio.gather(t1, t2)
    print(f"结果: {results}")


asyncio.run(main())
```

---

## 6. 异步上下文管理器

```python
import asyncio

class AsyncContext:
    async def __aenter__(self):
        print("进入上下文")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("退出上下文")
        return False  # 不屏蔽异常


async def main():
    async with AsyncContext() as ctx:
        print("使用资源")


asyncio.run(main())
```

---

## 7. 异步迭代器

```python
import asyncio


class AsyncCounter:
    """异步计数器"""

    def __init__(self, n):
        self.n = n
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        value = self.current
        self.current += 1
        return value


async def main():
    async for i in AsyncCounter(5):
        print(f"计数: {i}")


asyncio.run(main())
```

---

## 8. asyncio.Queue 异步队列

```python
import asyncio


async def producer(queue, n):
    for i in range(n):
        await queue.put(i)
        print(f"生产: {i}")
        await asyncio.sleep(0.5)


async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"消费: {item}")
        queue.task_done()


async def main():
    queue = asyncio.Queue()

    # 同时运行生产者和消费者
    await asyncio.gather(
        producer(queue, 5),
        consumer(queue)
    )


asyncio.run(main())
```

---

## 9. 超时控制

```python
import asyncio


async def long_task():
    await asyncio.sleep(10)
    return "完成"


async def with_timeout():
    try:
        # 3秒超时
        result = await asyncio.wait_for(long_task(), timeout=3)
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("任务超时！")


asyncio.run(with_timeout())
```

---

## 10. 取消任务

```python
import asyncio


async def task():
    try:
        while True:
            print("任务运行中...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("任务被取消")
        raise


async def main():
    t = asyncio.create_task(task())
    await asyncio.sleep(3)
    t.cancel()  # 取消任务
    try:
        await t  # 等待取消完成
    except asyncio.CancelledError:
        print("任务已确认取消")


asyncio.run(main())
```

---

## 11. 并发限制：Semaphore

限制同时运行的任务数：

```python
import asyncio


async def limited_task(semaphore, n):
    async with semaphore:
        await asyncio.sleep(1)
        return n


async def main():
    semaphore = asyncio.Semaphore(2)  # 最多同时2个

    # 5个任务，但限制2个并发
    tasks = [limited_task(semaphore, i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(f"结果: {results}")


asyncio.run(main())
# 5个任务，每次最多2个并发，~3秒完成
```

---

## 12. 常见错误

### 错误1：在非 async 函数中使用 await

```python
# 错误！
def sync_func():
    await asyncio.sleep(1)  # SyntaxError

# 正确！
async def async_func():
    await asyncio.sleep(1)
```

### 错误2：忘记 await

```python
async def task():
    return "done"


async def main():
    # 错误：返回的是协程对象，不是字符串
    # result = task()  # 协程对象！

    # 正确
    result = await task()  # "done"
    print(result)
```

### 错误3：阻塞事件循环

```python
# 错误！在 async 函数中使用同步阻塞
async def bad_example():
    time.sleep(10)  # 阻塞整个事件循环！

# 正确
async def good_example():
    await asyncio.sleep(10)  # 不阻塞其他任务
```

---

## 13. 小结

### 核心概念

| 概念 | 说明 |
|------|------|
| `async def` | 定义协程函数 |
| `await` | 等待协程完成 |
| `asyncio.run()` | 运行顶层协程 |
| `asyncio.gather()` | 并发执行多个协程 |
| `asyncio.create_task()` | 创建任务 |
| `asyncio.sleep()` | 异步睡眠 |

### 关键点

1. **`async/await` 是 Python 3.5+ 的语法**
2. **asyncio 适合 I/O 密集型**：网络请求、文件读写
3. **不要在 async 中使用同步阻塞**：用 `await asyncio.sleep()` 代替 `time.sleep()`
4. **协程是单线程内的并发**：不涉及锁（GIL 问题在 asyncio 中不明显）

### 什么时候用 asyncio

| 场景 | 选择 |
|------|------|
| I/O 密集（网络请求） | asyncio / aiohttp |
| CPU 密集 | 多进程 |
| 简单并发 | concurrent.futures |
| 需要真实并行 | multiprocessing |

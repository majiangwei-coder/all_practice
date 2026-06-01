# datetime 与 time

## datetime 模块

### datetime 类

```python
from datetime import datetime

# 当前时间
now = datetime.now()
print(now)  # 2024-03-15 10:30:45.123456

# 特定时间
dt = datetime(2024, 12, 25, 9, 30, 0)
print(dt)  # 2024-12-25 09:30:00
```

### datetime 属性

```python
dt = datetime(2024, 3, 15, 10, 30, 45)

print(dt.year)      # 2024
print(dt.month)     # 3
print(dt.day)       # 15
print(dt.hour)      # 10
print(dt.minute)    # 30
print(dt.second)    # 45
print(dt.weekday()) # 4 (0=周一, 4=周五)
print(dt.isoweekday())  # 5 (1=周一)
```

### 字符串转换

```python
from datetime import datetime

# datetime → 字符串
dt = datetime.now()
print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # "2024-03-15 10:30:45"
print(dt.strftime("%Y/%m/%d"))           # "2024/03/15"
print(dt.strftime("%B %d, %Y"))          # "March 15, 2024"

# 字符串 → datetime
dt = datetime.strptime("2024-03-15", "%Y-%m-%d")
print(dt)  # 2024-03-15 00:00:00
```

### strftime 格式代码

| 代码 | 含义 | 示例 |
|------|------|------|
| `%Y` | 4位年份 | 2024 |
| `%y` | 2位年份 | 24 |
| `%m` | 月（2位） | 03 |
| `%B` | 月（全名） | March |
| `%b` | 月（缩写） | Mar |
| `%d` | 日 | 15 |
| `%H` | 小时（24制） | 10 |
| `%I` | 小时（12制） | 10 |
| `%M` | 分钟 | 30 |
| `%S` | 秒 | 45 |
| `%p` | AM/PM | AM |
| `%w` | 星期（数字） | 5 |
| `%j` | 一年中的第几天 | 75 |

### datetime 比较与运算

```python
from datetime import datetime

dt1 = datetime(2024, 3, 15)
dt2 = datetime(2024, 3, 20)

# 比较
print(dt1 < dt2)   # True
print(dt1 == dt2)  # False

# 差值（timedelta）
diff = dt2 - dt1
print(diff)             # 5 days, 0:00:00
print(diff.days)        # 5
print(diff.total_seconds())  # 432000.0
```

## date 类

```python
from datetime import date

# 纯日期（无时间）
today = date.today()
print(today)  # 2024-03-15

# 创建
d = date(2024, 12, 25)
print(d.strftime("%Y-%m-%d"))  # 2024-12-25

# date 与 datetime
from datetime import datetime
dt = datetime.now()
d = dt.date()  # 提取 date 部分
t = dt.time()  # 提取 time 部分
```

## time 类

```python
from datetime import time

# 纯时间（无日期）
t = time(14, 30, 45)
print(t)           # 14:30:45
print(t.hour)      # 14
print(t.minute)    # 30
print(t.second)    # 45
print(t.strftime("%H:%M:%S"))  # "14:30:45"
```

## timedelta 类

时间差，用于日期运算：

```python
from datetime import datetime, timedelta

# 创建
delta = timedelta(days=5, hours=3, minutes=30)
print(delta)  # 5 days, 3:30:00

# 日期运算
dt = datetime(2024, 3, 15)
new_dt = dt + timedelta(days=10)
print(new_dt)  # 2024-03-25 00:00:00

# 时间差计算
dt1 = datetime(2024, 3, 20, 10, 0)
dt2 = datetime(2024, 3, 15, 8, 0)
diff = dt1 - dt2
print(diff.days)          # 5 (天)
print(diff.seconds)        # 7200 (2小时的秒数)
print(diff.total_seconds()) # 432000.0 (总共秒数)
print(diff.total_seconds() / 3600)  # 120.0 (总共小时数)
```

### 时间跨度表示

```python
delta = timedelta(days=30)

# 时间跨度转天/秒
print(delta.days)              # 30
print(delta.total_seconds())   # 2592000.0

# 从秒创建
delta = timedelta(seconds=3600)  # 1小时
print(delta)  # 1:00:00
```

## timezone 时区

```python
from datetime import datetime, timezone, timedelta

# UTC 时间
utc_now = datetime.now(timezone.utc)
print(utc_now)  # 2024-03-15 10:30:45+00:00

# 指定时区
tz = timezone(timedelta(hours=8))  # 北京时间 +8
bj_time = datetime(2024, 3, 15, 10, 30, tzinfo=tz)
print(bj_time)  # 2024-03-15 10:30:00+08:00

# astimezone：转换时区
utc_time = datetime.now(timezone.utc)
print(utc_time.astimezone(timezone(timedelta(hours=8))))
```

## time 模块

time 模块提供时间底层操作：

```python
import time

# Unix 时间戳（秒）
print(time.time())  # 1710499845.123

# 睡眠
time.sleep(1)  # 暂停 1 秒

# 结构化时间
t = time.localtime()  # 本地时间
print(t.tm_year, t.tm_mon, t.tm_mday)

t = time.gmtime()  # UTC 时间
```

### 格式化为字符串

```python
import time

# asctime：易读格式
print(time.asctime())  # 'Fri Mar 15 10:30:45 2024'

# strftime（与 datetime 相同）
print(time.strftime("%Y-%m-%d %H:%M:%S"))
```

## 实际应用

### 1. 测量执行时间

```python
import time
from datetime import datetime

# 方式1：time 模块
start = time.perf_counter()
# 耗时操作
elapsed = time.perf_counter() - start

# 方式2：datetime
start = datetime.now()
# 操作
elapsed = (datetime.now() - start).total_seconds()
```

### 2. 格式化显示

```python
from datetime import datetime

now = datetime.now()

# 人类友好格式
print(now.strftime("%Y年%m月%d日 %H:%M:%S"))
print(now.strftime("%Y-%m-%d %I:%M %p"))  # 12小时制

# ISO 格式
print(now.isoformat())
```

### 3. 日期边界处理

```python
from datetime import datetime, timedelta

def get_month_range(year, month):
    start = datetime(year, month, 1)
    # 下个月第一天减一天
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)
    return start, end

start, end = get_month_range(2024, 2)
print(f"{start} 到 {end}")  # 2024-02-01 到 2024-02-29
```

### 4. 人性化时间

```python
from datetime import datetime, timedelta

def humanize_time(dt):
    now = datetime.now()
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return "刚刚"
    elif seconds < 3600:
        return f"{int(seconds / 60)}分钟前"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}小时前"
    elif seconds < 604800:
        return f"{int(seconds / 86400)}天前"
    else:
        return dt.strftime("%Y-%m-%d")

print(humanize_time(datetime.now() - timedelta(hours=3)))
```

## 小结

1. **datetime**：日期时间组合
2. **date**：纯日期
3. **time**：纯时间
4. **timedelta**：时间差，用于日期加减
5. **timezone**：时区信息
6. **strftime**：datetime → 字符串
7. **strptime**：字符串 → datetime
8. **time.time()**：获取时间戳
9. **time.sleep()**：暂停

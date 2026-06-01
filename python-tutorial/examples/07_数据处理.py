"""
第七章：数据处理示例代码
配合 06_数据处理/ 目录下的 Markdown 文档学习
包含：文件IO、JSON、正则表达式
"""

import os

# ====================
# 文件与 IO
# ====================

print("=" * 50)
print("文件与 IO")
print("=" * 50)

# 写入文件
print("--- 基本文件操作 ---")
test_file = "test_io.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行\n")

# 读取文件
with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"read(): {content}")

# 按行读取
with open(test_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"readlines(): {lines}")

# 遍历文件对象
with open(test_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        print(f"第{i+1}行: {line}", end="")

# 写入多行
print("\n--- writelines ---")
with open(test_file, "w") as f:
    lines = ["line1\n", "line2\n", "line3\n"]
    f.writelines(lines)

# JSON 文件
print("\n--- JSON 文件 ---")
import json

data = {
    "name": "Alice",
    "age": 30,
    "scores": [95, 88, 76],
    "active": True,
    "address": {"city": "NYC", "zip": "10001"}
}

json_file = "test.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取 JSON
with open(json_file, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(f"JSON 加载: {loaded}")

# JSON 字符串互转
json_str = json.dumps(data, indent=2)
print(f"\nJSON 字符串 (前100字符):\n{json_str[:100]}...")

parsed = json.loads(json_str)
print(f"JSON 解析: {parsed}")

# 自定义 JSON 编码
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data_with_date = {"event": "conference", "date": datetime.now()}
json_str = json.dumps(data_with_date, cls=DateTimeEncoder)
print(f"\n自定义编码 datetime: {json_str}")

# JSON 反序列化回调
def datetime_parser(dct):
    if "date" in dct and "event" in dct:
        dct["date"] = datetime.fromisoformat(dct["date"])
    return dct

parsed = json.loads(json_str, object_hook=datetime_parser)
print(f"自定义解析: {parsed}")

# CSV 文件
print("\n--- CSV 文件 ---")
import csv

csv_file = "test.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "City"])
    writer.writerow(["Alice", 30, "NYC"])
    writer.writerow(["Bob", 25, "LA"])

# 读取 CSV
with open(csv_file, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"CSV 行: {row}")

# 读取为字典
with open(csv_file, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"CSV Dict: {dict(row)}")

# pickle
print("\n--- pickle ---")
import pickle

pickle_file = "test.pkl"
data_to_pickle = {"name": "Alice", "scores": [1, 2, 3]}

# 序列化
with open(pickle_file, "wb") as f:
    pickle.dump(data_to_pickle, f)

# 反序列化
with open(pickle_file, "rb") as f:
    restored = pickle.load(f)
print(f"pickle 恢复: {restored}")

# 清理测试文件
print("\n--- 清理 ---")
for f in [test_file, json_file, csv_file, pickle_file]:
    if os.path.exists(f):
        os.remove(f)
        print(f"已删除: {f}")


# ====================
# 正则表达式
# ====================

print("\n" + "=" * 50)
print("正则表达式")
print("=" * 50)

import re

text = "我的邮箱是 alice@example.com，另一个是 bob@test.org，电话 138-1234-5678"

# search - 查找第一个匹配
print("--- search ---")
match = re.search(r'\w+@\w+\.\w+', text)
if match:
    print(f"找到: {match.group()}")

# findall - 查找所有匹配
print("\n--- findall ---")
emails = re.findall(r'\w+@\w+\.\w+', text)
print(f"所有邮箱: {emails}")

phones = re.findall(r'\d{3}-\d{4}-\d{4}', text)
print(f"所有电话: {phones}")

# sub - 替换
print("\n--- sub ---")
masked = re.sub(r'\w+@\w+\.\w+', '[EMAIL]', text)
print(f"邮箱替换: {masked}")

# sub with 分组引用
date_text = "2024-03-15"
result = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', date_text)
print(f"日期格式转换: {result}")

# split
print("\n--- split ---")
parts = re.split(r'[,;|]', "apple,banana;cherry|orange")
print(f"分割: {parts}")

# 贪婪 vs 非贪婪
print("\n--- 贪婪 vs 非贪婪 ---")
html = "<div>content</div>"
print(f"HTML: {html}")
print(f"贪婪 .+: {re.search(r'<.+>', html).group()}")
print(f"非贪婪 .+?: {re.search(r'<.+?>', html).group()}")

# 分组
print("\n--- 分组 ---")
phone_text = "张三: 138-1234-5678，李明: 139-9999-8888"
pattern = r'(\d{3})-(\d{4})-(\d{4})'
for match in re.finditer(pattern, phone_text):
    print(f"完整: {match.group()}, 区号: {match.group(1)}, 号: {match.group(2)}-{match.group(3)}")

# 命名分组
print("\n--- 命名分组 ---")
pattern = r'(?P<area>\d{3})-(?P<number>\d{4}-\d{4})'
match = re.search(pattern, phone_text)
if match:
    print(f"区号: {match.group('area')}, 号码: {match.group('number')}")
    print(f"_asdict: {match._asdict()}")

# compile 预编译
print("\n--- compile ---")
pattern = re.compile(r'\d{3}-\d{4}-\d{4}')
matches = pattern.findall(phone_text)
print(f"预编译模式: {matches}")

# flags
print("\n--- flags ---")
text_multi = "Hello\nWorld\nhello"
print(f"多行模式: {re.findall(r'^hello', text_multi, re.IGNORECASE | re.MULTILINE)}")

# 常用模式
print("\n--- 常用模式 ---")

# 验证手机号
def validate_phone(phone):
    return bool(re.fullmatch(r'1[3-9]\d{9}', phone))

print(f"13812345678 有效: {validate_phone('13812345678')}")
print(f"12345678901 有效: {validate_phone('12345678901')}")

# 提取数字
text_with_nums = "价格是1999元，促销价仅999元"
numbers = re.findall(r'\d+', text_with_nums)
print(f"提取数字: {numbers}")

# 清洗 HTML
html_text = "<p>Hello <b>World</b>!</p>"
clean = re.sub(r'<[^>]+>', '', html_text)
print(f"清洗HTML: {clean}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

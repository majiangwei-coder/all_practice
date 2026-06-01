"""
第五章：异常与调试 示例代码
配合 05_异常与调试/ 目录下的 Markdown 文档学习
"""

# ====================
# 异常处理
# ====================

print("=" * 50)
print("异常处理")
print("=" * 50)

# 基本 try/except/else/finally
print("--- 基本结构 ---")
try:
    result = 10 / 2
    print(f"计算成功: {result}")
except ZeroDivisionError:
    print("除数不能为零")
except Exception as e:
    print(f"其他错误: {e}")
else:
    print("执行成功（无异常）")
finally:
    print("清理资源")

# 多异常捕获
print("\n--- 多异常捕获 ---")
try:
    # int("abc")
    # [1, 2, 3][10]
    result = 1 / 0
except (ValueError, TypeError) as e:
    print(f"值或类型错误: {e}")
except IndexError as e:
    print(f"索引错误: {e}")
except Exception as e:
    print(f"未知错误: {type(e).__name__}: {e}")

# 常见异常类型演示
print("\n--- 常见异常类型 ---")

# IndexError
try:
    lst = [1, 2, 3]
    print(lst[10])
except IndexError as e:
    print(f"IndexError: {e}")

# KeyError
try:
    d = {"a": 1}
    print(d["b"])
except KeyError as e:
    print(f"KeyError: {e}")

# TypeError
try:
    print("hello" + 1)
except TypeError as e:
    print(f"TypeError: {e}")

# ValueError
try:
    print(int("abc"))
except ValueError as e:
    print(f"ValueError: {e}")

# 自定义异常
print("\n--- 自定义异常 ---")

class ValidationError(Exception):
    """验证错误异常"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

try:
    raise ValidationError("email", "格式不正确")
except ValidationError as e:
    print(f"捕获自定义异常: {e.field}: {e.message}")

# 异常链
print("\n--- 异常链 ---")

try:
    try:
        int("abc")
    except ValueError as e:
        raise RuntimeError("转换失败") from e
except RuntimeError as e:
    print(f"主异常: {e}")
    if e.__cause__:
        print(f"原始异常: {e.__cause__}")

# 重新抛出异常
print("\n--- 重新抛出异常 ---")

def outer():
    try:
        inner()
    except ValueError:
        print("在 outer 中重新抛出")
        raise

def inner():
    raise ValueError("来自 inner")

try:
    outer()
except ValueError as e:
    print(f"最终捕获: {e}")

# 断言
print("\n--- 断言 ---")
x = -1
# assert x >= 0, "x 必须非负"  # 取消注释会抛出 AssertionError

# 最佳实践：异常不用于控制流
print("\n--- 最佳实践 ---")

# 不好：用异常做流程控制
# try:
#     result = d["key"]
# except KeyError:
#     result = default_value

# 好：用 get
d = {"a": 1}
result = d.get("key", "默认值")
print(f"用 get 处理缺失: {result}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("示例执行完毕")
    print("=" * 50)

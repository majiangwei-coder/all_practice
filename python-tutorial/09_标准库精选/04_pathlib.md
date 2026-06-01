# pathlib 路径操作

## 为什么用 pathlib

更现代、更面向对象的路径操作，比 os.path 更直观：

```python
# 传统方式
import os
path = os.path.join("folder", "subfolder", "file.txt")

# pathlib 方式
from pathlib import Path
path = Path("folder") / "subfolder" / "file.txt"
```

## Path 对象

```python
from pathlib import Path

# 当前目录
p = Path(".")  # 当前位置
print(p)  # .

# 主目录
home = Path.home()
print(home)  # /home/user (Linux/Mac) 或 C:\Users\user (Windows)

# 当前工作目录
cwd = Path.cwd()
print(cwd)  # /current/working/directory
```

## 路径拼接

```python
from pathlib import Path

# / 运算符（推荐）
p = Path("folder") / "subfolder" / "file.txt"
print(p)  # folder/subfolder/file.txt

# joinpath 方法
p = Path("folder").joinpath("subfolder", "file.txt")

# + 拼接字符串（不推荐）
# p = "folder" + "/subfolder/file.txt"  # 错误方式
```

## 路径解析

```python
from pathlib import Path

p = Path("/home/user/docs/report.pdf")

p.name        # "report.pdf" (文件名)
p.stem       # "report" (无扩展名)
p.suffix     # ".pdf" (扩展名)
p.suffixes   # ['.pdf'] (多个扩展名如 .tar.gz)
p.parent     # Path("/home/user/docs") (父目录)
p.parents    # [<Path("/home/user/docs")>, <Path("/home/user")>, ...] (所有祖先)
p.anchor     # "/" (路径前缀)

# 文件名操作
p.with_name("new_name.pdf")  # 替换文件名
p.with_suffix(".txt")        # 替换扩展名
p.with_stem("newname")       # 替换 stem
```

## 绝对路径与相对路径

```python
from pathlib import Path

p = Path("folder/file.txt")

p.is_absolute()    # False
p.absolute()       # 转为绝对路径

# 解析相对路径
p = Path("folder/file.txt")
p.resolve()        # 转为绝对路径（会解析符号链接）
```

## 路径存在性检查

```python
from pathlib import Path

p = Path("file.txt")

p.exists()    # True/False
p.is_file()   # 是否是文件
p.is_dir()    # 是否是目录
p.is_symlink()  # 是否是符号链接
p.is_mount()     # 是否是挂载点（跨平台）
```

## 创建路径

```python
from pathlib import Path

# 创建目录
Path("new_folder").mkdir()           # 创建单层目录（父目录不存在会报错）
Path("new_folder").mkdir(parents=True)  # 创建多层目录
Path("new_folder").mkdir(parents=True, exist_ok=True)  # 存在不报错

# 创建文件（空文件）
Path("new_file.txt").touch()

# 创建符号链接
Path("link").symlink_to("target")
```

## 遍历目录

```python
from pathlib import Path

# iterdir：遍历目录内容
p = Path(".")
for item in p.iterdir():
    print(item.name)

# glob：模式匹配
for py_file in p.glob("*.py"):
    print(py_file)

# 递归 glob
for py_file in p.rglob("*.py"):  # 或 p.glob("**/*.py")
    print(py_file)

# 过滤
py_files = list(p.glob("*.py"))
readme = p.glob("README*")
```

## 读取与写入

```python
from pathlib import Path

# 读取文本
content = Path("file.txt").read_text(encoding="utf-8")

# 写入文本
Path("file.txt").write_text("Hello!", encoding="utf-8")

# 读取字节
data = Path("file.bin").read_bytes()

# 写入字节
Path("file.bin").write_bytes(b"\x00\x01\x02")
```

## 文件信息

```python
from pathlib import Path
import time

p = Path("file.txt")

# stat 信息
p.stat().st_size       # 文件大小（字节）
p.stat().st_mtime      # 修改时间（时间戳）
p.stat().st_ctime      # 创建时间（时间戳）
p.stat().st_mode       # 权限模式

# 人性化时间
from datetime import datetime
mtime = datetime.fromtimestamp(p.stat().st_mtime)
print(mtime.strftime("%Y-%m-%d %H:%M:%S"))
```

## 通配符模式

```python
from pathlib import Path

p = Path(".")

# * 任意字符
list(p.glob("*.txt"))      # 所有 .txt 文件
list(p.glob("*"))           # 所有内容

# ? 单个字符
list(p.glob("file?.txt"))   # file1.txt, file2.txt, ...

# [] 字符集
list(p.glob("file[123].txt"))  # file1.txt, file2.txt, file3.txt

# ** 任意目录深度
list(p.glob("**/*.py"))  # 递归所有 .py 文件
```

## 路径匹配

```python
from pathlib import Path

p = Path("/home/user/docs/report.pdf")

# match：路径是否匹配模式
p.match("*.pdf")       # True
p.match("*.txt")      # False
p.match("docs/*")     # True
p.match("/home/*")    # True
```

## Path 对象比较

```python
from pathlib import Path

p1 = Path("folder/file.txt")
p2 = Path("folder/file.txt")
p3 = Path("folder/./file.txt")

p1 == p2   # True (等价路径)
p1 == p3   # True (符号链接解析后相同)
p1.samefile(p2)  # True（检查是否指向同一文件）

# 排序
sorted(Path(".").glob("*"))  # 按名称排序
```

## 其他方法

```python
from pathlib import Path

p = Path("folder/file.txt")

# 重命名
p.rename("folder/new_name.txt")

# 移动
p.replace("new_location/file.txt")

# 删除
p.unlink()           # 删除文件
Path("folder").rmdir()  # 删除空目录（不递归）

# 复制（Python 3.8+ 无 copy，用 shutil）
import shutil
shutil.copy2("src.txt", "dst.txt")

# 复制目录树
shutil.copytree("src_folder", "dst_folder")
```

## 跨平台注意

```python
from pathlib import Path

# Windows vs Unix
# Windows: C:\Users\...
# Unix: /home/...

# PurePath vs Path
# PurePath: 不与系统交互，仅路径操作
# Path: 与系统交互（检查存在性等）

from pathlib import PurePath, Path
pp = PurePath("folder/file.txt")  # 纯字符串操作
```

## 实际应用

### 1. 查找项目中的 Python 文件

```python
from pathlib import Path

project_root = Path(".")
py_files = [
    f for f in project_root.rglob("*.py")
    if not any(part.startswith('.') for part in f.parts)
]
print(py_files)
```

### 2. 批量修改扩展名

```python
from pathlib import Path

for f in Path(".").glob("*.txt"):
    new_name = f.with_suffix(".md")
    f.rename(new_name)
```

### 3. 配置文件路径

```python
from pathlib import Path
import os

# 相对于模块文件的位置
CONFIG_DIR = Path(__file__).parent / "config"
config_file = CONFIG_DIR / "settings.json"
```

### 4. 临时文件

```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    temp_file = Path(tmpdir) / "temp.txt"
    temp_file.write_text("temporary data")
    print(temp_file.read_text())
```

## 小结

1. **Path 对象**：面向对象的路径表示，用 `/` 拼接
2. **属性**：name, stem, suffix, parent, parents, anchor
3. **exists/is_file/is_dir**：检查路径类型
4. **mkdir/touch**：创建目录和文件
5. **iterdir/glob/rglob**：遍历和搜索
6. **read_text/write_text**：读写文件
7. **stat**：获取文件信息
8. **rename/replace/unlink**：文件操作
9. **resolve/samefile**：路径解析和比较
10. **推荐用 pathlib**：比 os.path 更现代、更直观

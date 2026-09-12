# din.txt 二进制格式说明文档

本项目将 `din.txt` 中的 8,320 条字与代码映射记录转换为了高效的二进制文件。

## 文件清单
1. **din_table.bin** (全记录结构体二进制，推荐)
   - 每个字符/符号占用固定 16 字节（Little-Endian 小端序）：
     - `uint32` (4 字节): 字符的 Unicode 码点 (UTF-32)
     - `uint32` (4 字节): 原始第一列序号 ID (无序号记为 0)
     - `uint64` (8 字节): 第四列 DIN 码值 (数值最大达 58,705,510,514，采用 64 位无符号整型保证精度无损)
   - 总记录数：8,320 条，文件大小：133,120 字节。

2. **din_codes_only.bin** (纯代码流二进制)
   - 仅包含第四列 DIN 编码，每个编码占用 8 字节 (`uint64` Little-Endian)。
   - 总记录数：8,320 个，文件大小：66,560 字节。

## Python 读取示例 (读取 din_table.bin)
```python
import struct

records = []
with open("din_table.bin", "rb") as f:
    while chunk := f.read(16):
        unicode_cp, orig_id, din_code = struct.unpack("<IIQ", chunk)
        char = chr(unicode_cp)
        records.append((char, orig_id, din_code))

print(f"成功读取 {len(records)} 条记录")
print("示例记录:", records[:5])
```

# make_CTT.py
# 生成 CTT.csv = Chinese Token Table
# 查询 CJK 汉字在 o200k_base 中的 Token ID

from pathlib import Path
import csv
import subprocess
import sys
import unicodedata

ROOT = Path(r"C:\GTT\EnglishDB")
CSV_DIR = ROOT / "CSV"
OUT = CSV_DIR / "CTT.csv"

try:
    import tiktoken
except ImportError:
    print("Installing tiktoken...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tiktoken"])
    import tiktoken

ENCODING_NAME = "o200k_base"
enc = tiktoken.get_encoding(ENCODING_NAME)

# 先生成常用范围：基本汉字 + 扩展A + 兼容汉字
RANGES = [
    ("CJK Unified Ideographs", 0x4E00, 0x9FFF),
    ("CJK Extension A", 0x3400, 0x4DBF),
    ("CJK Compatibility Ideographs", 0xF900, 0xFAFF),
    ("CJK Extension B", 0x20000, 0x2A6DF),
    ("CJK Extension C", 0x2A700, 0x2B73F),
    ("CJK Extension D", 0x2B740, 0x2B81F),
    ("CJK Extension E", 0x2B820, 0x2CEAF),
    ("CJK Extension F", 0x2CEB0, 0x2EBEF),
    ("CJK Extension G", 0x30000, 0x3134F),
    ("CJK Extension H", 0x31350, 0x323AF),

]


def safe_name(ch):
    try:
        return unicodedata.name(ch)
    except ValueError:
        return ""

def main():
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    total = 0
    single = 0

    for block, start, end in RANGES:
        for code in range(start, end + 1):
            ch = chr(code)
            ids = enc.encode(ch)
            pieces = [enc.decode([i]) for i in ids]

            if len(ids) == 1:
                single += 1

            total += 1

            row = {
                "Char": ch,
                "Unicode": f"U+{code:04X}",
                "CodePoint": code,
                "Block": block,
                "Encoding": ENCODING_NAME,
                "TokenCount": len(ids),
                "SingleToken": "YES" if len(ids) == 1 else "NO",
                "TokenIDs": " ".join(map(str, ids)),
                "TokenPieces": " | ".join(pieces),
                "UnicodeName": safe_name(ch),
            }

            for i in range(6):
                row[f"Token{i+1}"] = ids[i] if i < len(ids) else ""
                row[f"Piece{i+1}"] = pieces[i] if i < len(pieces) else ""

            rows.append(row)

    fieldnames = [
        "Char", "Unicode", "CodePoint", "Block",
        "Encoding", "TokenCount", "SingleToken",
        "TokenIDs", "TokenPieces",
        "Token1", "Piece1",
        "Token2", "Piece2",
        "Token3", "Piece3",
        "Token4", "Piece4",
        "Token5", "Piece5",
        "Token6", "Piece6",
        "UnicodeName"
    ]

    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print("DONE")
    print("Output:", OUT)
    print("Characters:", total)
    print("Encoding:", ENCODING_NAME)
    print("Single token:", single)
    print("Multi token:", total - single)

if __name__ == "__main__":
    main()
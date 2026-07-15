# extract_roots.py
# 从 EnglishDB\Words\*\*.md 中提取“词根”行
# 输出：
#   C:\GTT\EnglishDB\CSV\GTT_Morphology.csv
#   C:\GTT\EnglishDB\CSV\GTT_Root.csv

from pathlib import Path
import re
import csv
from collections import Counter, defaultdict

ROOT = Path(r"C:\GTT\EnglishDB")
WORDS = ROOT / "Words"
CSV_DIR = ROOT / "CSV"

OUT_MORPH = CSV_DIR / "GTT_Morphology.csv"
OUT_ROOT = CSV_DIR / "GTT_Root.csv"

def clean_text(s):
    s = s.replace("＋", "+")
    s = s.replace("：", ":")
    s = s.replace("（", "(").replace("）", ")")
    s = s.replace("；", ";")
    s = s.replace("，", ",")
    return s.strip()

def extract_root_line(text):
    """
    寻找类似：
    词根: speci (看) + fic (做) + ation (名词后缀)
    词根：speci（看）+ fic（做）+ ation（名词后缀）
    """
    text = clean_text(text)

    for line in text.splitlines():
        line2 = clean_text(line)
        if "词根" in line2:
            # 去掉 markdown 加粗
            line2 = line2.replace("**", "")
            return line2

    return ""

def parse_parts(root_line):
    """
    从 root_line 中提取：
    speci (看)
    fic (做)
    ation (名词后缀)
    """
    if not root_line:
        return []

    if ":" in root_line:
        root_line = root_line.split(":", 1)[1]

    root_line = clean_text(root_line)

    parts = []

    # 主要格式：abc(中文)
    pattern = re.compile(r"([A-Za-z\-]+)\s*\(([^)]*)\)")
    for m in pattern.finditer(root_line):
        part = m.group(1).strip()
        meaning = m.group(2).strip()
        if part:
            parts.append((part, meaning))

    # 如果没有括号格式，尝试按 + 分割
    if not parts:
        chunks = [x.strip() for x in root_line.split("+") if x.strip()]
        for ch in chunks:
            m = re.match(r"([A-Za-z\-]+)", ch)
            if m:
                parts.append((m.group(1), ""))

    return parts

def guess_type(part, meaning):
    p = part.lower()
    m = meaning

    suffixes = [
        "tion", "sion", "ation", "ment", "ness", "ity",
        "able", "ible", "al", "ic", "ous", "ive",
        "er", "or", "ist", "ism", "ly", "ed", "ing"
    ]

    prefixes = [
        "un", "in", "im", "ir", "il", "re", "pre", "post",
        "anti", "auto", "bio", "micro", "macro", "sub",
        "super", "inter", "trans", "pro", "con", "com", "ex"
    ]

    if "后缀" in m or p in suffixes:
        return "suffix"
    if "前缀" in m or p in prefixes:
        return "prefix"
    return "root"

def main():
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    morph_rows = []
    root_counter = Counter()
    root_meanings = defaultdict(Counter)

    md_files = list(WORDS.rglob("*.md"))

    for md in md_files:
        word = md.stem

        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        root_line = extract_root_line(text)
        parts = parse_parts(root_line)

        if not parts:
            morph_rows.append({
                "Word": word,
                "MD": md.relative_to(ROOT).as_posix(),
                "RootLine": "",
                "PartIndex": "",
                "Part": "",
                "Type": "",
                "Meaning": "",
                "HasMorph": "NO"
            })
            continue

        for i, (part, meaning) in enumerate(parts, start=1):
            typ = guess_type(part, meaning)

            morph_rows.append({
                "Word": word,
                "MD": md.relative_to(ROOT).as_posix(),
                "RootLine": root_line,
                "PartIndex": i,
                "Part": part,
                "Type": typ,
                "Meaning": meaning,
                "HasMorph": "YES"
            })

            key = part.lower()
            root_counter[key] += 1
            if meaning:
                root_meanings[key][meaning] += 1

    with OUT_MORPH.open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "Word", "MD", "RootLine",
            "PartIndex", "Part", "Type",
            "Meaning", "HasMorph"
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(morph_rows)

    root_rows = []
    for root, count in root_counter.most_common():
        common_meaning = ""
        if root_meanings[root]:
            common_meaning = root_meanings[root].most_common(1)[0][0]

        root_rows.append({
            "Root": root,
            "Meaning": common_meaning,
            "Count": count
        })

    with OUT_ROOT.open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["Root", "Meaning", "Count"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(root_rows)

    print("DONE")
    print("MD files:", len(md_files))
    print("Morph rows:", len(morph_rows))
    print("Unique roots:", len(root_rows))
    print("Output:", OUT_MORPH)
    print("Output:", OUT_ROOT)

if __name__ == "__main__":
    main()
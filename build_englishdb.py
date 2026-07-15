from pathlib import Path
import re
import csv

INPUT = Path(r"C:\GTT\COCA2w.md")
OUT = Path(r"C:\GTT\EnglishDB")

WORDS = OUT / "Words"
CSV_DIR = OUT / "CSV"
INDEX_DIR = OUT / "Index"
IMAGES_DIR = OUT / "Images"
GTT_DIR = OUT / "GTT"

for p in [WORDS, CSV_DIR, INDEX_DIR, IMAGES_DIR, GTT_DIR]:
    p.mkdir(parents=True, exist_ok=True)

def clean_pandoc(s):
    return (s.replace(r"\##", "##")
             .replace(r"\###", "###")
             .replace(r"\+", "+")
             .replace(r"\*", "*")
             .replace(r"\_", "_")
             .replace(r"\>", ">")
             .replace(r"\!", "!")
             .replace(r"\[", "[")
             .replace(r"\]", "]"))

def safe_name(word):
    return re.sub(r"[^a-z0-9_-]", "_", word.lower()) or "unknown"

def folder_of(word):
    c = word[:1].lower()
    return c if "a" <= c <= "z" else "_"

def parse_block(word, text, idx):
    uk = ""
    us = ""
    meaning = ""
    image = ""

    m = re.search(r"\*\*英音:\*\*\s*_\[(.*?)\]_", text)
    if m:
        uk = m.group(1)

    m = re.search(r"\*\*美音:\*\*\s*_\[(.*?)\]_", text)
    if m:
        us = m.group(1)

    m = re.search(r"\*\*译义:\*\*\s*\*(.*?)\*", text, re.S)
    if m:
        meaning = " ".join(m.group(1).split())

    m = re.search(r"!\[(.*?)\]\((.*?)\)", text)
    if m:
        image = m.group(2)

    pos = ""
    m = re.match(r"([a-z]+\.)", meaning)
    if m:
        pos = m.group(1)

    return {
        "id": f"{idx:06d}",
        "word": word,
        "uk": uk,
        "us": us,
        "meaning": meaning,
        "pos": pos,
        "image": image
    }

def extract_phrases(word, text, idx):
    rows = []
    for m in re.finditer(r"\+\s+\*\*(.*?):\*\*\s*_(.*?)_", text):
        rows.append([idx, word, m.group(1).strip(), m.group(2).strip()])
    return rows

def extract_examples(word, text, idx):
    rows = []
    pattern = re.compile(
        r"#### 例句(\d+).*?> \*\*(.*?)\*\*.*?\*\*中文翻译:\*\*\s*(.*?)(?:\n\n|\r\n\r\n).*?\*\*单词释义:\*\*\s*(.*?)(?:\n\n|###)",
        re.S
    )
    for m in pattern.finditer(text):
        rows.append([
            idx,
            word,
            m.group(1).strip(),
            " ".join(m.group(2).split()),
            " ".join(m.group(3).split()),
            " ".join(m.group(4).split())
        ])
    return rows

def extract_story(word, text, idx):
    m = re.search(r"### 背诵小故事(.*?)(?:### 图义|$)", text, re.S)
    if not m:
        return ""
    return " ".join(m.group(1).split())

def save_word_md(meta, text):
    word = meta["word"]
    folder = WORDS / folder_of(word)
    folder.mkdir(exist_ok=True)

    file = folder / f"{safe_name(word)}.md"

    yaml = f"""---
id: {meta['id']}
word: {word}
lemma: {word}
pos: {meta['pos']}
uk: "{meta['uk']}"
us: "{meta['us']}"
source: COCA2w
---

"""
    file.write_text(yaml + text.strip() + "\n", encoding="utf-8")
    return file

rows_words = []
rows_phrases = []
rows_examples = []
rows_stories = []
rows_images = []
rows_gtt = []
letter_index = {}

current_word = None
buffer = []
count = 0

def finish_word(word, lines):
    global count

    if not word:
        return

    raw = "".join(lines)
    text = clean_pandoc(raw)

    count += 1
    meta = parse_block(word, text, count)
    file = save_word_md(meta, text)

    rows_words.append([
        meta["id"], word, meta["pos"], meta["uk"], meta["us"],
        meta["meaning"], str(file)
    ])

    rows_phrases.extend(extract_phrases(word, text, meta["id"]))
    rows_examples.extend(extract_examples(word, text, meta["id"]))

    story = extract_story(word, text, meta["id"])
    if story:
        rows_stories.append([meta["id"], word, story])

    if meta["image"]:
        rows_images.append([meta["id"], word, meta["image"]])

    rows_gtt.append([meta["id"], word, meta["pos"], folder_of(word)])

    letter = folder_of(word).upper()
    letter_index.setdefault(letter, []).append((word, file))

    if count % 1000 == 0:
        print("已处理", count, "个词条")

with INPUT.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        s = line.lstrip("\ufeff ").rstrip()

        if s.startswith(r"\## ") and not s.startswith(r"\### "):
            finish_word(current_word, buffer)
            title = s.replace(r"\##", "##", 1)
            current_word = title[3:].strip().split()[0]
            buffer = [line]
        elif s.startswith("## ") and not s.startswith("### "):
            finish_word(current_word, buffer)
            current_word = s[3:].strip().split()[0]
            buffer = [line]
        else:
            buffer.append(line)

finish_word(current_word, buffer)

def write_csv(name, header, rows):
    path = CSV_DIR / name
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

write_csv("words.csv",
          ["id", "word", "pos", "uk", "us", "meaning", "file"],
          rows_words)

write_csv("phrases.csv",
          ["id", "word", "phrase", "meaning"],
          rows_phrases)

write_csv("examples.csv",
          ["id", "word", "example_no", "sentence", "translation", "word_meaning"],
          rows_examples)

write_csv("stories.csv",
          ["id", "word", "story"],
          rows_stories)

write_csv("images.csv",
          ["id", "word", "image_url"],
          rows_images)

with (GTT_DIR / "token.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["gtt_id", "word", "pos", "group"])
    w.writerows(rows_gtt)

# 生成 Obsidian 总目录
index_lines = ["# EnglishDB 总目录\n\n", f"共 {count} 个词条。\n\n"]

for letter in sorted(letter_index.keys()):
    index_lines.append(f"## {letter}\n\n")
    letter_file = INDEX_DIR / f"{letter}.md"
    sub_lines = [f"# {letter} 词条\n\n"]

    for word, file in letter_index[letter]:
        rel = file.relative_to(OUT).as_posix()
        index_lines.append(f"- [{word}](../{rel})\n")
        sub_lines.append(f"- [{word}](../{rel})\n")

    index_lines.append("\n")
    letter_file.write_text("".join(sub_lines), encoding="utf-8")

(INDEX_DIR / "index.md").write_text("".join(index_lines), encoding="utf-8")

print("完成！")
print("词条数：", count)
print("Words：", WORDS)
print("CSV：", CSV_DIR)
print("Index：", INDEX_DIR)
print("GTT：", GTT_DIR)
# -*- coding:
# -*- coding: utf-8 -*-
from pathlib import Path
import re

WORDS_DIR = Path(r"C:\GTT\EnglishDB\Words")
OUT_DIR = Path(r"C:\ETT")
OUT_FILE = OUT_DIR / "EnglishDB_Words_ALL.md"

OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_word_key(path):
    return path.stem.lower()

def clean_md(text):
    text = text.replace("\ufeff", "")
    return text.strip()

def main():
    files = sorted(WORDS_DIR.rglob("*.md"), key=get_word_key)

    with OUT_FILE.open("w", encoding="utf-8", newline="\n") as out:
        out.write("# EnglishDB Words ALL\n\n")
        out.write(f"Source: `{WORDS_DIR}`\n\n")
        out.write(f"Total files: {len(files)}\n\n")
        out.write("---\n\n")

        for i, path in enumerate(files, 1):
            try:
                text = path.read_text(encoding="utf-8-sig")
            except Exception as e:
                print("FAILED:", path, e)
                continue

            word = path.stem
            rel = path.relative_to(WORDS_DIR)

            out.write(f"\n\n<!-- FILE: {rel} -->\n\n")
            out.write(f"# {word}\n\n")
            out.write(clean_md(text))
            out.write("\n\n---\n")

            if i % 1000 == 0:
                print("Merged:", i)

    print("DONE")
    print("Files:", len(files))
    print("Output:", OUT_FILE)

if __name__ == "__main__":
    main()
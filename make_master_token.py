from pathlib import Path
import csv

ROOT = Path(r"C:\GTT\EnglishDB")
WORDS = ROOT / "Words"
IMAGES = ROOT / "Images"
CSV_DIR = ROOT / "CSV"
OUT = CSV_DIR / "GTT_MasterToken.csv"

IMG_EXTS = [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"]

def find_image(word):
    for ext in IMG_EXTS:
        p = IMAGES / f"{word}{ext}"
        if p.exists():
            return p.relative_to(ROOT).as_posix()
    return ""

def main():
    CSV_DIR.mkdir(exist_ok=True)

    rows = []
    token_id = 1

    for letter in "abcdefghijklmnopqrstuvwxyz":
        folder = WORDS / letter
        if not folder.exists():
            continue

        for md in sorted(folder.glob("*.md")):
            word = md.stem
            image = find_image(word)

            rows.append({
                "TokenID": token_id,
                "Word": word,
                "FirstLetter": letter,
                "Length": len(word),
                "MD": md.relative_to(ROOT).as_posix(),
                "Image": image,
                "HasImage": "YES" if image else "NO",
                "GTT": "",
                "Frequency": "",
                "POS": "",
                "Chinese": ""
            })

            token_id += 1

    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=[
            "TokenID", "Word", "FirstLetter", "Length",
            "MD", "Image", "HasImage",
            "GTT", "Frequency", "POS", "Chinese"
        ])
        w.writeheader()
        w.writerows(rows)

    print("完成！")
    print("词条数：", len(rows))
    print("输出：", OUT)

if __name__ == "__main__":
    main()
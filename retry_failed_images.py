from pathlib import Path
import csv
import urllib.request
import ssl
import time

FAILED = Path(r"C:\GTT\EnglishDB\CSV\failed_images.csv")
IMG_DIR = Path(r"C:\GTT\EnglishDB\Images")
NEW_FAILED = Path(r"C:\GTT\EnglishDB\CSV\failed_images_retry.csv")

IMG_DIR.mkdir(parents=True, exist_ok=True)

# 临时忽略网站证书过期
CTX = ssl._create_unverified_context()

def safe_filename(word, url):
    ext = url.split("?")[0].split(".")[-1].lower()
    if ext not in ["svg", "png", "jpg", "jpeg", "webp"]:
        ext = "svg"
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in word.lower())
    return f"{safe}.{ext}"

def download(url, out_file):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        data = r.read()
    out_file.write_bytes(data)

rows = []
with FAILED.open("r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

ok = 0
skip = 0
fail = []

for i, row in enumerate(rows, 1):
    word = row["word"].strip()
    url = row["url"].strip()
    out_file = IMG_DIR / safe_filename(word, url)

    if out_file.exists() and out_file.stat().st_size > 0:
        skip += 1
        continue

    try:
        download(url, out_file)
        ok += 1
        print(f"{i}/{len(rows)} 成功：{word}")
    except Exception as e:
        fail.append([row["id"], word, url, str(e)])
        print(f"{i}/{len(rows)} 失败：{word} {e}")
        time.sleep(1)

with NEW_FAILED.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "word", "url", "error"])
    w.writerows(fail)

print("重试完成")
print("成功：", ok)
print("跳过：", skip)
print("仍失败：", len(fail))
print("新失败表：", NEW_FAILED)
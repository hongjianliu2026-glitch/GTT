from pathlib import Path
import csv
import urllib.request
import urllib.error
import time

CSV_FILE = Path(r"C:\GTT\EnglishDB\CSV\images.csv")
IMG_DIR = Path(r"C:\GTT\EnglishDB\Images")
FAILED_FILE = Path(r"C:\GTT\EnglishDB\CSV\failed_images.csv")

IMG_DIR.mkdir(parents=True, exist_ok=True)

def filename_from_url(word, url):
    ext = url.split("?")[0].split(".")[-1].lower()
    if ext not in ["svg", "png", "jpg", "jpeg", "webp"]:
        ext = "svg"
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in word.lower())
    return f"{safe}.{ext}"

def download(url, out_file):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    out_file.write_bytes(data)

rows = []
with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

total = len(rows)
ok = 0
skip = 0
fail = []

print("准备下载图片数量：", total)

for i, row in enumerate(rows, 1):
    word = row.get("word", "").strip()
    url = row.get("image_url", "").strip()

    if not word or not url:
        continue

    out_file = IMG_DIR / filename_from_url(word, url)

    if out_file.exists() and out_file.stat().st_size > 0:
        skip += 1
        if i % 500 == 0:
            print(f"{i}/{total} 已存在，跳过")
        continue

    success = False

    for attempt in range(3):
        try:
            download(url, out_file)
            ok += 1
            success = True
            break
        except Exception as e:
            err = str(e)
            time.sleep(1)

    if not success:
        fail.append([row.get("id", ""), word, url, err])

    if i % 100 == 0:
        print(f"进度 {i}/{total} 下载成功 {ok} 跳过 {skip} 失败 {len(fail)}")

with FAILED_FILE.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "word", "url", "error"])
    w.writerows(fail)

print("完成！")
print("成功下载：", ok)
print("已存在跳过：", skip)
print("失败：", len(fail))
print("图片目录：", IMG_DIR)
print("失败记录：", FAILED_FILE)
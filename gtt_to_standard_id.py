from pathlib import Path
import csv
import tiktoken

MAP_FILE = Path(r"C:\GTT\EnglishDB\CSV\GTT_Map.csv")
OUT_FILE = Path(r"C:\GTT\EnglishDB\CSV\GTT_to_o200k.csv")

enc = tiktoken.get_encoding("o200k_base")

rows = []

with MAP_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for r in reader:
        gtt_id = r.get("GTT_ID", "").strip()
        gtt_char = r.get("GTT_CHAR", "").strip()
        word = r.get("WORD", "").strip()

        ids = enc.encode(word)

        rows.append({
            "GTT_ID": gtt_id,
            "GTT_CHAR": gtt_char,
            "WORD": word,
            "StandardEncoding": "o200k_base",
            "StandardTokenIDs": " ".join(map(str, ids)),
            "StandardTokenCount": len(ids)
        })

with OUT_FILE.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=[
        "GTT_ID",
        "GTT_CHAR",
        "WORD",
        "StandardEncoding",
        "StandardTokenIDs",
        "StandardTokenCount"
    ])
    w.writeheader()
    w.writerows(rows)

print("DONE")
print("Output:", OUT_FILE)
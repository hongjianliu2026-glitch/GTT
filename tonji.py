from pathlib import Path

root = Path(r"C:\GTT\EnglishDB\Words")

total = 0

for ch in "abcdefghijklmnopqrstuvwxyz":
    d = root / ch
    if d.exists():
        n = len(list(d.glob("*.md")))
        total += n
        print(f"{ch.upper():2} {n:5}")

print("-" * 20)
print("TOTAL", total)
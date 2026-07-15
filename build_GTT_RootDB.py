# build_GTT_RootDB.py
# 为 EnglishDB 生成基础构词数据库
# 输入：C:\GTT\EnglishDB\Words\*\*.md
# 输出：
#   GTT_Morphology.csv
#   GTT_Root.csv
#   GTT_Prefix.csv
#   GTT_Suffix.csv

from pathlib import Path
import csv
from collections import Counter, defaultdict

ROOT = Path(r"C:\GTT\EnglishDB")
WORDS_DIR = ROOT / "Words"
CSV_DIR = ROOT / "CSV"

OUT_MORPH = CSV_DIR / "GTT_Morphology.csv"
OUT_ROOT = CSV_DIR / "GTT_Root.csv"
OUT_PREFIX = CSV_DIR / "GTT_Prefix.csv"
OUT_SUFFIX = CSV_DIR / "GTT_Suffix.csv"

PREFIXES = {
    "anti":"反", "auto":"自", "bio":"生命", "co":"共同", "com":"共同", "con":"共同",
    "de":"下/去", "dis":"不/分离", "en":"使", "ex":"出/前", "extra":"外",
    "hyper":"过度", "il":"不", "im":"不", "in":"不/入", "inter":"之间",
    "intra":"内部", "ir":"不", "macro":"大", "micro":"小", "mis":"错",
    "mono":"单", "multi":"多", "non":"不", "over":"过度", "post":"后",
    "pre":"前", "pro":"向前", "re":"再/回", "semi":"半", "sub":"下",
    "super":"上/超", "trans":"横过", "tri":"三", "un":"不", "under":"下"
}

SUFFIXES = {
    "ability":"能力", "able":"可", "al":"形容词/名词后缀", "ance":"名词后缀",
    "ant":"人/物", "ary":"有关", "ation":"名词后缀", "ed":"过去/形容词",
    "ence":"名词后缀", "ent":"人/物", "er":"人/比较级", "ful":"充满",
    "hood":"状态", "ible":"可", "ic":"形容词后缀", "ical":"形容词后缀",
    "ing":"进行/名词", "ion":"名词后缀", "ism":"主义", "ist":"人",
    "ity":"性质", "ive":"形容词后缀", "ize":"使成为", "less":"无",
    "ly":"副词后缀", "ment":"名词后缀", "ness":"性质", "or":"人/物",
    "ous":"充满", "ship":"关系/状态", "sion":"名词后缀", "tion":"名词后缀",
    "ty":"性质", "ure":"名词后缀", "y":"形容词/名词后缀"
}

ROOTS = {
    "act":"做", "anim":"生命", "aud":"听", "auto":"自", "bio":"生命",
    "cap":"抓/取", "cede":"走", "ceed":"走", "cess":"走",
    "chron":"时间", "cid":"落/切", "cis":"切", "cred":"信",
    "dict":"说", "duc":"引导", "duct":"引导", "fac":"做", "fact":"做",
    "fect":"做", "fic":"做", "form":"形", "graph":"写/画",
    "ject":"投", "log":"说/学", "man":"手", "meter":"测量",
    "mit":"送", "miss":"送", "mot":"动", "mov":"动", "path":"感",
    "phon":"声", "photo":"光", "port":"搬运", "pos":"放",
    "press":"压", "rupt":"破", "scrib":"写", "script":"写",
    "sect":"切", "spect":"看", "spec":"看", "spic":"看",
    "struct":"建造", "tele":"远", "tract":"拉", "vid":"看",
    "vis":"看", "voc":"声/叫", "volv":"卷"
}

def split_word(word):
    w = word.lower()
    original = w
    parts = []

    # prefix: 取最长匹配
    for p in sorted(PREFIXES, key=len, reverse=True):
        if w.startswith(p) and len(w) > len(p) + 2:
            parts.append(("prefix", p, PREFIXES[p]))
            w = w[len(p):]
            break

    # suffix: 取最长匹配
    suffix_found = None
    for s in sorted(SUFFIXES, key=len, reverse=True):
        if w.endswith(s) and len(w) > len(s) + 2:
            suffix_found = ("suffix", s, SUFFIXES[s])
            w = w[:-len(s)]
            break

    # root: 在剩余部分中找已知词根
    root_hits = []
    for r in sorted(ROOTS, key=len, reverse=True):
        if r in w:
            root_hits.append(("root", r, ROOTS[r]))
            break

    if root_hits:
        parts.extend(root_hits)
    elif w and w != original:
        parts.append(("stem", w, ""))

    if suffix_found:
        parts.append(suffix_found)

    if not parts:
        parts.append(("word", original, ""))

    return parts

def main():
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    morph_rows = []
    root_counter = Counter()
    prefix_counter = Counter()
    suffix_counter = Counter()
    root_words = defaultdict(list)

    md_files = sorted(WORDS_DIR.rglob("*.md"))

    for md in md_files:
        word = md.stem
        parts = split_word(word)

        for i, (typ, part, meaning) in enumerate(parts, 1):
            morph_rows.append({
                "Word": word,
                "MD": md.relative_to(ROOT).as_posix(),
                "PartIndex": i,
                "Part": part,
                "Type": typ,
                "Meaning": meaning
            })

            if typ == "root":
                root_counter[part] += 1
                root_words[part].append(word)
            elif typ == "prefix":
                prefix_counter[part] += 1
            elif typ == "suffix":
                suffix_counter[part] += 1

    with OUT_MORPH.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "Word", "MD", "PartIndex", "Part", "Type", "Meaning"
        ])
        w.writeheader()
        w.writerows(morph_rows)

    with OUT_ROOT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "Root", "Meaning", "Count", "ExampleWords"
        ])
        w.writeheader()
        for r, c in root_counter.most_common():
            w.writerow({
                "Root": r,
                "Meaning": ROOTS.get(r, ""),
                "Count": c,
                "ExampleWords": " ".join(root_words[r][:20])
            })

    with OUT_PREFIX.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Prefix", "Meaning", "Count"])
        w.writeheader()
        for p, c in prefix_counter.most_common():
            w.writerow({"Prefix": p, "Meaning": PREFIXES[p], "Count": c})

    with OUT_SUFFIX.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Suffix", "Meaning", "Count"])
        w.writeheader()
        for s, c in suffix_counter.most_common():
            w.writerow({"Suffix": s, "Meaning": SUFFIXES[s], "Count": c})

    print("DONE")
    print("MD files:", len(md_files))
    print("Morph rows:", len(morph_rows))
    print("Roots:", len(root_counter))
    print("Prefixes:", len(prefix_counter))
    print("Suffixes:", len(suffix_counter))
    print("Output:", CSV_DIR)

if __name__ == "__main__":
    main()
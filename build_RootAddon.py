# -*- coding: utf-8 -*-
"""
build_RootAddon.py
词根外挂脚本

功能：
1. 自动建立 C:\GTT\EnglishDB\CSV\RootAddon.csv
2. 内置一批常用英语词根
3. 读取旧 RootDB.csv
4. 合并去重
5. 输出 RootDB_PLUS.csv

运行：
    cd /d C:\GTT
    python build_RootAddon.py
"""

import csv
from pathlib import Path

BASE = Path(r"C:\GTT")
CSV_DIR = BASE / "EnglishDB" / "CSV"

OLD_ROOT = CSV_DIR / "RootDB.csv"
ADDON_ROOT = CSV_DIR / "RootAddon.csv"
OUT_ROOT = CSV_DIR / "RootDB_PLUS.csv"

CSV_DIR.mkdir(parents=True, exist_ok=True)

# 词根外挂：root, meaning_cn, meaning_en, examples
ROOT_ADDON = [
    ("act", "做；行动", "do, act", "action, active, actor"),
    ("ag", "做；驱动", "do, drive", "agent, agenda"),
    ("anim", "生命；精神", "life, spirit", "animal, animation"),
    ("ann", "年", "year", "annual, anniversary"),
    ("anthrop", "人类", "human", "anthropology"),
    ("audi", "听", "hear", "audio, audience"),
    ("auto", "自己", "self", "automatic, autobiography"),
    ("bio", "生命", "life", "biology, biography"),
    ("brev", "短", "short", "brief, abbreviate"),
    ("cap", "拿；头", "take, head", "capture, capital"),
    ("capt", "拿；抓", "take, seize", "capture, captive"),
    ("ced", "走；让步", "go, yield", "cede, precede"),
    ("cede", "走；让步", "go, yield", "precede, recede"),
    ("ceed", "走", "go", "proceed, exceed"),
    ("cess", "走", "go", "process, access"),
    ("chron", "时间", "time", "chronology, chronic"),
    ("cid", "切；杀", "cut, kill", "decide, homicide"),
    ("cise", "切", "cut", "incise, concise"),
    ("clam", "喊", "cry out", "exclaim, proclaim"),
    ("clar", "清楚；明亮", "clear, bright", "clear, clarify"),
    ("clud", "关闭", "shut", "include, exclude"),
    ("clus", "关闭", "shut", "conclusion, exclusive"),
    ("cogn", "知道", "know", "recognize, cognition"),
    ("cord", "心", "heart", "cordial, accord"),
    ("corp", "身体", "body", "corporation, corpse"),
    ("cred", "相信", "believe", "credit, credible"),
    ("cur", "跑；流", "run", "current, occur"),
    ("curr", "跑；流", "run", "current, curriculum"),
    ("cycl", "圆；环", "circle", "cycle, bicycle"),
    ("dem", "人民", "people", "democracy, epidemic"),
    ("dict", "说", "say", "dictate, predict"),
    ("duc", "引导", "lead", "produce, educate"),
    ("duct", "引导", "lead", "conduct, product"),
    ("fac", "做", "make, do", "factory, facilitate"),
    ("fact", "做", "make, do", "fact, manufacture"),
    ("fer", "带来；承载", "carry, bring", "transfer, refer"),
    ("fid", "信任", "faith, trust", "fidelity, confidence"),
    ("fin", "结束；边界", "end, limit", "final, define"),
    ("form", "形状", "shape", "form, reform"),
    ("fract", "破", "break", "fraction, fracture"),
    ("gen", "生；产生", "birth, produce", "generate, gene"),
    ("grad", "步；级", "step, degree", "grade, gradual"),
    ("graph", "写；画", "write, draw", "graph, photograph"),
    ("gress", "走", "go, step", "progress, regress"),
    ("ject", "投；扔", "throw", "project, reject"),
    ("jud", "判断", "judge", "judge, judicial"),
    ("jur", "法律；誓言", "law, oath", "jury, jurisdiction"),
    ("leg", "法律；读；派遣", "law, read, send", "legal, legend"),
    ("log", "言；理；学", "word, reason, study", "logic, biology"),
    ("luc", "光", "light", "lucid, translucent"),
    ("magn", "大", "great", "magnify, magnificent"),
    ("man", "手", "hand", "manual, manage"),
    ("manu", "手", "hand", "manual, manufacture"),
    ("mater", "母；材料", "mother, matter", "maternal, material"),
    ("memor", "记忆", "memory", "memory, memorial"),
    ("micro", "小", "small", "microphone, microscope"),
    ("mit", "送", "send", "submit, transmit"),
    ("miss", "送", "send", "mission, dismiss"),
    ("mob", "动", "move", "mobile, automobile"),
    ("mot", "动", "move", "motion, promote"),
    ("mov", "动", "move", "move, remove"),
    ("nat", "生", "birth", "native, natural"),
    ("nom", "名；法则", "name, rule", "nominate, astronomy"),
    ("nov", "新", "new", "novel, innovate"),
    ("onym", "名", "name", "synonym, anonymous"),
    ("path", "感情；疾病", "feeling, disease", "sympathy, pathology"),
    ("ped", "脚；儿童", "foot, child", "pedal, pediatric"),
    ("pend", "悬挂", "hang", "depend, suspend"),
    ("phon", "声音", "sound", "phone, phonetic"),
    ("photo", "光", "light", "photo, photograph"),
    ("port", "携带", "carry", "transport, import"),
    ("pos", "放置", "put, place", "position, compose"),
    ("press", "压", "press", "pressure, compress"),
    ("rupt", "破裂", "break", "rupture, interrupt"),
    ("scrib", "写", "write", "describe, scribble"),
    ("script", "写", "write", "script, manuscript"),
    ("sect", "切", "cut", "section, dissect"),
    ("sens", "感觉", "feel", "sense, sensitive"),
    ("sent", "感觉；送", "feel, send", "sentiment, consent"),
    ("serv", "服务；保存", "serve, keep", "service, preserve"),
    ("sign", "标记", "mark, sign", "signal, design"),
    ("spec", "看", "look, see", "inspect, specification"),
    ("spect", "看", "look, see", "respect, spectator"),
    ("spir", "呼吸", "breathe", "spirit, inspire"),
    ("stat", "站；状态", "stand", "state, station"),
    ("struct", "建造", "build", "structure, construct"),
    ("tain", "持有", "hold", "contain, retain"),
    ("tect", "覆盖；建造", "cover, build", "protect, architecture"),
    ("temp", "时间", "time", "temporary, contemporary"),
    ("term", "边界；期限", "limit, end", "term, terminal"),
    ("tract", "拉", "draw, pull", "attract, subtract"),
    ("ven", "来", "come", "event, convenient"),
    ("vert", "转", "turn", "convert, reverse"),
    ("vid", "看", "see", "video, evidence"),
    ("vis", "看", "see", "vision, visible"),
    ("voc", "声音；叫", "voice, call", "vocal, vocabulary"),
    ("vol", "意志；卷；飞", "will, roll, fly", "voluntary, volume"),
]


def read_csv_rows(path):
    if not path.exists():
        return []

    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def write_addon():
    with open(ADDON_ROOT, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["root", "meaning_cn", "meaning_en", "examples", "source"])
        for root, cn, en, examples in ROOT_ADDON:
            writer.writerow([root, cn, en, examples, "addon"])


def normalize_old_rows(rows):
    """
    兼容不同旧表字段。
    如果旧 RootDB.csv 字段不同，也尽量转成统一格式。
    """
    out = []

    for r in rows:
        root = (
            r.get("root")
            or r.get("Root")
            or r.get("word")
            or r.get("morph")
            or ""
        ).strip()

        if not root:
            continue

        cn = (
            r.get("meaning_cn")
            or r.get("meaning")
            or r.get("cn")
            or r.get("中文")
            or ""
        ).strip()

        en = (
            r.get("meaning_en")
            or r.get("en")
            or r.get("english")
            or ""
        ).strip()

        examples = (
            r.get("examples")
            or r.get("example")
            or r.get("words")
            or ""
        ).strip()

        out.append({
            "root": root.lower(),
            "meaning_cn": cn,
            "meaning_en": en,
            "examples": examples,
            "source": "old"
        })

    return out


def addon_rows():
    return [
        {
            "root": root.lower(),
            "meaning_cn": cn,
            "meaning_en": en,
            "examples": examples,
            "source": "addon"
        }
        for root, cn, en, examples in ROOT_ADDON
    ]


def merge_roots(old_rows, addon):
    """
    合并规则：
    1. root 相同则合并
    2. 中文义项、英文义项、例词尽量保留
    3. source 标记 old+addon
    """
    db = {}

    for row in old_rows + addon:
        root = row["root"].strip().lower()
        if not root:
            continue

        if root not in db:
            db[root] = row.copy()
        else:
            old = db[root]

            for key in ["meaning_cn", "meaning_en", "examples"]:
                a = old.get(key, "").strip()
                b = row.get(key, "").strip()

                if not a:
                    old[key] = b
                elif b and b not in a:
                    old[key] = a + "；" + b

            src = old.get("source", "")
            new_src = row.get("source", "")
            if new_src and new_src not in src:
                old["source"] = src + "+" + new_src

    return sorted(db.values(), key=lambda x: x["root"])


def write_root_plus(rows):
    with open(OUT_ROOT, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["root", "meaning_cn", "meaning_en", "examples", "source"]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    write_addon()

    old_raw = read_csv_rows(OLD_ROOT)
    old = normalize_old_rows(old_raw)
    addon = addon_rows()

    merged = merge_roots(old, addon)
    write_root_plus(merged)

    print("DONE")
    print("Old RootDB:", OLD_ROOT)
    print("Addon:", ADDON_ROOT)
    print("Output:", OUT_ROOT)
    print("Old roots:", len(old))
    print("Addon roots:", len(addon))
    print("Merged roots:", len(merged))


if __name__ == "__main__":
    main()
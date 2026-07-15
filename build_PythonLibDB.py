import csv
import sys
import os
import importlib.util
from pathlib import Path
from importlib.metadata import distributions, version, PackageNotFoundError

BASE = Path(r"C:\GTT")
CSV_OUT = BASE / "PythonLibDB.csv"
MD_OUT = BASE / "PythonLibDB.md"


def safe_version(pkg_name):
    try:
        return version(pkg_name)
    except PackageNotFoundError:
        return ""


def guess_import_name(pkg_name):
    return pkg_name.replace("-", "_").replace(".", "_")


def find_module_info(import_name):
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            return False, ""

        if spec.origin and spec.origin != "built-in":
            return True, spec.origin

        if spec.submodule_search_locations:
            return True, ";".join(str(p) for p in spec.submodule_search_locations)

        return True, str(spec.origin)
    except Exception:
        return False, ""


def get_dir_size_and_files(path_text):
    if not path_text:
        return 0, 0

    first_path = path_text.split(";")[0]
    p = Path(first_path)

    if p.is_file():
        p = p.parent

    if not p.exists():
        return 0, 0

    total_size = 0
    total_files = 0

    try:
        for root, dirs, files in os.walk(p):
            for name in files:
                fp = Path(root) / name
                try:
                    total_size += fp.stat().st_size
                    total_files += 1
                except Exception:
                    pass
    except Exception:
        pass

    return round(total_size / 1024 / 1024, 3), total_files


def get_summary(dist):
    try:
        return dist.metadata.get("Summary", "")
    except Exception:
        return ""


def main():
    BASE.mkdir(parents=True, exist_ok=True)

    rows = []
    seen = set()

    for dist in distributions():
        pkg_name = dist.metadata.get("Name", "")
        if not pkg_name:
            continue

        key = pkg_name.lower()
        if key in seen:
            continue
        seen.add(key)

        import_name = guess_import_name(pkg_name)
        ok, path = find_module_info(import_name)
        size_mb, file_count = get_dir_size_and_files(path)

        rows.append({
            "package": pkg_name,
            "version": safe_version(pkg_name),
            "import_name_guess": import_name,
            "import_ok": "YES" if ok else "NO",
            "module_path": path,
            "size_mb": size_mb,
            "file_count": file_count,
            "summary": get_summary(dist),
        })

    rows.sort(key=lambda x: x["package"].lower())

    with CSV_OUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "package",
                "version",
                "import_name_guess",
                "import_ok",
                "module_path",
                "size_mb",
                "file_count",
                "summary",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    with MD_OUT.open("w", encoding="utf-8-sig") as f:
        f.write("# PythonLibDB\n\n")
        f.write(f"- Python: `{sys.version}`\n")
        f.write(f"- Executable: `{sys.executable}`\n")
        f.write(f"- Packages: **{len(rows)}**\n\n")

        f.write("| Package | Version | Import | OK | Size MB | Files | Summary |\n")
        f.write("|---|---:|---|---|---:|---:|---|\n")

        for r in rows:
            summary = str(r["summary"]).replace("|", "/")
            f.write(
                f"| {r['package']} | {r['version']} | "
                f"`{r['import_name_guess']}` | {r['import_ok']} | "
                f"{r['size_mb']} | {r['file_count']} | {summary} |\n"
            )

    print("DONE")
    print("Python:", sys.version)
    print("Executable:", sys.executable)
    print("CSV:", CSV_OUT)
    print("MD:", MD_OUT)
    print("Packages:", len(rows))


if __name__ == "__main__":
    main()
"""Search archive member text in memory; never unpack or execute project code."""
from pathlib import Path
from collections import Counter
from bisect import bisect_right
import csv
import hashlib
import json
import re
import subprocess
import zipfile

from scan_workspace_database import ROOT, OUT, PATTERNS, decode


def main():
    manifest = json.loads((OUT / "inventory.json").read_text(encoding="utf-8"))
    records = []
    patterns = {name: re.compile(pattern, re.I) for name, pattern in PATTERNS.items()}
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if path.suffix.lower() not in {".zip", ".rar"}:
            continue
        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as archive:
                members = [(i.filename, archive.read(i)) for i in archive.infolist() if not i.is_dir()]
        else:
            listing = subprocess.run(["tar", "-tf", str(path)], capture_output=True, check=True)
            names = listing.stdout.decode("utf-8").splitlines()
            members = []
            for name in names:
                # The inspected RAR has two files and one directory entry.
                if not Path(name).suffix:
                    continue
                result = subprocess.run(["tar", "-xOf", str(path), "--", name], capture_output=True, check=True)
                members.append((name, result.stdout))
        for name, raw in members:
            text, encoding = decode(raw)
            record = {"archive": entry["path"], "member": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "encoding": encoding}
            if text is None:
                record["status"] = encoding
            else:
                record["status"] = "scanned"
                line_starts = [m.start() for m in re.finditer("\n", text)]
                record["features"] = {}
                for key, pattern in patterns.items():
                    lines = sorted({bisect_right(line_starts, m.start()) + 1 for m in pattern.finditer(text)})
                    if lines:
                        record["features"][key] = lines
            records.append(record)
    summary = {"archives": len({r['archive'] for r in records}), "members": len(records), "statuses": dict(Counter(r['status'] for r in records)), "candidate_members": sum(bool(r.get('features')) for r in records), "nested_archive_members": [r['archive'] + '!' + r['member'] for r in records if Path(r['member']).suffix.lower() in {'.zip', '.rar', '.7z'}]}
    result = {"method": "ZIP read in memory; RAR member contents streamed by system tar to stdout captured in memory. Text searched using the workspace patterns. No source snippets or values exported. Archive copies are not assumed deployed or current.", "summary": summary, "members": records}
    (OUT / "archives.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (OUT / "archive-locations.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["archive", "member", "feature", "line"])
        for r in records:
            for feature, lines in r.get("features", {}).items():
                for line in lines:
                    writer.writerow([r["archive"], r["member"], feature, line])
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

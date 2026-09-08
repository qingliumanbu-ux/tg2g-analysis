"""Read the two user-named DOCX files without modifying them."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

SOURCE = Path(r"D:\AIGC\Documents\Documents\xwechat_files\wxid_3vg7yizievz322_e550\msg\file\2026-09")
NAMES = ["太钢自主可控替换方案_0721.docx", "太钢集团2026年深化自主可控改造项目(二钢北区MES).docx"]
OUT = Path(__file__).resolve().parent / "document-review"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": W[1:-1]}


def text_of(element):
    parts = []
    for node in element.iter():
        if node.tag == W + "t":
            parts.append(node.text or "")
        elif node.tag in {W + "br", W + "tab"}:
            parts.append(" " if node.tag == W + "tab" else " / ")
    return "".join(parts).strip()


def redact(value):
    return re.sub(r"(?i)((?:password|passwd|pwd|api[_ -]?key|secret|token|密码|口令|密钥)\s*[:：=]\s*)[^\s，,；;]+", r"\1<REDACTED>", value)


def main():
    OUT.mkdir(exist_ok=True)
    summaries = []
    for index, name in enumerate(NAMES, 1):
        path = SOURCE / name
        raw = path.read_bytes()
        folder = OUT / f"doc{index}"
        folder.mkdir(exist_ok=True)
        with zipfile.ZipFile(path) as archive:
            root = ET.fromstring(archive.read("word/document.xml"))
            body = root.find(W + "body")
            blocks = []
            for number, child in enumerate(body, 1):
                if child.tag == W + "p":
                    value = text_of(child)
                    if value:
                        blocks.append(f"[P{number}] {redact(value)}")
                elif child.tag == W + "tbl":
                    blocks.append(f"[T{number}]")
                    for row_number, row in enumerate(child.findall(W + "tr"), 1):
                        values = [redact(text_of(cell)).replace("\n", " / ") for cell in row.findall(W + "tc")]
                        blocks.append(f"  R{row_number}: " + " | ".join(values))
            (folder / "content.txt").write_text("\n".join(blocks) + "\n", encoding="utf-8")
            auxiliary = []
            for entry in archive.namelist():
                if re.fullmatch(r"word/(?:header\d+|footer\d+|footnotes|endnotes|comments)\.xml", entry):
                    extra = ET.fromstring(archive.read(entry))
                    value = redact(text_of(extra))
                    if value:
                        auxiliary.append({"part": entry, "text": value})
            (folder / "auxiliary.json").write_text(json.dumps(auxiliary, ensure_ascii=False, indent=2), encoding="utf-8")
            media = []
            for entry in archive.namelist():
                if entry.startswith("word/media/") and not entry.endswith("/"):
                    data = archive.read(entry)
                    media_path = folder / Path(entry).name
                    media_path.write_bytes(data)
                    media.append({"file": media_path.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            app = ET.fromstring(archive.read("docProps/app.xml")) if "docProps/app.xml" in archive.namelist() else None
            stats = {child.tag.split('}')[-1]: child.text for child in app or [] if child.tag.split('}')[-1] in {'Pages','Words','Paragraphs'}}
            summary = {"file": name, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "source_stats_may_be_stale": stats, "blocks": len(blocks), "media": media, "insertions": len(root.findall('.//w:ins', NS)), "deletions": len(root.findall('.//w:del', NS))}
            summaries.append(summary)
    (OUT / "manifest.json").write_text(json.dumps(summaries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summaries, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()

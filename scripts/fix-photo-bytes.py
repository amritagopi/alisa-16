from pathlib import Path

FIXES = {
    "photos/balcony.1.txt": [
        (b'YjDiIc4YRqjZcitHfiO/tcXvp', b'YjDiIc4YRqjZzitHfiO/tcXvp'),
        (b'HckK0NrYuL8NESHEmAnNrA4qU', b'HckK0NrYuL8NOSHEmAnNrA4qU'),
    ],
    "photos/grain.0.txt": [
        (b'92OEx+sASg6oosAuD2xXY4j8V', b'92OEx+sASg6olsAuD2xXY4j8V'),
        (b'UeMNqBhe/npDOZSKbCTQvloXf', b'UeMNqBhe/npDIZSKbCTQvloXf'),
    ],
}

for rel, pairs in FIXES.items():
    path = Path(rel)
    data = path.read_bytes()
    changed = False
    for old, new in pairs:
        if old == new:
            continue
        if new in data and old not in data:
            continue
        count = data.count(old)
        if count != 1:
            raise SystemExit(f"{rel}: expected 1 occurrence of fix, found {count}")
        data = data.replace(old, new, 1)
        changed = True
    if changed:
        path.write_bytes(data)

Path("scripts/fix-photo-bytes.py").unlink(missing_ok=True)
wf = Path(".github/workflows/fix-photo-bytes.yml")
if wf.exists():
    wf.unlink()

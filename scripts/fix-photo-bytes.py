from pathlib import Path

FIXES = {
    "photos/balcony.0.txt": [
        (
            b"vYdmBVbtbImemosCUZ6ZgmtUKZumMzUnzHwItwUH",
            b"vYdmBVbtbImemosCUZ6ZmntUKZumMzUnzHwItwUH",
        )
    ]
}

for rel, pairs in FIXES.items():
    path = Path(rel)
    data = path.read_bytes()
    for old, new in pairs:
        count = data.count(old)
        if count != 1:
            raise SystemExit(f"{rel}: expected 1 occurrence, found {count}")
        data = data.replace(old, new, 1)
    path.write_bytes(data)

Path("scripts/fix-photo-bytes.py").unlink()
Path(".github/workflows/fix-photo-bytes.yml").unlink()

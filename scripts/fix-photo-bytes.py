import hashlib
from pathlib import Path

FIXES = {
    "photos/balcony.1.txt": {
        "sha": "8e238e6c28579e1494972c4b75999a274e01a7a1",
        "size": 24000,
        "pairs": [
            ("4963345952716a5a6369744866694f2f74", "4963345952716a5a7a69744866694f2f74"),
            ("304e7259754c384e455348456d416e4e72", "304e7259754c384e4f5348456d416e4e72"),
        ],
    },
    "photos/grain.0.txt": {
        "sha": "49980dc35cf0f73ecc19cbed8fac660765d61432",
        "size": 24000,
        "pairs": [
            ("782b73415367366f6f7341754432785859", "782b73415367366f637341754432785859"),
            ("714268652f6e70444f5a534b6243545176", "714268652f6e7044495a534b6243545176"),
        ],
    },
}

def blob_sha(data):
    return hashlib.sha1(("blob %d" % len(data)).encode() + bytes([0]) + data).hexdigest()

for rel, spec in FIXES.items():
    path = Path(rel)
    data = path.read_bytes()
    for oh, nh in spec["pairs"]:
        old, new = bytes.fromhex(oh), bytes.fromhex(nh)
        if new in data and old not in data:
            continue
        count = data.count(old)
        if count != 1:
            raise SystemExit("%s: expected 1, found %s" % (rel, count))
        data = data.replace(old, new, 1)
    got = blob_sha(data)
    if got != spec["sha"] or len(data) != spec["size"]:
        raise SystemExit("%s: sha %s size %s" % (rel, got, len(data)))
    path.write_bytes(data)

Path("scripts/fix-photo-bytes.py").unlink(missing_ok=True)
wf = Path(".github/workflows/fix-photo-bytes.yml")
if wf.exists():
    wf.unlink()

import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import unicodedata

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
CORPUS = ROOT / "experiments/idea_collapse/corpus/iclr_2024_2026"
RECOVERY = ROOT / "experiments/idea_collapse/feasibility_1"


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n").encode()


def hash_value(value):
    return hashlib.sha256(encode(value)).hexdigest()


def read_rows(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def save(path, value, rows=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = b"".join(encode(v) for v in value) if rows else encode(value)
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError(f"immutable artifact differs: {path}")
    else:
        with path.open("xb") as f:
            f.write(raw)


def text(value):
    return " ".join(unicodedata.normalize("NFC", value).split())


def render_evidence(items):
    return "\n\n".join(item["abstract_text"] for item in items)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=20).strip()

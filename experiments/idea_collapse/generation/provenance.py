"""Content identities and exclusive evidence writes; standard library only."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def object_hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_hash(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def repository_root():
    return Path(__file__).resolve().parents[3]


def git_state(root=None):
    root = Path(root or repository_root())
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, text=True, timeout=10).strip()
    return {"git_commit": git("rev-parse", "HEAD"),
            "git_dirty": bool(git("status", "--porcelain=v1"))}


def code_hash(root=None):
    root = Path(root or repository_root())
    base = root / "experiments/idea_collapse"
    files = {str(p.relative_to(root)): file_hash(p)
             for p in sorted(base.rglob("*.py")) if "runs" not in p.parts}
    return object_hash(files)


def input_path(relative, root=None):
    root = Path(root or repository_root()).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("input must be inside the repository")
    return path


def write_exclusive(path, raw):
    """Link a completed temporary file into place, never replacing existing evidence."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".evidence-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        os.unlink(temporary)


def export_jsonl(records, output):
    if len({record["run_id"] for record in records}) != len(records):
        raise ValueError("duplicate run IDs in export")
    raw = b"".join(canonical_bytes(record) for record in sorted(records, key=lambda r: r["run_id"]))
    output = Path(output)
    if output.exists():
        if output.read_bytes() != raw:
            raise ValueError("existing JSONL differs; use a new export path")
        return
    write_exclusive(output, raw)

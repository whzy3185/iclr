"""Lossless byte sharding for GitHub transport, with explicit hash verification."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


def hash_file(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def split(path, chunk_size=2 * 1024 * 1024):
    path = Path(path)
    destination = path.with_name(path.name + ".parts")
    destination.mkdir(exist_ok=False)
    parts = []
    with path.open("rb") as source:
        while raw := source.read(chunk_size):
            name = f"part-{len(parts):04d}.bin"
            with (destination / name).open("xb") as target:
                target.write(raw)
            parts.append({"name": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    manifest = {"kind": "LOSSLESS_BYTE_TRANSPORT_NOT_NEW_ANALYSIS", "filename": path.name,
                "bytes": path.stat().st_size, "sha256": hash_file(path), "parts": parts}
    with (destination / "manifest.json").open("x") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    return destination


def restore(parts_path, verify_only=False):
    parts_path = Path(parts_path)
    manifest = json.loads((parts_path / "manifest.json").read_text())
    if Path(manifest["filename"]).name != manifest["filename"]:
        raise ValueError("unsafe output name")
    result = parts_path.parent / manifest["filename"]
    h = hashlib.sha256()
    total = 0
    for index, part in enumerate(manifest["parts"]):
        if part["name"] != f"part-{index:04d}.bin":
            raise ValueError("unexpected part sequence")
        raw = (parts_path / part["name"]).read_bytes()
        if len(raw) != part["bytes"] or hashlib.sha256(raw).hexdigest() != part["sha256"]:
            raise ValueError("part integrity failure")
        h.update(raw)
        total += len(raw)
    if total != manifest["bytes"] or h.hexdigest() != manifest["sha256"]:
        raise ValueError("assembled hash mismatch")
    if verify_only:
        return manifest["sha256"]
    if result.exists():
        if hash_file(result) != manifest["sha256"]:
            raise ValueError("existing artifact differs; refusing overwrite")
        return manifest["sha256"]
    fd, temporary = tempfile.mkstemp(dir=parts_path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as target:
            for part in manifest["parts"]:
                target.write((parts_path / part["name"]).read_bytes())
            target.flush()
            os.fsync(target.fileno())
        if hash_file(temporary) != manifest["sha256"]:
            raise ValueError("restore verification failed")
        os.link(temporary, result)
    finally:
        os.unlink(temporary)
    return manifest["sha256"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["split", "restore", "verify"])
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(split(args.path) if args.mode == "split" else restore(args.path, args.mode == "verify"))

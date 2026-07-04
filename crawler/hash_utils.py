import hashlib
import json
import os

HASH_FILE = "metadata/hashes.json"


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hashes(hashes):
    os.makedirs("metadata", exist_ok=True)

    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=4)
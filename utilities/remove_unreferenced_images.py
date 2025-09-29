"""
Run this script from the root of the repository to delete all unused images.
python3 utilities/remove_unreferenced_images.py
Note: this is broken. chatgpt generated it and it doesn't work right.
"""

import os
import re
import argparse
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
IMAGE_REGEX = re.compile(
    r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=["\']([^"\']+)["\']',
    re.IGNORECASE,
)

def gather_references(root: Path):
    referenced = set()
    for md_file in root.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        for match in IMAGE_REGEX.findall(text):
            for path in match:
                if not path:
                    continue
                # Strip Jekyll/Liquid variables like {{ site.baseurl }}
                path = re.sub(r"\{\{.*?\}\}", "", path).strip()
                # Drop leading slashes
                path = path.lstrip("/")
                ext = Path(path).suffix.lower()
                if ext in IMAGE_EXTS:
                    referenced.add(path.lower())
    return referenced

def gather_actual_images(root: Path):
    images = set()
    for file in root.rglob("*"):
        if file.suffix.lower() in IMAGE_EXTS:
            images.add(str(file.relative_to(root)).lower())
    return images

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview unused images without deleting")
    args = parser.parse_args()

    root = Path(".").resolve()
    referenced = gather_references(root)
    actual = gather_actual_images(root)

    unused = actual - referenced

    print(f"Referenced images: {len(referenced)}")
    print(f"Actual images: {len(actual)}")
    print(f"Unused images: {len(unused)}")

    if not unused:
        print("Nothing to delete.")
        return

    for rel_path in sorted(unused):
        file_path = root / rel_path
        if args.dry_run:
            print(f"(dry-run) Would delete: {file_path}")
        else:
            try:
                file_path.unlink()
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Could not delete {file_path}: {e}")

if __name__ == "__main__":
    main()

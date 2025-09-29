"""
Run this script from the root of the repository to delete all unused images.
python3 utilities/remove_unreferenced_images.py
"""

import os
import re
from pathlib import Path

# File extensions we treat as images
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Regex to match Markdown image/link references: ![alt](path/to/file.jpg)
IMAGE_REGEX = re.compile(r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)

def gather_references(root: Path):
    """Scan all markdown files under root and return set of referenced image paths (relative to root)."""
    referenced = set()
    for md_file in root.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Skipping {md_file}: {e}")
            continue

        for match in IMAGE_REGEX.findall(text):
            # match gives a tuple (md_image, html_image)
            for path in match:
                if not path:
                    continue
                ext = Path(path).suffix.lower()
                if ext in IMAGE_EXTS:
                    # Normalize path
                    referenced.add(str(Path(path).as_posix()))
    return referenced

def gather_actual_images(root: Path):
    """Return set of all image paths (relative to root)."""
    images = set()
    for file in root.rglob("*"):
        if file.suffix.lower() in IMAGE_EXTS:
            images.add(str(file.relative_to(root).as_posix()))
    return images

def main():
    root = Path(".").resolve()

    print("Scanning for image references in markdown...")
    referenced = gather_references(root)

    print("Gathering all actual images...")
    actual = gather_actual_images(root)

    unused = actual - referenced

    print(f"Found {len(referenced)} referenced images")
    print(f"Found {len(actual)} actual images")
    print(f"Found {len(unused)} unused images")

    if not unused:
        print("Nothing to delete.")
        return

    # Delete unused images
    for rel_path in unused:
        file_path = root / rel_path
        try:
            file_path.unlink()
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Could not delete {file_path}: {e}")

if __name__ == "__main__":
    main()

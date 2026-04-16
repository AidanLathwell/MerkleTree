import hashlib
import sys
import os

def hash_file(filepath, algo='sha1'):
    h = hashlib.new(algo)
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def hash_pair(h1, h2, algo='sha1'):
    h = hashlib.new(algo)
    h.update((h1 + h2).encode())
    return h.hexdigest()

def build_merkle_tree(file_paths, algo='sha1'):
    hashes = [hash_file(fp, algo) for fp in file_paths]

    print("\n=== LEAF HASHES ===")
    for i, h in enumerate(hashes):
        print(f"File {i+1}: {h}")

    level = 0

    while len(hashes) > 1:
        print(f"\n=== LEVEL {level + 1} ===")

        new_level = []

        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hash_pair(hashes[i], hashes[i+1], algo)
            else:
                combined = hash_pair(hashes[i], hashes[i], algo)

            print(f"{hashes[i][:8]} + {hashes[i+1][:8] if i+1 < len(hashes) else hashes[i][:8]} -> {combined}")

            new_level.append(combined)

        hashes = new_level
        level += 1

    print("\n=== TOP HASH (MERKLE ROOT) ===")
    print(hashes[0])

    return hashes[0]

if __name__ == "__main__":
    files = sys.argv[1:]

    if not files:
        print("Usage: py merkle_tree.py file1 file2 ...")
        sys.exit(1)

    top_hash = build_merkle_tree(files)
    print("\nTop Hash:", top_hash)

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
    # Step 1: hash all files
    hashes = [hash_file(fp, algo) for fp in file_paths]

    # Step 2: build tree
    while len(hashes) > 1:
        new_level = []

        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hash_pair(hashes[i], hashes[i+1], algo)
            else:
                # If odd number, duplicate last
                combined = hash_pair(hashes[i], hashes[i], algo)

            new_level.append(combined)

        hashes = new_level

    return hashes[0]  # Top hash

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merkle.py file1 file2 ...")
        sys.exit(1)

    files = sys.argv[1:]

    for f in files:
        if not os.path.exists(f):
            print(f"File not found: {f}")
            sys.exit(1)

    top_hash = build_merkle_tree(files)
    print("Top Hash:", top_hash)

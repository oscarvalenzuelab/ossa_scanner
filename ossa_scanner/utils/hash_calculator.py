import os
import json
import hashlib
import ssdeep

def calculate_file_hash(file_path):
    file_hash = {}
    file_hash['sha1'] = compute_sha1(file_path)
    file_hash['sha256'] = compute_sha256(file_path)
    file_hash['ssdeep'] = compute_fuzzy_hash(file_path)
    file_hash['swhid'] = compute_swhid(file_path)
    print(file_hash)
    return file_hash

def compute_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha1.update(chunk)
    return sha1.hexdigest()

def compute_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def compute_fuzzy_hash(file_path):
    return ssdeep.hash_from_file(file_path)

def compute_swhid(file_path):
    sha1_hash = compute_sha1(file_path)
    swhid = f"swh:1:cnt:{sha1_hash}"
    return swhid
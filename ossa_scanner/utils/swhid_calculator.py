from swh.model.hashutil import hash_directory

def calculate_swhid(directory_path):
    return hash_directory(directory_path)

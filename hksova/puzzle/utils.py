import os
import secrets
from flask import current_app
from werkzeug.utils import secure_filename


def get_puzzle_upload_dir():
    upload_dir = os.path.join(current_app.root_path, 'upload', 'puzzles')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


def save_puzzle_file(file_storage, year, puzzle_id):
    if not file_storage:
        return None

    upload_dir = get_puzzle_upload_dir()
    original_filename = secure_filename(file_storage.filename)
    if not original_filename:
        return None

    # YYYY_id_random-hash_original-name
    random_hash = secrets.token_hex(16)
    filename = f"{year}_{puzzle_id}_{random_hash}_{original_filename}"
    file_path = os.path.join(upload_dir, filename)

    file_storage.save(file_path)
    return filename


def delete_puzzle_file(filename):
    if not filename:
        return

    upload_dir = get_puzzle_upload_dir()
    file_path = os.path.join(upload_dir, filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")

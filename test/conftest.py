from io import BytesIO
import os
import shutil
from pathlib import Path
import pytest
from app.server import app

TEST_INPUT_DATA_DIR = os.path.join(Path(__file__).parent.absolute(), 'data/input')
TEST_OUTPUT_DATA_DIR = os.path.join(Path(__file__).parent.absolute(), 'data/output')
TEST_VALIDATION_DATA_DIR = os.path.join(Path(__file__).parent.absolute(), 'data/validation')
TEST_FILES = ['IM000001.dcm', 'IM000010.dcm']
TEST_VALIDATION_FILES = ['IM000001_tags.json']

def seed_test_data():
    shutil.copytree(str(TEST_INPUT_DATA_DIR), str(TEST_OUTPUT_DATA_DIR), dirs_exist_ok=True)

def remove_test_data(only=None):
    with os.scandir(TEST_OUTPUT_DATA_DIR) as entries:
        for entry in entries:
            if only and (entry.name not in only):
                continue
            if not entry.is_dir():
                os.remove(entry.path)

def uploads_contain(f):
    with os.scandir(TEST_OUTPUT_DATA_DIR) as entries:
        for entry in entries:
            if entry.is_dir():
                continue
            if entry.name == f:
                return True
    return False

def get_input_file_as_io(f):
    f = os.path.join(TEST_INPUT_DATA_DIR, f)
    with open(f, 'rb') as f0:
        f0_io = BytesIO(f0.read())
    return f0_io
    
@pytest.fixture()
def test_client():
    remove_test_data()
    app.config['UPLOAD_FOLDER'] = TEST_OUTPUT_DATA_DIR
    yield app.test_client()
    remove_test_data()

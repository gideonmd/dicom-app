from io import BytesIO
import json
import os
from PIL import Image
from werkzeug.datastructures import FileStorage

from test.conftest import seed_test_data, remove_test_data, uploads_contain, get_input_file_as_io, TEST_FILES, TEST_VALIDATION_FILES, TEST_INPUT_DATA_DIR, TEST_VALIDATION_DATA_DIR


def test_get_all_images(test_client):
    response = test_client.get('/images')
    assert '200' in response.status
    assert json.loads(response.data.decode('utf-8')) == []

    seed_test_data()

    response = test_client.get('/images')
    assert '200' in response.status
    assert json.loads(response.data.decode('utf-8')) == TEST_FILES

    remove_test_data(only=[TEST_FILES[0]])
    
    response = test_client.get('/images')
    assert '200' in response.status
    assert json.loads(response.data.decode('utf-8')) == [TEST_FILES[1]]

    remove_test_data()

    response = test_client.get('/images')
    assert '200' in response.status
    assert json.loads(response.data.decode('utf-8')) == []


def test_add_image(test_client):
    test_file_0 = FileStorage(
        stream=open(os.path.join(TEST_INPUT_DATA_DIR, TEST_FILES[0]), "rb"),
        filename=TEST_FILES[0]
    )
    
    response = test_client.post('/images', data={"file": test_file_0}, content_type="multipart/form-data")
    assert '201' in response.status
    assert uploads_contain(TEST_FILES[0])

    test_file_1 = FileStorage(
        stream=open(os.path.join(TEST_INPUT_DATA_DIR, TEST_FILES[1]), "rb"),
        filename=TEST_FILES[1]
    )
    
    response = test_client.post('/images', data={"file": test_file_1}, content_type="multipart/form-data")
    assert '201' in response.status
    assert uploads_contain(TEST_FILES[0])
    assert uploads_contain(TEST_FILES[1])


def test_add_image_exists(test_client):
    seed_test_data()
    
    test_file_0 = FileStorage(
        stream=open(os.path.join(TEST_INPUT_DATA_DIR, TEST_FILES[0]), "rb"),
        filename=TEST_FILES[0]
    )
    
    response = test_client.post('/images', data={"file": test_file_0}, content_type="multipart/form-data")
    assert '409' in response.status


def test_delete_image(test_client):
    seed_test_data()

    response = test_client.delete(f'/images/{TEST_FILES[0]}')
    assert '200' in response.status
    assert not uploads_contain(TEST_FILES[0])
    assert uploads_contain(TEST_FILES[1])

    response = test_client.delete(f'/images/{TEST_FILES[1]}')
    assert '200' in response.status
    assert not uploads_contain(TEST_FILES[0])
    assert not uploads_contain(TEST_FILES[1])


def test_delete_image_not_found(test_client):
    response = test_client.delete(f'/images/DOES_NOT_EXIST.dcm')
    assert '404' in response.status


def test_get_image(test_client):
    seed_test_data()

    test_file_0_data = get_input_file_as_io(TEST_FILES[0])
    test_file_0_data.seek(0)
    response = test_client.get(f'/images/{TEST_FILES[0]}')
    response_bytes = BytesIO(response.data)
    response_bytes.seek(0)

    assert '200' in response.status
    assert response_bytes.read() == test_file_0_data.read()


def test_get_image_not_found(test_client):
    response = test_client.get(f'/images/DOES_NOT_EXIST.dcm')
    assert '404' in response.status


def test_get_image_png(test_client):
    seed_test_data()

    response = test_client.get(f'/images/{TEST_FILES[0]}?png=true')
    response_bytes = BytesIO(response.data)
    response_bytes.seek(0)
    
    response_img = Image.open(response_bytes)
    
    try:
        response_img.verify()
        valid = True
    except Exception:
        valid = False

    assert '200' in response.status
    assert valid


def test_get_image_png_not_found(test_client):
    response = test_client.get(f'/images/DOES_NOT_EXIST.dcm?png=true')
    assert '404' in response.status    


def test_get_image_tags(test_client):
    seed_test_data()

    expected_file = os.path.join(TEST_VALIDATION_DATA_DIR, TEST_VALIDATION_FILES[0])
    with open(expected_file) as f:
        expected = json.load(f)
        
    response = test_client.get(f'/images/{TEST_FILES[0]}/tags')

    assert '200' in response.status
    assert expected == response.json


def test_get_image_tags_search(test_client):
    seed_test_data()

    search_param = '0008,'

    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    expected_file = os.path.join(TEST_VALIDATION_DATA_DIR, TEST_VALIDATION_FILES[0])
    with open(expected_file) as f:
        expected = json.load(f)
    expected = [ e for e in expected if search_param in e ]

    assert '200' in response.status
    assert expected == response.json

    search_param = ',0008'

    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    expected_file = os.path.join(TEST_VALIDATION_DATA_DIR, TEST_VALIDATION_FILES[0])
    with open(expected_file) as f:
        expected = json.load(f)
    expected = [ e for e in expected if search_param in e ]

    assert '200' in response.status
    assert expected == response.json

    search_param = '0008'

    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    expected_file = os.path.join(TEST_VALIDATION_DATA_DIR, TEST_VALIDATION_FILES[0])
    with open(expected_file) as f:
        expected = json.load(f)
    expected = [ e for e in expected if search_param in e ]

    assert '200' in response.status
    assert expected == response.json

    search_param = '0010,0010'

    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    expected_file = os.path.join(TEST_VALIDATION_DATA_DIR, TEST_VALIDATION_FILES[0])
    with open(expected_file) as f:
        expected = json.load(f)
    expected = [ e for e in expected if search_param in e ]

    assert '200' in response.status
    assert expected == response.json


def test_get_image_tags_not_found(test_client):
    seed_test_data()
    
    search_param = '008'
    response = test_client.get(f'/images/DOES_NOT_EXIST.dcm/tags?search={search_param}')
    assert '404' in response.status

    response = test_client.get(f'/images/DOES_NOT_EXIST.dcm/tags')
    assert '404' in response.status    

    
def test_get_image_tags_search_invalid(test_client):
    seed_test_data()
    
    search_param = '008'
    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    assert '400' in response.status

    search_param = '00800'
    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    assert '400' in response.status

    search_param = '008,0029'
    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    assert '400' in response.status

    search_param = ',1234,1234'
    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    assert '400' in response.status

    search_param = '213$,asyb'
    response = test_client.get(f'/images/{TEST_FILES[0]}/tags?search={search_param}')
    assert '400' in response.status

from __future__ import annotations

import os

from pathlib import Path
from typing import Optional, List, Union
from flask import Flask, request, jsonify, send_from_directory

from app.models import DicomFile, DicomDirectory
    

DATA_CAP = int(os.environ.get('DATA_CAP', 100 * 1024 * 1024))
DATA_LOC = os.environ.get('DATA_LOC', 'data')
DATA_DIR = os.path.join(Path(__file__).parent.parent.absolute(), DATA_LOC)

app = Flask(__name__, static_folder='../public', static_url_path='/')
app.config['TITLE'] = 'Image API'
app.config['DESCRIPTION'] = 'API for managing images and their tags'
app.config['VERSION'] = '1.0.0'
app.config['UPLOAD_FOLDER'] = DATA_DIR
app.config['MAX_CONTENT_LENGTH'] = DATA_CAP


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/images', methods=['GET'])
def list_images():
    """
    List all image names
    """
    print(request.headers.get('Accept'))
    image_names = DicomDirectory(app.config['UPLOAD_FOLDER']).all()
    return image_names, 200

@app.route('/images', methods=['POST'])
def add_image():
    """
    Add a new image
    """
    if 'file' not in request.files:
        return 'No file name provided', 400

    f = request.files['file']
        
    if f.filename == '':
        return 'No file name provided', 400

    dicom_dir = DicomDirectory(app.config['UPLOAD_FOLDER'])
    
    if dicom_dir.exists(f.filename):
        return f'File with name already exists: {f.filename}', 409 # Status Code: Conflict

    if not dicom_dir.safe_path(f.filename):
        return f'Invalid file name: {f.filename}', 400
    
    if f and dicom_dir.accepts(f.filename):
        dicom_dir.add(f)
        return 'Created', 201
    else:
        return 'Unable to process file', 400

@app.route('/images/<name>', methods=['GET'])
def get_image_by_name(name):
    """
    Find image by name
    """
    dicom_dir = DicomDirectory(app.config['UPLOAD_FOLDER'])
    
    if not dicom_dir.exists(name):
        return f'Image not found: {name}', 404

    dicom_file = dicom_dir.get_file(name)
    png = request.args.get('png')

    if png == 'true':
        dicom_file.convert_to_png()
        return send_from_directory(dicom_file.directory.data_dir, dicom_file.name.replace('.dcm', '.png'))
    else:
        return send_from_directory(dicom_file.directory.data_dir, dicom_file.name)

@app.route('/images/<name>', methods=['DELETE'])
def delete_image(name):
    """
    Delete image by name
    """
    dicom_dir = DicomDirectory(app.config['UPLOAD_FOLDER'])
    
    if not dicom_dir.exists(name):
        return f'Image not found: {name}', 404

    status, msg = dicom_dir.remove(name)

    if status:
        return msg, 200
    else:
        return msg, 400

@app.route('/images/<name>/tags', methods=['GET'])
def get_image_tags(name):
    """
    Get image tags
    """
    dicom_dir = DicomDirectory(app.config['UPLOAD_FOLDER'])
    
    if not dicom_dir.exists(name):
        return f'Image not found: {name}', 404
    
    search = request.args.get('search')

    if search:
        if not DicomFile.valid_tag_search(search):
            return (
                f'Invalid search param: {search}.'
                ' Valid examples: "0008"; "0008,"; ",0008"; "0010,0008".'
            ), 400
        
    return dicom_dir.get_file(name).search_tags(search=search), 200
            


if __name__ == '__main__':
    app.run(debug=True)

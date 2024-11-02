import cv2
import numpy as np
import os
import png
from pydicom import dcmread
import re
from werkzeug.utils import secure_filename


class DicomFile:

    @staticmethod
    def valid_tag_search(search):
        if re.match(r'^[a-zA-Z0-9]{4}$', search):
            return True
        elif re.match(r'^[a-zA-Z0-9]{4},$', search):
            return True
        elif re.match(r'^,[a-zA-Z0-9]{4}$', search):
            return True
        elif re.match(r'^[a-zA-Z0-9]{4},[a-zA-Z0-9]{4}$', search):
            return True
        else:
            return False

    def __init__(self, directory, name):
        self.directory = directory
        self.name = name
        self.location = os.path.join(self.directory.data_dir, name)

    def convert_to_png(self):
        png_fname = os.path.basename(self.location).lower().replace('.dcm', '.png')
        png_path = os.path.join(self.directory.data_dir, png_fname)

        if self.directory.exists(png_path):
            return True
    
        ds = dcmread(self.location)
        shape = ds.pixel_array.shape
        
        image_2d = ds.pixel_array.astype(float) # Convert to float to avoid overflow or underflow losses.
        image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0 # Rescaling grey scale between 0-255
        image_2d_scaled = np.uint8(image_2d_scaled) # Convert to uint

        with open(png_path, 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=True)
            w.write(png_file, image_2d_scaled)

        return True

    def search_tags(self, search=None):
        if search:
            components = [ c.strip() for c in search.split(',') ]
        else:
            components = []

        if len(components) == 0:
            criteria = lambda _: True
        elif len(components) == 1:
            group_n, elem_n = int(components[0], 16), int(components[0], 16)
            criteria = lambda tag: (tag.group == group_n) or (tag.elem == elem_n)
        elif len(components) == 2:
            if components[0] == '':
                elem_n = int(components[1], 16)
                criteria = lambda tag: tag.elem == elem_n
            elif components[1] == '':
                group_n = int(components[0], 16)
                criteria = lambda tag: tag.group == group_n
            else:
                group_n, elem_n = int(components[0], 16), int(components[1], 16)
                criteria = lambda tag: (tag.group == group_n) and (tag.elem == elem_n)
        else:
            raise ValueError(f"Invalid search parameter: {search}")

        results = []
        with dcmread(self.location) as ds:
            for data_element in ds.iterall():
                if criteria(data_element.tag):
                    results.append(str(data_element))
        return results

        
class DicomDirectory:
    ALLOWED_EXTENSIONS = ['dcm']

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        
    def fullpath(self, f):
        return os.path.join(self.data_dir, f)            

    def accepts(self, filename):
        return '.' in filename and (filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS)

    def exists(self, filename):
        return os.path.isfile(self.fullpath(filename))

    def safe_path(self, filename):
        if (filename == os.path.basename(filename)): # guard: security
            return True
        else:
            return False
        
    def get_file(self, filename):
        filename = secure_filename(filename)
        return DicomFile(self, filename)

    def add(self, f):
        filename = secure_filename(f.filename)
        f.save(self.fullpath(filename))

    def remove(self, filename):
        filename = secure_filename(filename)
        try:
            os.remove(self.fullpath(filename))
            return True, 'ok'
        except OSError as e:
            return False, str(e)

    def all(self):
        is_dcm = lambda x: os.path.isfile(self.fullpath(x)) and self.accepts(x)
        return [
            f for f in os.listdir(self.data_dir) if is_dcm(f)
        ]

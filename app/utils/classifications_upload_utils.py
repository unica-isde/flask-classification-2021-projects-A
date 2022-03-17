from config import Configuration
from werkzeug.utils import secure_filename
import os


def check_extensions(filename):
    '''
    check if the extension of the image is included
    among those specified in the tuple allowed_extension
    if it is return True
    else False
    '''
    if len(filename.split('.')) == 2:
        return filename.split('.')[1] in Configuration.allowed_extension
    return False


def is_allowed_file(filename):
    '''
    Check if the filename is not empty
    and call the function check_extension
    return True if both those checks are successfully
    else return False
    '''
    if filename == '':
        return False
    return check_extensions(filename)


def return_path():
    '''
    return the path of the image specified in UPLOAD_FOLDER
    if this path doesn't exist it create it
    '''
    image_path = Configuration.UPLOAD_FOLDER
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    return image_path


def save_image(upload_image):
    '''
    save the image
    '''
    image_path = return_path()
    filename = secure_filename(upload_image.filename)
    upload_image.save(os.path.join(image_path, filename))

from app import app
from app.utils.list_images import list_images
from config import Configuration


@app.route('/info', methods=['GET'])
def info():
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {
        "models": list_of_models,
        "images": list_of_images
    }

    return data
from PIL import Image
from config import Configuration
from ml.classification_utils import fetch_image
import torchvision.transforms.functional as TF
import os

conf = Configuration()

def transform_image(brightness=conf.default_brightness, contrast=conf.default_contrast, saturation=conf.default_saturation, hue=conf.default_hue, image_id=""):
    img = fetch_image(image_id)

    output = TF.adjust_brightness(img, brightness)
    output = TF.adjust_contrast(output, contrast)
    output = TF.adjust_saturation(output, saturation)
    output = TF.adjust_hue(output, hue)

    image_name, _ = image_id.split(".")

    edit_img_id = "{}_{}_{}_{}_{}.JPEG".format(image_name, brightness, contrast, saturation, hue)

    return output, edit_img_id

def save_image(image_id, image):
    image_path = os.path.join(conf.edit_image_folder_path, image_id)
    image.save(image_path)


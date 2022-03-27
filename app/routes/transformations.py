from flask import render_template

from app import app
from app.forms.transformation_form import TransformationForm
from ml.transformation_utils import transform_image, save_image
from config import Configuration

config = Configuration()

@app.route('/transformations', methods=['GET', 'POST'])
def transformations():
    """API for selecting a an image and running a
    transformation job. Returns the output image from the
    transformation."""
    form = TransformationForm()
    if form.validate_on_submit():  # POST

        brightness = form.brightness.data
        contrast = form.contrast.data
        saturation = form.saturation.data
        hue = form.hue.data

        image_id = form.image.data

        img, edit_image_id = transform_image(brightness, contrast, saturation, hue, image_id)

        save_image(edit_image_id, img)

        # returns the image transformation output
        return render_template("transformation_output.html", image_id=image_id, edit_image_id=edit_image_id)

    # otherwise, it is a get request and should return the
    # transformation selecter
    return render_template('transformation_select.html', form=form)

""""
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
"""
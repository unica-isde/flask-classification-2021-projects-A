import redis
from flask import render_template
import os
from app import app
from app.forms.image_histogram_form import HistogramForm
from config import Configuration
import matplotlib.pyplot as plt
import cv2
import numpy as np
    
config = Configuration()

@app.route('/showhistogram', methods=['GET', 'POST'])
def showHistogram():
    """API for selecting an image and running a 
    histogram image job. Returns the original image and histogram image
    """
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        histogram_image = plot_png(image_id)

        return render_template("show_histogram.html", histogram_image=histogram_image, image_id=image_id)

    # otherwise, it is a get request and should return the
    # image  selector
    return render_template('show_histogramform.html', form=form)


def plot_png(imageurl):
    image_path = os.path.join(config.image_folder_path, imageurl)
    histo_path =os.path.join(config.histo_folder_path,imageurl)
    # read image
    im = cv2.imread(image_path)
    # calculate mean value from RGB channels and flatten to 1D array
    vals = im.mean(axis=2).flatten()
    # calculate histogram
    counts, bins = np.histogram(vals, range(257))
    # plot histogram centered on values 0..255
    plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])
    plt.savefig(histo_path)
    return imageurl

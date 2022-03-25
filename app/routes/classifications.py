import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from app.forms.classification_form2 import ClassificationForm2

from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()


@app.route('/classifications', methods=['GET', 'POST'])
def classifications():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""
    form = ClassificationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": image_id
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_select.html', form=form)






@app.route('/showhistogram', methods=['GET', 'POST'])
def showHistogram():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""
    form = ClassificationForm2()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        
        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "img_id": image_id
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        histogram_image = plot_png(image_id)

        return render_template("show_histogram.html", histogram_image=histogram_image, image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image  selector
    return render_template('show_histogramform.html', form=form)


def plot_png(imageurl):
    import matplotlib.pyplot as plt
    import cv2
    imagepath = "/home/nahom/Documents/flask-classification-2021-projects-A/app/static/imagenet_subset/" + imageurl 
    
    import numpy as np


    # read image
    im = cv2.imread(imagepath)
    # calculate mean value from RGB channels and flatten to 1D array
    vals = im.mean(axis=2).flatten()
    # calculate histogram
    counts, bins = np.histogram(vals, range(257))
    # plot histogram centered on values 0..255
    plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])
    # plt.show()
    
    # im = cv2.imread(imagepath)
    # # calculate mean value from RGB channels and flatten to 1D array
    # vals = im.mean(axis=2).flatten()
    # # plot histogram with 255 bins
    # b, bins, patches = plt.hist(vals, 255)
    # plt.xlim([0,255])
    plt.savefig('/home/nahom/Documents/flask-classification-2021-projects-A/app/static/histoimage/'+ imageurl)
    #plt.show() 
    return imageurl

from flask import Flask, render_template, request, url_for, flash, redirect

#other libraries
import os
import numpy as np
from skimage import io
import math
import random
import copy
import scipy.misc
import filters

UPLOAD_FOLDER = 'server/imageProc/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def add_header(response):
    response.cache_control.max_age = 10
    return response


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("not work")
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.root_path, 'static/uploads/', 'result.png'))

    return render_template('home.html')

@app.route("/about")
def about():
    #return "Made by Kirtan and Tim."
    return render_template('about.html')

@app.route("/result", methods=['GET', 'POST'])
def result():


    imageSelected = False

    select = request.form.get('comp_select')
    compress = request.form.get('compress')


    if request.method == 'POST':

        #print(await (request.files))


        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("here")
            imageSelected = True
            filename = file.filename
            file.save(os.path.join(app.root_path, 'static/uploads/', 'result.png'))


    if imageSelected:
        photo = io.imread( 'imageProc/static/uploads/result.png' )
    else:
        photo = io.imread( 'imageProc/static/uploads/Jeff_Ames.png' )


    if compress == 'compressed':
        print("true")
        photo = scipy.misc.imresize(photo,0.5)

    print(select)
    if select == None:
        select = 'bnw'


    test = getattr(filters, select)
    photo = test(photo)


    #photo = filters.glassDoor(photo)
    scipy.misc.imsave('imageProc/static/uploads/result.png', photo)

    return render_template('result.html')


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
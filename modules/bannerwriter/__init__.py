import json
import logging
import os
import random
import time
import requests
import pyfiglet

from pathlib import Path

from celery import Celery
from flask import (Flask, flash, jsonify, make_response, redirect,
                   render_template, request, url_for)
from flask_wtf import FlaskForm


app = Flask(__name__, template_folder="../../resources/templates",
            static_folder="../../resources/static")


# Flask Configuration
app.config['SECRET_KEY'] = '\xf0\x9524"C\xa2\xdd\xac\xc6\xa2O\t\xaf\x0bA\x96,5\xe5r\x96\x99\xc8'

# Celery Configuration

celery = Celery(app.name, backend='rpc://', broker='pyamqp://')#broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route("/")
def home():
    '''
    Endpoint serving about home page and form
    '''
    form = FlaskForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template("home.html", title='Home', form=form)


@app.route('/asciiart', methods=['POST'])
def asciiart():
    print(request.form.get('text'))
    text = request.form.get('text')
    if(text == None):
        result = {
            'error': 'invalid input',
        }
    else:
        task = generate_art_task.apply_async(args=[text])
        result = {
            "text": text,
            "url": url_for('taskstatus', task_id=task.id),
            "status": 'Submitted'
        }
    return jsonify(result)


@app.route('/status/<task_id>')
def taskstatus(task_id):
    '''
    Endpoint to check task status '/status/<task_id>'
    '''

    task = generate_art_task.AsyncResult(task_id)

    if task.state == 'SUCCESS':
        response = task.info.get('art', None)
    else:
        # in other cases
        response = jsonify({
            'text': task.info.get('text', None),
            'state': task.state,
        })
    return response, 201, {'Content-Type': 'text/plain'}


@celery.task(bind=True)
def generate_art_task(self, text):
    '''
    Background task that runs a long function with progress reports.
    '''

    try:
        meta_info = {'text': text}
        self.update_state(state='PROGRESS', meta=meta_info)

        ascii_banner = pyfiglet.figlet_format(text)
        time.sleep(10)
        result = {
            "text": text,
            "art": ascii_banner
        }
    except Exception as e:
        meta_info['error'] = e
        self.update_state(state='FAILURE', meta=meta_info)

    print('Background [generate_art_task] completed')
    return result    


@app.route("/about")
def about():
    '''
    Endpoint serving about page
    '''
    return render_template("about.html")
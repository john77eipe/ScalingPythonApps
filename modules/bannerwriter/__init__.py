import json
import logging
import os
import random
import time
import requests
import pyfiglet

from pathlib import Path

from flask import (Flask, flash, jsonify, make_response, redirect,
                   render_template, request, url_for)
from flask_wtf import FlaskForm

# Flask app
app = Flask(__name__, template_folder="../../resources/templates",
            static_folder="../../resources/static")
app.config['SECRET_KEY'] = '\xf0\x9524"C\xa2\xdd\xac\xc6\xa2O\t\xaf\x0bA\x96,5\xe5r\x96\x99\xc8'



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
        response = generate_art_task(text)
    return response['art'], 201, {'Content-Type': 'text/plain'}



def generate_art_task(text):
    '''
    Background task that runs a long function.
    '''

    try:
        ascii_banner = pyfiglet.figlet_format(text)
        time.sleep(5)
        result = {
            "text": text,
            "art": ascii_banner
        }
    except Exception as e:
        print(e)

    print(' [generate_art_task] completed')
    return result    


@app.route("/about")
def about():
    '''
    Endpoint serving about page
    '''
    return render_template("about.html")
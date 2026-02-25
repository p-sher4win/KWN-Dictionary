from flask import Blueprint, render_template, jsonify
from .mast_models import *

root = Blueprint('root', __name__)

@root.route('/dashboard')
def dashboard():
    
    return render_template('view/dashboard.html')


@root.route('/synset')
def get_synset():

    data = KonkaniWord.query.all()
    
    return render_template('view/synset.html', data=data)
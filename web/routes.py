from flask import Blueprint, render_template
from .webforms import TestFrom
from .models import Test


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    
    return render_template('view/home.html')
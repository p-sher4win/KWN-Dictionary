from flask import Blueprint, render_template


root = Blueprint('root', __name__)

@root.route('/dashboard')
def dashboard():
    
    return render_template('view/dashboard.html')
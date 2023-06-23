from flask import Blueprint, render_template, g
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("Home.html")

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('Dashboard.html')

@views.route('/pricing')
def pricing():
    return render_template('Pricing.html')
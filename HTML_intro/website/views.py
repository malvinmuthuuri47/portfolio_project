from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Hotels

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("Home.html")

@views.route('/dashboard')
@login_required
def dashboard():
    hotels = Hotels.query.all()
    return render_template('Dashboard.html', hotels=hotels)

@views.route('/deals')
def deals():
    hotels = Hotels.query.all()
    return render_template('Pricing.html', hotels=hotels)

@views.route('/hotel')
def hotel():
    hotels = Hotels.query.all()
    return render_template('Hotel.html', hotels=hotels)
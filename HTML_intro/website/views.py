from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Hotels

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # This function redirects to the Home page
    return render_template("Home.html")

@views.route('/dashboard')
@login_required
def dashboard():
    # This function rdirects the user to the dashboard and it requires a user to have an account created.
    # The hotels variable holds all the details of the hotels present in the database and so we have to
    # pass the details to the template so that we can dynamically display the details of the hotels to
    # the user.
    hotels = Hotels.query.all()
    return render_template('Dashboard.html', hotels=hotels)

@views.route('/deals')
def deals():
    # This function redirects the user to the deals page that contains the offers available at various hotels.
    hotels = Hotels.query.all()
    return render_template('Pricing.html', hotels=hotels)
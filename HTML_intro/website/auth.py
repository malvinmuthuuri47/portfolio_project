from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Hotels

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Function that handles the signup page. It gets the details from the form and checks if they exist in the database
    If the email exists, the user is asked to enter another email as email field is unique. It also checks if the first
    and last name are strings and also if the passwords entered are the same.
    If the email doesn't exist, the user is added to the database and allowed to access the website's dashboard.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists', category='error')
        elif len(email) < 4:
            flash('Email must be a valid email', category='error')
        elif not isinstance(firstName, str):
            flash('Please enter a valid FirstName', category='error')
        elif not isinstance(lastName, str):
            flash('Please enter a valid LastName', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 7:
            flash('Password is too short', category='error')
        else:
            # add user to database
            new_user = User(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.dashboard', user=user))

    return render_template('Signup.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function queries the database when the user enters their email and password. If the user exists in the database,
    they are logged in and if not, they are asked to signup or entera valid email/password
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            elif not check_password_hash(user.password, password):
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email doesn\'t exist.', category='error')
    return render_template('Login.html', user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required # This decorator just ensures that the function can only be accessed if the user is logged in
def profile():
    """
    This function is responsible for allowing an existing user to alter the specific details of their profile
    including the email, first and last name.
    """
    user = User.query.all()
    if request.method == 'POST':
        current_user.email = request.form.get('email')
        current_user.firstName = request.form.get('firstName')
        current_user.lastName = request.form.get('lastName')

        try:
            db.session.commit()
            flash('Profile updated')
            return redirect('/dashboard')
        except:
            return "Update unsuccessful"
    else:
        return render_template('Profile.html', user=current_user)

@auth.route('/search', methods=['GET'])
@login_required
def search():
    """
    This function is responsible for filtering the results of hotels based on price and location when the user
    wished to see the hotels available in a certain location should they choose to search rather than scrolling
    through the entire website.
    """
    search_term_location = request.args.get('location')
    search_term_price = request.args.get('price')

    hotels_location = Hotels.query.filter_by(location=search_term_location).all()
    hotels_price = Hotels.query.filter_by(price=search_term_price).all()

    if hotels_location:
        flash('Location exists', category='success')
        return render_template('Search.html',hotels_location=hotels_location)
    elif hotels_price:
        flash('Hotels with that price are available', category='success')
        return render_template('Search.html', hotels_price=hotels_price)
    else:
        flash('No facilities in that area/price range', category='error')
        return redirect(url_for('views.dashboard'))

    return render_template('Search.html')

@auth.route('/logout')
@login_required
def logout():
    # This function is responsible for logging out a user and redirecting them ot the login page.
    logout_user()
    return redirect(url_for('auth.login'))
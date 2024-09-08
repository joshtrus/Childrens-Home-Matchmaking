#GET requests display content, POST requests submit content (sorta)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Home, Donater
from . import db, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps

auth = Blueprint('auth', __name__)

#------------------------------------------------------------------------#
#TESTING SOMETHING HERE
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.urole != role) and (role != "ANY")):
                return login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
# https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes



#------------------------------------------------------------------------#
#LOGIN

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user: #if we did actually find a user
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                if user.urole == "Donater":
                    return redirect(url_for('views.donater'))
                else:
                    return redirect(url_for('views.chome_profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


#------------------------------------------------------------------------#
#LOGOUT

@auth.route('/logout')
@login_required(role="ANY")
def logout():
    logout_user() #logs out current user
    return redirect(url_for('auth.login'))


#------------------------------------------------------------------------#
#SIGNUP

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        urole = request.form.get('urole')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first() 
        if user:
            flash('Email already exists', category='error')
        else:
            if len(email) < 4:
                flash('Invalid email', category='error')
            elif len(full_name) < 2:
                flash('Invalid first name', category='error')
            elif password1 != password2:
                flash('Passwords do not match', category='error')
            elif len(password1) < 7:
                flash('Password is too short', category='error')
            else:
                #add user to database
                new_user = User(full_name=full_name, email=email, password=generate_password_hash(password1, method='sha256'), urole=urole)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!', category='success')
                if new_user.urole == 'Donater':
                    new_donater = Donater(full_name=full_name, donater_email=email, donater_password=generate_password_hash(password1, method='sha256'))
                    db.session.add(new_donater)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.chome_edit_profile'))
                elif new_user.urole == "CHome":
                    new_home = Home(home_name=full_name, home_email=email, home_password=generate_password_hash(password1, method='sha256'))
                    db.session.add(new_home)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)

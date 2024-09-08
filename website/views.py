from flask import Blueprint, jsonify, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .auth import login
from . import db 
from .models import User, Home, Donater
import sqlite3

# -----------------------------------------------------------------------------------------------------------------#
# SETTING UP SQLITE THINGS for matchmaking survey
# Connection and cursor
# conn = sqlite3.connect('homes_in_database.db')
# cursor = conn.cursor()
# create_table = """CREATE TABLE IF NOT EXISTS
# matchmaker(id INTEGER PRIMARY KEY autoincrement, parish TEXT, type TEXT, size TEXT, budget TEXT)"""
# cursor.execute(create_table)


#------------------------------------------------------------------------#
#GENERAL VIEWS
views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/shelters', methods=['GET', 'POST'])
def shelters():
    allShelters = Home.query.all()
    return render_template("shelters.html", user=current_user, shelters=allShelters)

@views.route('/about')
def about():
    return render_template("about_us.html", user=current_user)

@views.route('/learn-more/<home_name>')
def shelter_details(home_name):
    shelter_details = Home.query.filter(Home.home_name==home_name).first()
    return render_template("shelter_details.html", user=current_user, shelter_details=shelter_details, home_name=home_name)

#------------------------------------------------------------------------#
#VIEWS TO DO WITH CHILDREN'S HOMES
@views.route('/chome', methods=['GET', 'POST'])
@login_required
def chome_profile():
    #-------#
    if current_user.urole != "CHome":
        return redirect(url_for("auth.login"))
    #-------#
    home = Home.query.filter_by(home_name=current_user.full_name).first() 
    return render_template("chome_profile.html", user=current_user, home=home)

@views.route('/chome-edit-profile', methods=['GET', 'POST'])
@login_required
def chome_edit_profile():
    #-------#
    if current_user.urole != "CHome":
        return redirect(url_for("auth.login"))
    #-------#
    if request.method == 'POST':
        home_name = request.form.get('home_name')
        current_email = request.form.get('current_email')
        home_email = request.form.get('home_email')
        home_location = request.form.get('home_location')
        home_population = request.form.get('home_population')
        home_specialization = request.form.get('home_specialization')
        home_description = request.form.get('home_description')
        home_needs = request.form.get('home_needs')
        home_needs_cost = request.form.get('home_needs_cost')
        home_needs_cost = int(home_needs_cost)
        #---------------------------#
        #Updating User Table
        this_user = User.query.filter_by(email=current_email).first() 
        if len(home_name) > 0:
            this_user.full_name = home_name
            db.session.commit()
        else:
            print('')
        if len(home_email) > 0:
            this_user.email = home_email
            db.session.commit()
        else:
            print('')
        #---------------------------#
        #Updating Home Table
        home = Home.query.filter_by(home_email=current_email).first() 
        if home:
            home.home_name = this_user.full_name
            home.home_email = this_user.email
            db.session.commit()
            if len(home_location) > 0:
                home.home_location = home_location
                db.session.commit()
            else:
                print('No change')
            if len(home_population) > 0:
                home.home_population = home_population
                db.session.commit()
            else:
                print('No change')
            if len(home_specialization) > 0:
                home.home_specialization = home_specialization
                db.session.commit()
            else:
                print('No change')
            if len(home_description) > 0:
                home.home_description = home_description
                db.session.commit()
            else:
                print('No change')
            if len(home_needs) > 0:
                home.home_needs = home_needs
                db.session.commit()
            else:
                print('No change')
            if home_needs_cost > 0:
                home.home_needs_cost = home_needs_cost
                db.session.commit()
            else:
                print('No change')
        else:
            home_name = this_user.full_name
            home_email = this_user.email
            if len(home_location) > 0:
                home_location = home_location
            else:
                home_location = " "
            if len(home_population) > 0:
                home_population = home_population
            else:
                home.home_population = " "
            if len(home_specialization) > 0:
                home_specialization = home_specialization
            else:
                home_specialization = " "
            if len(home_description) > 0:
                home_description = home_description
            else:
                home_description = ""
            if len(home_needs) > 0:
                home_needs = home_needs
            else:
                home_needs = ""
            if home_needs_cost > 0:
                home_needs_cost = home_needs_cost
            else:
                home_needs_cost = 0

            new_home = Home(home_name=home_name, home_email=home_email, home_location=home_location, home_population=home_population, home_specialization=home_specialization, home_description=home_description, home_needs=home_needs, home_needs_cost=home_needs_cost)
            db.session.add(new_home)
            db.session.commit()
        db.session.commit()
        return redirect(url_for('views.chome_profile'))
    home = Home.query.filter_by(home_name=current_user.full_name).first() 
    return render_template("chome_edit_your_profile.html", user=current_user, home=home)


#------------------------------------------------------------------------#
#VIEWS TO DO WITH DONATERS
#TODO uncomment login_required decoraters


@views.route('/donater', methods=['GET', 'POST'])
@login_required
def donater():
    #-------#
    if current_user.urole != "Donater":
        return redirect(url_for("auth.login"))
    #-------#
    donater = Donater.query.filter_by(full_name=current_user.full_name).first() 
    return render_template("d_profile.html", user=current_user, donater=donater)



@views.route('/donater-edit-profile', methods=['GET', 'POST'])
@login_required
def donater_edit_profile():
    #-------#
    if current_user.urole != "Donater":
        return redirect(url_for("auth.login"))
    #-------#
    if request.method == 'POST':
        donater_name = request.form.get('donater_name')
        current_email = request.form.get('current_email')
        donater_email = request.form.get('donater_email')
        #---------------------------#
        #Updating User Table
        this_user = User.query.filter_by(email=current_email).first() 
        if len(donater_name) > 0:
            this_user.full_name = donater_name
            db.session.commit()
        else:
            print('')
        if len(donater_email) > 0:
            this_user.email = donater_email
            db.session.commit()
        else:
            print('')
        #---------------------------#
        #Updating Donater Table
        donater = Donater.query.filter_by(donater_email=current_email).first()
        if donater:
            donater.donater_name = this_user.full_name
            donater.donater_email = this_user.email
            db.session.commit()
        else:
            donater_name = this_user.full_name
            donater_email = this_user.email
            new_donater = Donater(full_name=donater_name, donater_email=donater_email)
            db.session.add(new_donater)
            db.session.commit()
        db.session.commit()
        print(donater.full_name, donater.donater_email)
        return redirect(url_for("views.donater"))
    donater = Donater.query.filter_by(full_name=current_user.full_name).first() 
    return render_template("donater_edit_your_profile.html", user=current_user, donater=donater)


@views.route('/matchmaking-survey', methods=['GET', 'POST'])
@login_required
def donater_survey():
    #-------#
    if current_user.urole != "Donater":
        return redirect(url_for("auth.login"))
    #-------#
    if request.method == 'POST':
        parish = request.form.get('parish')
        budget = request.form.get('budget')
        size = request.form.get('party')
        type = request.form.get('specialization')
        #HOME DATABASE SQLITE THINGS
        conn = sqlite3.connect('homes_in_database.db')
        cursor = conn.cursor()
        create_table = """CREATE TABLE IF NOT EXISTS
        matchmaker(id INTEGER PRIMARY KEY autoincrement, parish TEXT, type TEXT, size TEXT, budget TEXT)"""
        cursor.execute(create_table)
        tableName = "matchmaker"
        cursor.execute("INSERT INTO {tableName} (parish, type, size, budget) VALUES(?,?,?,?)".format(tableName=tableName),
        (parish, type, size, budget))
        conn.commit()
        # #EMAILS DATABASE SQLITE THINGS
        # conn = sqlite3.connect('email_list.db')
        # cursor = conn.cursor()
        # create_table = """CREATE TABLE IF NOT EXISTS
        # emails(id INTEGER PRIMARY KEY autoincrement, email TEXT)"""
        # cursor.execute(create_table)
        # tableName = "emails"
        # cursor.execute("INSERT INTO {tableName} (email) VALUES(?)".format(tableName=tableName), (current_user.email))
        # conn.commit()
        return render_template("confirmation.html", user=current_user)
    else: 
        return render_template("match.html", user=current_user)

from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/') #this is the form to register/login
def home_page():
    return render_template("home_page.html")

@app.route('/register_user', methods = ['POST']) #this is to actually register a user
def register_user():
    print(request.form) #print statement should be on all post methods to make sure the information is being taken in 
    if not User.validate_create(request.form): #validation needs to happen BEFORE hashing 
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) #hashing - make sure Bcrpyt is installed/imported 
    print(pw_hash)    
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id #this key is IMPORTANT to hold information (Result of an insert query)
    return redirect('/dashboard')

@app.route('/login_user', methods = ['POST']) #this is to login a user
def login():
    print(request.form)
    data = {
        "email" : request.form['email']
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db: #checks to see if email is correct
        flash('Invalid Email/password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): #checks to see if password is correct
        flash('Invalid Email/password')
        return redirect('/')
    session['user_id'] = user_in_db.id #this is result of select query 
    return redirect('/dashboard')

@app.route('/dashboard') #this is dashbaord/welcome for user
def dashboard():
    if "user_id" not in session: #if user is not logged in this will take them back to the login/register page 
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('dashboard.html', active_user = User.get_by_id(data))

@app.route('/logout') #this is to logout
def logout():
    session.clear() #this clears the session 
    return redirect('/')
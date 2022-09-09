from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/') #this is the form to register/login
def home_page():
    return render_template("home_page.html")

@app.route('/register_user', methods = ['POST']) #this is to actually register a user
def register_user():
    print(request.form)
    if not User.validate_create(request.form): #validation needs to happen BEFORE hashing 
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)    
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id #this key is IMPORTANT
    return redirect('/dashboard')
from flask import Blueprint, abort, redirect, render_template,request, session, url_for
from jinja2 import TemplateNotFound
from pyrebase import pyrebase


# Configuration and Initialize firebase
config = {
  "apiKey": "AIzaSyAPy27QXRyF66zTNI8_7YL6VPy6_fV1YN0",
  "authDomain": "kingsbiz.firebaseapp.com",
  "projectId": "kingsbiz",
  "storageBucket": "kingsbiz.appspot.com",
  "messagingSenderId": "759077597041",
  "appId": "1:759077597041:web:0c7aab9c764499cacf50d0",
  'databaseURL':''
    
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Registering our urls
views = Blueprint(__name__,"views")

# home page route
@views.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
        
# Login page route
@views.route('/auth-view')
def auth_view():
    try:
        return render_template('login.html')
    except TemplateNotFound:
        abort(404)
# Dashboard Page Route
@views.route('/dashboard', methods=['GET'])
def dash_view():
    if auth.current_user != None:
        return render_template('dashboard-user.html')
    return render_template('login.html', user_not_authenticated=True)        

@views.route('/authenticate', methods=['GET','POST'])
def authenticate():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email == 'admin@angels4kings.com':
            # Authenticate as admin
            try:
                # Login the user
                user = auth.sign_in_with_email_and_password(email, password)
                
                # Set the session
                user_id = user['idToken']
                user_email = email
                session['usr'] = user_id
                session['email'] = email
                
                # Redirect admin to admin dashboard
                return render_template("dashboard-admin.html", success_message='You have successfully logged in')
                
            except:
                return render_template('login.html', error_message="Bad credentials. Contact the administrator")
        else:
            # Authenticate as user
            try:
                # Login the user
                user = auth.sign_in_with_email_and_password(email, password)
                
                # Set the session
                user_id = user['idToken']
                user_email = email
                session['usr'] = user_id
                session['email'] = email
                
                # Redirect regular user to user dashboard
                return render_template("dashboard-user.html", success_message='You are logged in successfully to angels paradise')
                
            except:
                return render_template('login.html', error_message="Bad credentials. Contact the administrator")
    
    return render_template('login.html')
   
# Logout page route  
@views.route('/logout')
def logout():
    # remove the token setting the user to None
    auth.current_user = None
    # Clear session
    session.clear()
    
    # Redirect the user to the login page with a success message
    return render_template('index.html', success_message='You have successfully logged out from Angels Paradise')
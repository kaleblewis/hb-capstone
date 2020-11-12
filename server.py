"""Server for online viewing recommendations app."""

import crud
from model import connect_to_db
import os
import datetime
from flask import (Flask, render_template, request, flash, session, redirect, 
    url_for)
from flask.json import jsonify
from jinja2 import StrictUndefined
# from google.oauth2 import service_account
# import google.oauth2.credentials


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = '''service_account.Credentials.from_service_account_file(
    'secrets.sh')'''
#netflix api key =  ~approx:  os.environ....  (import sys <?)
# credentials = google.oauth2.credentials.Credentials(
#     'access_token',
#     refresh_token='refresh_token',
#     token_uri='token_uri',
#     client_id='client_id',
#     client_secret='client_secret')


@app.route('/')
def homepage():
    """View homepage."""

    try:
        session['name']
        return render_template("homepage.html")                             
    except KeyError:
        return render_template("homepage.html")


@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_all_users()

    return render_template('all_users.html', users=users)


@app.route('/profile')                                                             #@maybe render a more unique route? ('/users/<id>')
def show_user():
    """Show details for one particular user."""

    login_user = crud.get_user_by_email(session['email'])

    if login_user:
        return render_template('profile.html', user=login_user)  

    else:
        flash(f'Your account was not found, please login or create an account')
        session['name'] = 'no-account-found-please-create-account'
        return redirect('/')


@app.route('/login', methods=['POST'])
def user_login():

    email = request.form.get('email-input')
    password = request.form.get('password-input')

    login_user = crud.get_user_by_email(email)

    if login_user:
        if login_user.password == password:
            flash('Success')
            session['name'] = login_user.fname
            session['email'] = email
            session['isNew'] = False
            session['loggedIn'] = True
            return redirect('/')    

        else:
            flash(f'Wrong password, try again')
                                                                                # TODO password counter: session['password-counter'] = session['password-counter'] + 1
                                                                                # flash(f'You entered an incorrect password'+{session['password-counter']}+'times(s).')
            return redirect('/')

    else:
        flash(f'Your account was not found, please create one')
        session['name'] = 'no-account-found-please-create-account'
        return redirect('/')

                                                                                # TODO password counter: build login lockout with auto refresh later
                                                                                        # if session exists ['password-counter'] < 6:
                                                                                            # (wrap all of the login code here?)
                                                                                        # else:
                                                                                        #     flash(f'You will be able to reload this page and try again in 5 minutes')           


@app.route('/newuser', methods=['POST'])
def register_user():
    """Create new user"""

    fname = request.form.get('name-input')
    email = request.form.get('email-input')
    password = request.form.get('password-input')
    password2 = request.form.get('password-input-2')

    new_user = crud.get_user_by_email(email)

    if password != password2:
        flash(f"The passwords you entered do not match, please try again")
        return redirect('/')

    elif new_user:

        if new_user.password == password:
            flash(f"Thanks, {fname} but you already have an account with that same password")  #TODO debug issue where fplks receive the 
            flash(f"You have successfully logged in to your account")           # // TODO fix bug msg scenario where someone gets stuck in loop if they enter existing Username/password within /newuser
            session['name'] = fname
            session['email'] = email
            session['isNew'] = False
            session['loggedIn'] = True
            return redirect('/')

        else:
            flash(f"Thanks, {fname} but you already have an account with that same email")
            flash(f"Please login to your existing account")                 
            session['name'] = fname
            session['email'] = email
            session['isNew'] = False
            session['loggedIn'] = False
            return redirect('/login')

    else:
        crud.create_user(fname, email, password)
        flash("You now have an account")
        session['name'] = fname
        session['email'] = email
        session['isNew'] = True  
        session['loggedIn'] = True                                               #this way we can display dynamic content to users who are new to the site
                                                                                # TODO password counter: reset counter when login successful:  session['password-counter'] = 0 
        return redirect('/')


@app.route('/recommendations')
def recommendations_page():
    """View recommendations page"""

    try:
        session['loggedIn'] = True
        return render_template("recommendations.html")                             
    except KeyError:
        return render_template('homepage.html')                                 # TODO debug: when user clicks form homepage, to recommendations, and homepage re-renders *OR* redirects, jinja kicks an error even though page loads fine directly""
                                                                                                # # jinja2.exceptions.UndefinedError: 'flask.sessions.SecureCookieSession object' has no attribute 'name'
                                                                                                # ....
                                                                                                #  File "/home/vagrant/src/project/env/lib/python3.6/site-packages/flask/templating.py", line 120, in _render
                                                                                                # rv = template.render(context)
                                                                                                # File "/home/vagrant/src/project/env/lib/python3.6/site-packages/jinja2/environment.py", line 1090, in render
                                                                                                # self.environment.handle_exception()
                                                                                                # File "/home/vagrant/src/project/env/lib/python3.6/site-packages/jinja2/environment.py", line 832, in handle_exception
                                                                                                # reraise(*rewrite_traceback_stack(source=source))
                                                                                                # File "/home/vagrant/src/project/env/lib/python3.6/site-packages/jinja2/_compat.py", line 28, in reraise
                                                                                                # Open an interactive python shell in this frameraise value.with_traceback(tb)
                                                                                                # File "/home/vagrant/src/project/templates/homepage.html", line 1, in top-level template code
                                                                                                # {% extends 'base.html' %}
                                                                                                # File "/home/vagrant/src/project/templates/base.html", line 62, in top-level template code
                                                                                                # {% block body %}
                                                                                                # File "/home/vagrant/src/project/templates/homepage.html", line 10, in block "body"
                                                                                                # {% if session['name'] == 'no-account-found-please-create-account' %}
                                                                                                # jinja2.exceptions.UndefinedError: 'flask.sessions.SecureCookieSession object' has no attribute 'name'



@app.route('/search', methods=['POST'])
def render_specific_movie(search_terms):
    """Serve up *one* search result based on user's specific input parameters"""
    
    search_result = get_by_filmid((search_by_id(search_by_title(search_terms))))

    return render_template("recommendations.html", 
        current_recommendations=search_result)    


@app.route('/random', methods=['POST'])
def render_random_top_3_results():                        
    """Serve up top 3 randomly selected results"""
    
    #crud.search_random_top_3_results(....include params here....)

    return render_template("recommendations.html")    


@app.route('/newrecommendations', methods=['POST'])
def render_x_movies_based_on_y_preferences():                                          # TODO:  what params?
    """Serve up top X recommended results based on Y preferences"""

    #crud.search_x_movies_based_on_y_preferences(....include params here....)

    return render_template("recommendations.html")    


@app.route('/previousrecommendations')
def get_all_query_history():                                                
    """Render all of a users's previous searches from the QueryHistory table"""

    #crud.search_all_query_history(....include params here....)

    return render_template("recommendations.html")    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


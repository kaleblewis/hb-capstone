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

LANGUAGES = {"audio": ["Arabic", "Cantonese", "Croatian", "English", "Filipino", "French", "German", "Gujarati", "Hebrew", "Hindi", "Italian", "Japanese", "Khmer", "Korean", "Mandarin", "Persian", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", "Tagalog", "Thai", "Urdu", "Vietnamese", "Yiddish"], "subtitles": ["Croatian", "English", "Filipino", "French", "German", "Hebrew", "Hindi", "Italian", "Japanese", "Korean", "Persian", "Polish", "Portuguese", "Russian", "Spanish", "Tagalog", "Thai", "Traditional Chinese", "Vietnamese"]}

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


#*############################################################################*#
#*#                                   USER                                   #*#
#*############################################################################*#

@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_all_users()

    return render_template('all_users.html', users=users)


@app.route('/profile')                                                             #@maybe render a more unique route? ('/users/<id>')
def show_user():
    """Show details for one particular user."""

    login_user = crud.get_user_by_email(session['email'])
    all_genres = crud.get_stored_genres()
    user_preferred_genres = crud.get_user_genre_preferences_active(login_user)

    if login_user:
        return render_template('profile.html', user=login_user, \
            all_genres=all_genres, user_genres = user_preferred_genres, \
            languages=LANGUAGES)

    else:
        flash(f'Your account was not found, please login or create an account')
        session['name'] = 'no-account-found-please-create-account'
        return redirect('/')


@app.route("/updateuserfname", methods=["POST"])
def update_user_fname():
    """Allow user to update their own fname from their profile screen."""
    
    existing_user = crud.get_user_by_email(session['email'])
    fname = request.form.get('name-input')

    crud.update_user_fname(existing_user.id, fname)

    session['name'] = fname
    flash(f"Your name has been successfully updated to: ''{fname}''")

    return redirect('/profile')


# @app.route("/updateuserpurl", methods=["POST"])
# def update_user_purl():
#     """Update user unique PURL parameter from their profile screen."""
    
#     existing_user = crud.get_user_by_email(session['email'])
#     purl_name = request.form.get('purl-name-input')

#     crud.update_user_purl(existing_user.id, purl_name)

#     flash(f"Your shareable personalized URL for networking with friends &\
#         family has been updated to:  www.blah.blah/{purl_name}")

#     return redirect('/profile')


@app.route("/updateuseremail", methods=["POST"])
def update_user_email():
    """Allow user to update their own email from their profile screen."""
    
    existing_user = crud.get_user_by_email(session['email'])
    email = request.form.get('email-input')

    crud.update_user_email(existing_user.id, email)

    session['email'] = email
    flash(f"Your email has been successfully updated to: ''{email}''")

    return redirect('/profile')


@app.route("/updateuserpassword", methods=["POST"])
def update_user_password():
    """Allow user to update their own password from their profile screen."""

    current_pw = request.form.get('current-password')
    new_pw_1 = request.form.get('new-password-1')
    new_pw_2 = request.form.get('new-password-2')

    existing_user = crud.get_user_by_email(session['email'])
    
    if existing_user:

        if existing_user.password == current_pw:

            if new_pw_1 == new_pw_2:

                crud.update_user_password(existing_user.id, new_pw_1)

                flash(f"Your password has been successfully updated")
                flash(f"Please login with your new password")
                session['logged_in'] = False

                return redirect('/')

            else:
                flash(f"sorry, the new passwords you entered do not match")
                flash(f"please try again")

                return redirect('/profile')
        
        else:
            flash(f"sorry, the current password you entered is not accurate")
            flash(f"please try again")

            return redirect('/profile')
    
    else:
        return redirect('/')


@app.route('/adduserpreferences', methods=['POST'])
def register_user_preferences():
    """Set a new entry for a group of a user's current preferences"""

    existing_user = crud.get_user_by_email(session['email']) 
    param_subtitle = request.form.get('preferred-subtitle') #request.form.get('subtitle-input')
    param_audio = request.form.get('preferred-audio') #request.form.get('audio-input')
    param_genre = request.form.get('genre-input')
    param_release_date_start = request.form.get('date-range-start')
    param_release_date_end = request.form.get('date-range-end')
    param_duration = request.form.get('duration-input')
    param_matlevel = request.form.get('matlevel-input')
    param_viewing_location = request.form.get('viewing-location-input')

    crud.add_user_preference_to_preferences(existing_user, param_subtitle,                 # TODO:  what params?
    param_audio, param_genre, param_release_date_start, 
    param_release_date_end, param_duration)
    
    flash("Your preferences have been updated")
    session['has_default_preferences'] = True                                      #this way we can display dynamic content to users who are new to the site
                                                                                # TODO password counter: reset counter when login successful:  session['password-counter'] = 0 
    return redirect('/profile')


#*############################################################################*#
#*#                       USER  LOGIN/LOGOUT/CREATION                        #*#
#*############################################################################*#

@app.route("/login", methods=["GET"])
def login_redirect():
    """Show login form."""     
    # mostly just so that the route doesn't bomb out if someone enters it manually                     
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
            session['logged_in'] = True
            return redirect('/')    

        else:
            flash(f'Wrong password, try again')
            return redirect('/')

    else:
        flash(f'please create an account')
        return redirect('/newuser')
      

@app.route("/existinguser", methods=["GET"])
def show_login():
    """Show sign-up form."""

    session['logged_in'] = False
    session['name'] = ''
    return redirect('/')  


@app.route("/newuser", methods=["GET"])
def show_sign_up():
    """Show sign-up form."""

    session['name'] = 'no-account-found-please-create-account'
    session['logged_in'] = False
    return redirect('/')  


@app.route('/createuser', methods=['POST'])
def register_user():
    """Create new user"""

    fname = request.form.get('name-input')
    email = request.form.get('email-input')
    password = request.form.get('password-input')
    password2 = request.form.get('password-input-2')

    existing_user = crud.get_user_by_email(email)
    
    if password != password2:
        flash(f"The passwords you entered do not match, please try again")
        return redirect('/')

    elif existing_user:

        if existing_user.password == password:
            flash(f"Thanks, {fname} but you already have an account with that same password")
            flash(f"You have successfully logged in to your existing account")
            session['name'] = fname
            session['email'] = email
            session['isNew'] = False
            session['logged_in'] = True
            return redirect('/')

        else:
            flash(f"Thanks, {fname} but you already have an account with that same email")
            flash(f"Please login to your existing account")                 
            session['name'] = fname
            session['email'] = email
            session['isNew'] = False
            session['logged_in'] = False
            return redirect('/')

    else:
        crud.create_user(fname, email, password)
        existing_user = crud.get_user_by_email(email)
        crud.add_user_preference_to_preferences(existing_user)
        flash("You now have an account")
        session['name'] = fname
        session['email'] = email
        session['isNew'] = True  
        session['logged_in'] = True  
        # ^ allows ability to display unique/dynamic content to 1st time users 
        return redirect('/')


@app.route("/logout")
def logout():
    """Log a user out"""
    session['logged_in'] = False
    flash('You have logged out successfully')
    return render_template('homepage.html') 


#*############################################################################*#
#*#                     CONTENT/SEARCHES/RECOMMENDATIONS                     #*#
#*############################################################################*#

@app.route('/recommendations')
def recommendations_page():
    """View recommendations page"""

    try:
        session['logged_in'] = True
        return render_template("recommendations.html")                             
    except KeyError:
        return render_template('homepage.html')                                 


@app.route('/search', methods=['POST'])
def render_specific_movie():
    """Serve up *one* search result based on user's specific input parameters"""

    search_term = request.form.get('search-input')
    search_result = crud.get_movie_details_by_filmid((crud.search_by_id(\
        crud.search_by_title(search_term))))

    if search_result['imdbid'] != '':
        flash(f"{search_term}")
        return render_template("recommendations.html", 
        current_recommendations=search_result)

    else:
        flash(f"...crickets chirping....  	🦗")
        flash(f"try a different search term, {session['name']}?")
        return redirect('/')                                                    # TODO:  debug why this works successfully if searching from '/' page
                                                                                #        but results in keyerror on [imdbID] if User is searching from '/search' page 


# @app.route('/random', methods=['POST'])
# def render_random_top_3_results():                        
#     """Serve up top 3 randomly selected results"""
    
#     #crud.search_random_top_3_results(....include params here....)

#     return render_template("recommendations.html")    


# @app.route('/newrecommendations', methods=['POST'])
# def render_x_movies_based_on_y_preferences():                                          # TODO:  what params?
#     """Serve up top X recommended results based on Y preferences"""

#     #crud.search_x_movies_based_on_y_preferences(....include params here....)

#     return render_template("recommendations.html")    


# @app.route('/previousrecommendations')
# def get_all_query_history():                                                
#     """Render all of a users's previous searches from the QueryHistory table"""

#     #crud.search_all_query_history(....include params here....)

#     return render_template("recommendations.html")    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


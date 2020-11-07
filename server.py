"""Server for online viewing recommendations app."""

import crud
from model import connect_to_db
import datetime
from flask import (Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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


@app.route('/user')                                                             #@maybe render a more unique route? ('/users/<id>')
def show_user(id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(id)

    return render_template('user.html', user=user)


@app.route('/login', methods=['POST'])
def user_login():

    email = request.form.get('email-input')
    password = request.form.get('password-input')

    login_user = crud.get_user_by_email(email)

    if login_user:
        if login_user.password == password:
            flash('Success')
            session['name'] = fname
            session['email'] = email
            session['isNew'] = False
            session['loggedIn'] = True    

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
            return redirect('/')

        else:
            flash(f"Thanks, {fname} but you already have an account with that same email")
            flash(f"Please login to your existing account")                 
            session['name'] = fname
            session['email'] = email
            session['isNew'] = False
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


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

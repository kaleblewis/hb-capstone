"""Server for online viewing recommendations app."""

# import crud
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

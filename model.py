"""Models for online viewing recommendations app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # netflix_id = db.Column(db.String) #ForeignKey Netflix
    fname = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))
    user_since = db.Column(db.DateTime)
    # mobile = db.Column(db.String(15))
    # SMS_allowed = db.Column(db.DateTime)
    # SMS_allowed_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} email={self.email}>'


class Connections(db.Model):
    """A User's social connections with other Users."""

    __tablename__ = 'connections'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    requestee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20))
    connection_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} status={self.status} requestor_id:{self.requestor_id} requestee_id:{self.requestee_id}>'


class Preference(db.Model):
    """A user's default preferences."""

    __tablename__ = 'preferences'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    preferred_app_lang = db.Column(db.String(50))
    default_subtitle = db.Column(db.String)
    default_dubbing = db.Column(db.String)
    default_genre = db.Column(db.String)
    default_release_date_start = db.Column(db.String(20))
    default_release_date_end = db.Column(db.String(20))
    default_duration = db.Column(db.Integer)

    user = db.relationship('User', backref='preferences')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} related to user_id={self.user_id}>'    # ? is this ok?  should i include more/less/other info here?
                                                                                                # TODO convert to <80 chars/line

class QueryHistory(db.Model):
    """A user's history of queries which were already run."""

    __tablename__ = 'query_history'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    query_run_date_time = db.Column(db.DateTime)
    query_string = db.Column(db.String)                                                         # ? should this be "text" or "string"
    payload = db.Column(db.String)                                                              # ? should this be "text" or "string"
    param_subtitle = db.Column(db.String)
    param_dubbing = db.Column(db.String)
    param_genre = db.Column(db.String)
    param_release_date = db.Column(db.String(20))
    param_duration = db.Column(db.Integer)
    param_total_seasons = db.Column(db.String(20))

    user = db.relationship('User', backref='query_history')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} related to user_id={self.user_id}>'    # ? is this ok?  should i include more/less/other info here?
                                                                                                # TODO convert to <80 chars/line

def connect_to_db(flask_app, db_uri='postgresql:///recommendations', echo=True):                # ? doublecheck this URL
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # * NOTE: Call connect_to_db(app, echo=False) if your program output gets
    # * too annoying; this will tell SQLAlchemy not to print out every
    # * query it executes.

    connect_to_db(app)
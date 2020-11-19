"""Models for online viewing recommendations app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    netflix_id = db.Column(db.String) #ForeignKey --> Netflix
    status = db.Column(db.Integer)
    fname = db.Column(db.String(50))
    #purl_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    user_since = db.Column(db.DateTime, nullable=False)
    mobile = db.Column(db.String(15))
    SMS_allowed = db.Column(db.DateTime)
    SMS_allowed_date = db.Column(db.DateTime)
    #viewing_location_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} email={self.email}>'


class UserNetwork(db.Model):
    """A User's social connections with other Users."""

    __tablename__ = 'user_network'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    requestee_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
        nullable=False)
    status = db.Column(db.String(20), nullable=False)
    connection_date = db.Column(db.DateTime, nullable=False)

    requestor = db.relationship('User', foreign_keys=[requestor_id])
    requestee = db.relationship('User', foreign_keys=[requestee_id])

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} status={self.status} \
            requestor_id:{self.requestor_id} requestee_id:{self.requestee_id}>'


class Preference(db.Model):
    """A user's default preferences."""

    __tablename__ = 'preferences'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preferences_set_date_time = db.Column(db.DateTime)
    preferred_app_lang = db.Column(db.String(50))
    default_subtitle = db.Column(db.String)
    default_audio = db.Column(db.String)
    default_genre = db.Column(db.String)
    default_release_date_start = db.Column(db.String(20))
    default_release_date_end = db.Column(db.String(20))
    default_duration = db.Column(db.Integer)
    #rating = db.Column(db.String)
    #viewing_location_id = db.Column(db.Integer)  
    # #strip out all the "default"?
    #match field names to API field names?
    
    user = db.relationship('User', backref='preferences')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} \
            related to user_id={self.user_id}>'    


class QueryHistory(db.Model):
    """A user's history of queries which were already run."""

    __tablename__ = 'query_history'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query_run_date_time = db.Column(db.DateTime)
    query_string = db.Column(db.Text)
    payload = db.Column(db.Text)
    param_subtitle = db.Column(db.String)
    param_audio = db.Column(db.String)
    param_genre = db.Column(db.String)
    param_release_date_start = db.Column(db.String(20))
    param_release_date_end = db.Column(db.String(20))
    param_duration = db.Column(db.Integer)
    param_total_seasons = db.Column(db.String(20))

    user = db.relationship('User', backref='query_history')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} \
            related to user_id={self.user_id}>'


def connect_to_db(flask_app, db_uri='postgresql:///recommendations', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print(' ✅ Connected to the db!')


if __name__ == '__main__':
    from server import app

    # * NOTE: Call connect_to_db(app, echo=False) if your program output gets
    # * too annoying; this will tell SQLAlchemy not to print out every
    # * query it executes.

    connect_to_db(app)
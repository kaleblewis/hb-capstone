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
    purl_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    user_since = db.Column(db.DateTime, nullable=False)
    mobile = db.Column(db.String(15))
    SMS_allowed = db.Column(db.DateTime)
    SMS_allowed_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} email={self.email}>'


class Location(db.Model):
    """A user's location (where Netflix streaming is available)."""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)  #NF's country code #'s
    name = db.Column(db.String(50))
    abbr = db.Column(db.String(3))
    default_subtitle = db.Column(db.String)
    default_audio = db.Column(db.String)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} location={self.name}>'    


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
    subtitle = db.Column(db.String)
    audio = db.Column(db.String)
    genre = db.Column(db.String)
    syear = db.Column(db.String(20)) #start date for release date range
    eyear = db.Column(db.String(20)) #end date for release date range
    duration = db.Column(db.Integer) #called 'duration' in API response
    matlevel = db.Column(db.String) #maturity level/rating
    viewing_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    location = db.relationship('Location', backref='preferences')
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
    query_result = db.Column(db.Text)
    param_viewing_location = db.Column(db.String)
    param_subtitle = db.Column(db.String)
    param_audio = db.Column(db.String)
    param_start_year = db.Column(db.String)
    param_end_year = db.Column(db.String)
    param_start_rating = db.Column(db.String)
    param_end_rating = db.Column(db.String)
    movie_or_series = db.Column(db.String)
    param_genre = db.Column(db.String)

    user = db.relationship('User', backref='query_history')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} \
            related to user_id={self.user_id}>'


# WELL, NETFLIX AND THE UNOGS API BOTH USE STRINGS FOR THESE
# class Subtitle(db.Model):
#     """Available Netflix subtitle languages."""

#     __tablename__ = 'subtitles'

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     name = db.Column(db.String(50))
    
#     user = db.relationship('Preference', backref='subtitles')

#     def __repr__(self):
#         return f'<{self.__class__.__name__} id={self.id} \
#             Location={self.user_id}>'    


# class Audio(db.Model):
#     """Available Netflix audio languages."""

#     __tablename__ = 'audios' #yeah, well, in English singular/plural is weird.

#     id = db.Column(db.Integer, autoincrement=True,primary_key=True) 
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     name = db.Column(db.String(50))
#     default_subtitle = db.Column(db.String)
    
#     user = db.relationship('User', backref='preferences')

#     def __repr__(self):
#         return f'<{self.__class__.__name__} id={self.id} \
#             Location={self.user_id}>'    


class Genre(db.Model):
    """A Netflix genre."""

    __tablename__ = 'genres'

    name = db.Column(db.Text, primary_key=True, nullable=False) #yes, this is pk
    id = db.Column(db.Text, nullable=False)# yes, text, i know, and not pk

    def __repr__(self):
        return f'<{self.__class__.__name__} genre_name_as_pk={self.name} list_of_ids={self.id}>'


class GenrePreference(db.Model):
    """A Users preferred genre(s)."""

    __tablename__ = 'genre_preferences'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    genre_name = db.Column(db.Text, db.ForeignKey('genres.name'), nullable=False)
    isActive = db.Column(db.Boolean) 

    user = db.relationship('User', backref='genre_prefs')
    genres = db.relationship('Genre', backref='genre_prefs')

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} user={self.user_id} \
            genre_name={self.genre_name} isActive={self.isActive}>'


class TmdbKeyword(db.Model):
    """A TMDB Keyword."""

    __tablename__ = 'tmdb_keywords'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} name={self.keyword}>'


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
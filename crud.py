"""CRUD operations."""

from model import db, User, Preference, QueryHistory, connect_to_db
import datetime


#*############################################################################*#
#*#                             USER OPERATIONS                              #*#
#*############################################################################*#

def create_user(name, email, password):
    """Create and return a new user.

    >>> create_user('jane', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    >>> create_user('', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    >>> create_user('jane', '', 'password1')
    # TODO: update docstring

    >>> create_user('jane', 'jane.doe@email.com', '')
    # TODO: update docstring

    user cannot pass a name that's other than alpha chars
    >>> create_user('1', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    >>> create_user('@', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    user cannot pass an email that's not an email
    >>> create_user('jane', 'jane.doe', 'password1')
    # TODO: update docstring

    >>> create_user('jane', 'janedoe@emailcom', 'password1')
    # TODO: update docstring

    >>> create_user('jane', '@.', 'password1')
    # TODO: update docstring

    name cannot be > 50 chars:
    >>> create_user('jane12345678901234156789012345678901234567890123415678901234567890123456789012345', 'jane.doe@email.com', 'password1')
    # TODO: update docstring

    email cannot be > 80 chars:
    >>> create_user('jane', 'jane.doe@email.com123456789012341567890123456789012345678901234156789012345678901', 'password1')
    # TODO: update docstring

    password cannot be > 20 chars:
    >>> create_user('jane', 'jane.doe@email.com', 'password1234567890123')
    # TODO: update docstring

    if user already exists, do not duplicate, simply log them in instead:
    >>> create_user('jane', 'jane.doe@email.com', 'password1')
    # TODO: update docstring
    """
    
                                                                                # TODO: add steps to first check if unique user exists based on email, if so, fail gracefully and simply log them in to their existing account w/o creating new user

    user = User(fname=name, 
                email=email, 
                password=password,
                user_since = datetime.datetime.now())

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Return a user by unique email address.
    
    >>> get_user_by_email(jane.doe@email.com)
    <User id=1 email=jane.doe@email.com>
    """

    return User.query.filter(User.email == email).first()                       


#*############################################################################*#
#*#                      USER CONNECTIONS OPERATIONS                         #*#
#*############################################################################*#

def add_user_connection(user, requestee):                                       # // TODO:  what params?
    """Create and store a user's social network connection invitation.

    new connection should get created:
    >>> add_user_connection(1, 2)
    <connections id=1 status="Pending" requestor_id:1 requestee_id:2>           # TODO: validate docstring response

    user shouldn't be both requestor and requestee                              # TODO:  add in this logic with if statement?
    >>> add_user_connection(1, 2)
    <connections id=1 status="Pending" requestor_id:1 requestee_id:2>           # TODO: validate docstring response

    only one record should exist per requestor+requestee+status combination     # TODO:  add in this logic with if statement?
    >>> add_user_connection(1, 2)
    <connections id=1 status="Pending" requestor_id:1 requestee_id:2>           # TODO: validate docstring response
    """

    user_connection = Connections(                                              # // TODO:  what params?
        requestee_id = requestee_id,
        status = "Pending",
        connection_date = datetime.datetime.now()
        )                   

    db.session.add(user_connection)
    db.session.commit()

    return user_connection

# def update_user_connection_by_id(connection_id):
#     """Update a User Connection by primary key

#     # TODO: update docstring with doctest
#     """

#     pass


def get_connections_by_user(user):                                              # TODO: implement new feature later to update/"approve" pending connection requests
    """Return all of a User's requested connections.

    Should return all requested connections, regardless of outcome/status.

    # TODO: update docstring with doctest
    """

    return Connections.query.filter(Connections.requestor_id == (User.query.get(id)))

    
# def get_pending_connections_by_user(user):                                    # TODO: implement new feature later to approve pending connection requests
#     """Return all pending connections where User is the Requestee.

#     Should return only the connections where:
#         Connections.Requestee_ID == User.ID
#         Connections.status = "Pending"

#     # TODO: update docstring with doctest
#     """

#     pass                                                    


#*############################################################################*#
#*#                      USER PREFERENCES OPERATIONS                         #*#
#*############################################################################*#

def add_user_preference_to_preferences(user, param_subtitle="",                 # TODO:  what params?
    param_dubbing="", param_genre="", param_release_date_start="", 
    param_release_date_end="", param_duration="", param_total_seasons=""):
    """Create and store a collection of User's default preferences"""

    user_preferences = Preferences(user_id = db.Column(db.Integer, 
            db.ForeignKey(User.query.get(id))),
        query_run_date_time = datetime.datetime.now(),
        query_string = query_string,
        payload = payload,
        param_subtitle = param_subtitle,
        param_dubbing = param_dubbing,
        param_genre = param_genre,
        param_release_date_start = param_release_date_start,
        param_release_date_end = param_release_date_end,
        param_duration = param_duration,
        param_total_seasons = param_total_seasons
        )                          

    db.session.add(user_preferences)
    db.session.commit()

    return user_preferences


# def get_user_preferences_specific_kvp():
#     """Return ONE SPECIFIC default preference of current User's preferences"""

#     pass                                                                      # TODO:  get only one value out of a specified col in the most recent row


# def get_user_preferences_current_collection():
#     """Return the most recent collection of this User's default preferences."""

#     pass                                                                      # TODO:  get only the most recent entry in the table, like, the largest ID?


def get_user_preferences_all_time(user):
    """Return all of the collections of this User's default preferences from forever ever."""

    return Preferences.query.filter(User.query.get(id))                        


#*############################################################################*#
#*#                            QUERY OPERATIONS                              #*#
#*############################################################################*#

# def search_specific_movie():                                                    # TODO:  what params?
#     """Allow user to search for content based on specific input parameters      # ? is there a better, more general term than "movie", TV shows count, too
    
#     """                                                                         # TODO:  update docstring with doctests      

#     pass                                                                        # TODO:  complete function stub 


# def get_single_result_by_id(movie_id):
#     """Return a single movie by primary key."""

#     pass                                                                        # TODO:  complete function stub 


# def search_random_top_3_results():                                                 # TODO:  what params?
#     """Allow user to search for top 3 randomly selected results
    
#     Should return top ranked result based on both:
#         1.) user default preferences (if any)
#         2.) content's avg review score ( sort by --> decending )
#         3.) if/when score is tied, then randomize to select only 3 

#     """                                                                         # TODO:  update docstring with doctests 

#     pass                                                                        # TODO:  complete function stub 


# def search_x_movies_based_on_y_preferences():                                          # TODO:  what params?
#     """Allow user to search for top X number of results 
    
#     Should return top ranked result based on both:
#         1.) user default preferences (if any)
#         2.) content's avg review score ( sort by --> decending )
#         3.) if/when score is tied, then randomize to select only top 10
#         4.) returning X qty selected by user

#     """                                                                         # TODO:  update docstring with doctests 

#     pass                                                                        # TODO:  complete function stub 


#*############################################################################*#
#*#                        QUERYHISTORY OPERATIONS                           #*#
#*############################################################################*#

def add_query_to_query_history(user, query_string, 
    payload, param_subtitle="", param_dubbing="", param_genre="", 
    param_release_date_start="", param_release_date_end="", param_duration="", 
    param_total_seasons=""):          # TODO:  what params?
    """Create a new entry in Query History with query results                   # TODO: update docstring with doctest
    """

    query = QueryHistory(user_id = (User.query.get(id)),
        query_run_date_time = datetime.datetime.now(),
        query_string = query_string,
        payload = payload,
        param_subtitle = param_subtitle,
        param_dubbing = param_dubbing,
        param_genre = param_genre,
        param_release_date_start = param_release_date_start,
        param_release_date_end = param_release_date_end,
        param_duration = param_duration,
        param_total_seasons = param_total_seasons
        )                   

    db.session.add(query)
    db.session.commit()

    return query


# def get_previous_query_from_history():                                          # TODO:  what params?
#     """Retreive only users's most recent search from the QueryHistory table"""  # TODO:  update docstring with doctests    

#     pass                                                                        # TODO:  complete function stub 


def get_all_query_history(user):                                                    # TODO:  what params?
    """Retreive all of a users's searches from the QueryHistory table"""        # TODO:  update docstring with doctests    

    return queryhistory.query.all(QueryHistory.user_id == (User.query.get(id))) # TODO:  complete function stub 


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
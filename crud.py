"""CRUD operations."""

from model import db, User, Preference, QueryHistory, Location, Genre, GenrePreference, TmdbKeyword, Watchlist, connect_to_db
import datetime
import os
import sys
import requests
import json
from flask.json import jsonify
import urllib, hashlib
from urllib.parse import quote, unquote
from sqlalchemy import update

TMDB_API_KEY = (os.environ.get('TMDB_API_KEY'))



#*############################################################################*#
#*#                             USER OPERATIONS                              #*#
#*############################################################################*#

def create_user(name, email, password):
    """Create and return a new user.

    >>> create_user('jane', 'jane.doe@email.com', 'password1')
    <User id=1 email=jane.doe@gmail.com>
    """
    
    user = User(fname=name, 
                email=email, 
                password=password,
                user_since = datetime.datetime.now())

    db.session.add(user)
    db.session.commit()  #TODO:  going to need to loop through a second pass to set PURL_name = User.ID

    return user


def get_user_by_email(email):
    """Return a user by unique email address.
    
    >>> get_user_by_email('jane.doe@email.com')
    <User id=1 email=jane.doe@email.com>
    """

    return User.query.filter(User.email == email).first()    
                       

def update_user_fname(user_id, name):
    """Update the fname of an existing user.
    
    The new name will be captured via user input field.

    >>> update_user_fname("1", "wombat")
    <User id=1 email=jane.doe@email.com>
    """

    user = User.query.get(user_id)
    user.fname = name
    db.session.commit()

    return user

def update_user_email(user_id, email):
    """Update the email of an existing user.
    
    The new email will be captured via user input field.
    Validation will happen upstream.

    >>> update_user_email("1", "wombat@email.com")
    <User id=1 email=wombat@email.com>
    """

    user = User.query.get(user_id)
    user.email = email
    db.session.commit()

    return user

def update_user_password(user_id, password):
    """Update the password of an existing user.
    
    The new password will be captured via user input field.
    Validation will happen upstream.

    >>> update_user_password("1", "wombat")
    'success'
    """

    user = User.query.get(user_id)
    user.password = password
    db.session.commit()

    return "success"

def get_user_gravitar(user_email):
    """Fetch user info/photo from Gravitar."""
    #https://libgravatar.readthedocs.io/en/latest/
    #https://en.gravatar.com/site/implement/profiles/json/
    #https://en.gravatar.com/site/implement/hash/

    email = user_email
    default = "https://www.example.com/default.jpg"
    size = 40
    
    # construct the url
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})


#*############################################################################*#
#*#                           USERNETWORK OPERATIONS                         #*#
#*############################################################################*#

def add_user_connection(requestee, user):
    """Create and store a user's social network connection invitation.

    # new connection should get created:
    >>> add_user_connection(1, 2)
    <UserNetwork id=1 status="Pending" requestor_id:1 requestee_id:2> 

    # user shouldn't be both requestor and requestee
    >>> add_user_connection(1, 2)
    <UserNetwork id=1 status="Pending" requestor_id:1 requestee_id:2> 

    # only one record should exist per requestor+requestee+status combination  
    >>> add_user_connection(1, 2)
    <UserNetwork id=1 status="Pending" requestor_id:1 requestee_id:2> 
    """

    user_connection = db.UserNetwork(requestor_id = user.id,
                                    requestee_id = requestee.id,
                                    status = "Pending",
                                    connection_date = datetime.datetime.now())                   

    db.session.add(user_connection)
    db.session.commit()

    return user_connection


# TODO: implement new feature later to update/"approve" pending connection requests
# def update_user_connection_by_id(connection_id):
#     """Update a UserNetwork by primary key

#     # TODO: update docstring with doctest
#     """

#     pass


# def get_connections_by_user(user):
#     """Return all of a User's requested connections.

#     Should return all requested connections, regardless of outcome/status.

#     # TODO: update docstring with doctest
#     """

#     return UserNetwork.query.filter(UserNetwork.requestor_id == (User.id))

    
# def get_pending_connections_by_user(user):
#     """Return all pending connections where User is the Requestee.

#     Should return only the connections where:
#         UserNetwork.Requestee_ID == User.ID
#         UserNetwork.status = "Pending"

#     # TODO: update docstring with doctest
#     """

#     pass                                                    


#*############################################################################*#
#*#                      USER PREFERENCES OPERATIONS                         #*#
#*############################################################################*#

def add_user_preference_to_preferences(user, param_subtitle="any",
    param_audio="any", param_genre="any", param_release_date_start="any", 
    param_release_date_end="any", param_duration=60, param_matlevel="any", 
    param_viewing_location=78):
    """Create and store a collection of User's default preferences"""

    genre_prefs = add_genre_preference(user, param_genre)

    user_preferences = Preference(
        preferences_set_date_time  = datetime.datetime.now(),
        user_id = user.id,
        subtitle = param_subtitle,
        audio = param_audio,
        genre = param_genre,
        syear = param_release_date_start,
        eyear = param_release_date_end,
        duration = param_duration,
        matlevel = param_matlevel,
        viewing_location_id = param_viewing_location)

    db.session.add(user_preferences)
    db.session.commit()

    return user_preferences


def add_title_to_watchlist(user, title_id):
    """Store a title to User's watchlist"""

    add_to_watchlist = Watchlist(
        added_date_time = datetime.datetime.now(),
        user_id = user.id,
        title_id = title_id)

    db.session.add(add_to_watchlist)
    db.session.commit()

    return user_preferences


def get_user_watchlist(user):
    """Return all of this User's watchlist."""

    user_watchlist = Watchlist.query.filter(User.id).all()                     

    return user_watchlist


def add_genre_preference(user, param_genre):
    """ Create a genre preference for a user.

    >>> add_genre_preference('1', '[7442]')
    <Preference id=1 related to user_id=1>
    """

    if param_genre == "" or param_genre == "any" or param_genre == "all":
        return "any"
    
    else:
        user_genre_preference = GenrePreference(
            user_id = user.id,
            genre_name = param_genre,
            isActive = True)

        db.session.add(user_genre_preference)
        db.session.commit()

        return GenrePreference.id


def get_current_user_preferences(user):
    """Return the most recent collection of this User's default preferences.
    
    >>> get_current_user_preferences('1')
    <Preference id=1 related to user_id=1>
    """
    
    current_user_prefs = Preference.query.filter(Preference.user_id==User.id).order_by(Preference.id.desc()).first()

    return current_user_prefs
    

def get_user_preferences_all_time(user):
    """Return all of the collections of this User's default preferences from forever ever."""

    all_user_prefs_all_time = Preference.query.filter(User.id).all()                     

    return all_user_prefs_all_time


def get_user_genre_preferences_active(user):
    """Return all of the collections of this User's default preferences from forever ever."""

    all_user_genre_prefs_active = GenrePreference.query.filter(GenrePreference.user_id==User.id, \
        GenrePreference.isActive != "false").all()                       

    return all_user_genre_prefs_active


def disable_genre_preference(user_id, genre_id):
    """ Disable a genre preference a user had stored previously.

    >>> disable_genre_preference('1', '[7442]')
    <GenrePreference id=1 user="1" genre='[7442]' isActive=False>'
    """

    user_genre_preference = GenrePreference.query.filter(user_id, genre_id, isActive != false).all()
    genre_prefs.isActive = False
    db.session.commit()

    return user_genre_preference


#*############################################################################*#
#*#                            QUERY OPERATIONS                              #*#
#*############################################################################*#

def search_films_by_parameters(current_user, genre_list, movie_or_series, start_rating, end_rating, start_year, end_year, subtitle, audio, country_list):  #new_year, 
    """ Return a number of results based on parameters from User.

    All of the front end parameters are optional.
    Ordering/sorting will be handled on the front end instead of via querystring parameter
    """

    url = "https://unogsng.p.rapidapi.com/search"

    # # correct any inadvertent start-date range mix-ups or inadvertent exclusions
    # if new_year < start_year:
    #     start_year = new_year

    # else:
    #     new_year = start_year

    # # NOT-SO-OPTIONAL PARAMETERS, ones that needed a little extra help
    # if start_year:
    #     new_date=f"{start_year}" + "-01-01"    # DATE (YYYY-MM-DD)  something new-ish where streaming began after this date 
     # TODO:  re-enable ^ this for "recently added" search parameter  

    country_list = "78" # comma-separated list of uNoGS country ID's 
    #(from country endpoint) leave blank for all country search
    # hard-coded "USA" for now 
    # TODO: flip this back to dynamic list value later

    order_by = "rating"     # orderby string (date,rating,title,type,runtime)
    limit = 10           # Limit of returned items default (MAX 100)
    offset = "0"            # Starting Number of results (Default is 0)



    parameter_list = {"genrelist": f"{genre_list}","type": f"{movie_or_series}",
    "start_year": f"{start_year}","orderby":"rating","start_rating": 
    f"{start_rating}","limit":f"{limit}","end_rating": f"{end_rating}",
    "subtitle": f"{subtitle}","countrylist":"78","audio": f"{audio}",
    "offset":"0","end_year": f"{end_year}","audiosubtitle_andor":"OR"}   #"newdate":f"{new_date}",
    # TODO:  re-enable ^ this for "recently added" search parameter

    querystring = {}

    # Fill in the entries one by one if they have values
    for key in parameter_list:
        if parameter_list[key]:
            if parameter_list[key] != "":
                querystring[key] = parameter_list[key]

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    response = requests.request("GET", url, headers=headers, params=querystring)

    #take the response and unpack it into a workable format
    search_results = json.loads(response.text)
    search_results_values = search_results.values()

    #extract the embedded dictionary from 2 levels down in results
    try:
        listify_results = list(search_results_values)
        result_list = listify_results[2]  

    except IndexError:
        return {"error": "your search was too specific and returned no results. please try again."}
        

    #then wrap it back into a dictionary using index/result number as key
    recommendations = dict()

    for index, movie in enumerate(result_list):
        recommendations[index + 1] = movie

    # store results, qstr, and login_user in the query_history table
    add_query_to_query_history(current_user, str(querystring), 
        str(recommendations), str(genre_list), movie_or_series, start_year, 
        end_year, subtitle, audio, str(country_list), start_rating, end_rating)

    return recommendations


def search_by_title(str):
    """ Pass movie title to unofficial imdb API to receive imdb 'id'.

    should begin with two alpha chars

    >>> search_by_title('the last unicorn')
    'tt0084237'
    """
    imdb_query_param = quote(str)

    imdb_url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{imdb_query_param}"
    # example looks like of a full url: 
    # "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/the%20last%20unicorn"

    imdb_headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
        }
    imdb_headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    imdb_response = requests.request("GET", imdb_url, headers=imdb_headers)

    imdb_list = []
    imdb_payload = json.loads(imdb_response.text)
    imdb_list.append(imdb_payload)

    imdb_dictionary = (imdb_list[0])

    return imdb_dictionary['id']


def search_by_id(str):
    """ Pass 'imdbid' to *unofficial* netflix API to receive netflix 'filmid'.

    Accepts string of alpha and numeric chars
        accepts parameter: 'imdbid' which begins with two alpha chars
        returns result: 'filmid' netflix id does not contain alpha chars

    >>> search_by_id('tt0084237')
    '60035334'

    >>> search_by_id(search_by_title('the last unicorn'))
    '60035334'
    """

    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"getimdb","q":f"{str}"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    n_response = requests.request("GET", url, headers=headers, params=querystring)

    n_list = []
    n_payload = json.loads(n_response.text)
    n_list.append(n_payload)

    n_dictionary = (n_list[0])

    return n_dictionary['filmid']


def get_by_filmid(str):
    """ Pass 'filmid' to receive title details.

    >>> get_by_filmid('60035334').keys()
    {"RESULT":{"nfinfo":{"image1":"https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg","title":"The Last Unicorn","synopsis":"This animated tale follows a unicorn who believes she may be the last of her species and is searching high and low for someone just like her.","matlevel":"35","matlabel":"Contains nothing in theme, language, nudity, sex, violence or other matters that, in the view of the Rating Board, would offend parents whose younger children view the motion picture","avgrating":"3.8214536","type":"movie","updated":"","unogsdate":"2015-07-10 01:09:00","released":"1982","netflixid":"60035334","runtime":"1h32m","image2":"https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg","download":"1"},"imdbinfo":{"rating":"7.5","votes":"23234","metascore":"70","genre":"Animation, Adventure, Drama, Family, Fantasy","awards":"1 nomination.","runtime":"92 min","plot":"From a riddle-speaking butterfly, a unicorn learns that she is supposedly the last of her kind, all the others having been herded away by the Red Bull. The unicorn sets out to discover the truth behind the butterfly&amp;#39;s words. She is eventually joined on her quest by Schmendrick, a second-rate magician, and Molly Grue, a now middle-aged woman who dreamed all her life of seeing a unicorn. Their journey leads them far from home, all the way to the castle of King Haggard...","country":"UK, France, West Germany, Japan, USA","language":"English, German","imdbid":"tt0084237"},"mgname":["Animal Tales","Family Sci-Fi & Fantasy","Children & Family Films","Films for ages 8 to 10","Films based on childrens books","Films for ages 11 to 12"],"Genreid":["5507","52849","783","561","10056","6962"],"people":[{"actor":["Alan Arkin","Jeff Bridges","Mia Farrow","Tammy Grimes","Angela Lansbury","Robert Klein","Keenan Wynn","Christopher Lee","Rene Auberjonois","Paul Frees","Jack Lester","Brother Theodore","Don Messick","Ed Peck","Kenneth Jennings","Nellie Bellflower"]},{"creator":["Peter S. Beagle"]},{"director":["Jules Bass","Arthur Rankin Jr."]}],"country":[]}}
    """
    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"getimdb","q":f"{str}"}                                  
    
    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    response = requests.request("GET", url, headers=headers, params=querystring)

    imdb_list = []
    imdb_payload = json.loads(response.text)
    imdb_list.append(imdb_payload)

    imdb_dictionary = imdb_list[0]
    imdb_dictionary['plot'] = unquote(imdb_dictionary['plot'])                  # TODO: Try to find other ways to get rid of goofy chars?

    return imdb_dictionary


def get_nfinfo_by_id(netflixid):
    """ Pass 'netflixid' to receive netflix information.

    Accepts string of numeric chars
        accepts parameter: 'filmid' netflix id does not contain alpha chars
        returns: dictionary of netflix info... most importantly: title

    >>> get_nfinfo_by_id('60035334')
    {'image1': 'https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg', 'title': 'The Last Unicorn', 'synopsis': 'This animated tale follows a unicorn who believes she may be the last of her species and is searching high and low for someone just like her.', 'matlevel': '35', 'matlabel': 'Contains nothing in theme, language, nudity, sex, violence or other matters that, in the view of the Rating Board, would offend parents whose younger children view the motion picture', 'avgrating': '3.8214536', 'type': 'movie', 'updated': '', 'unogsdate': '2015-07-10 01:09:00', 'released': '1982', 'netflixid': '60035334', 'runtime': '1h32m', 'image2': 'https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg', 'download': '1'}
    """
    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"loadvideo","q":f"{netflixid}"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    response = requests.request("GET", url, headers=headers, params=querystring)

    n_list = []
    n_payload = json.loads(response.text)
    n_list.append(n_payload)

    n_dictionary = n_list[0].values()
    new_list = list(n_dictionary)
    n_str_result = new_list[0]

    nfinfo = n_str_result['nfinfo']

    return nfinfo


def get_imdb_details_by_filmid(str):
    """ Pass 'filmid' to receive imbd details.

    >>> get_by_filmid('60035334')['poster']
    'https://images-na.ssl-images-amazon.com/images/M/MV5BOTBjOTg1ZmMtMjFlZi00ODkyLTkwOGMtY2FmNTc1MTEzMGQyXkEyXkFqcGdeQXVyMjA0MDQ0Mjc@._V1_SX300.jpg'
    """
    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"getimdb","q":f"{str}"} 

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    response = requests.request("GET", url, headers=headers, params=querystring)

    imdb_list = []
    imdb_payload = json.loads(response.text)
    imdb_list.append(imdb_payload)

    imdb_dictionary = (imdb_list[0])

    return imdb_dictionary


def get_movie_details_by_filmid(str):
    """Pass 'filmid' to receive all KVPs

    >>> get_movie_details_by_filmid('60035334')['image1']
    'https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg'
    """
    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"loadvideo","q":f"{str}"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    response = requests.request("GET", url, headers=headers, params=querystring)

    n_list = []
    n_payload = json.loads(response.text)
    n_list.append(n_payload)

    n_dictionary = n_list[0].values()
    new_list = list(n_dictionary)
    n_str_result = new_list[0]

    #extract a *dictionary* of the NETFLIX specific data 
    nfinfo = n_str_result['nfinfo']
    nfinfo['runtime'] = '' # <-- strip this runtime, it's a mash of hrs and mins

    #extract a *dictionary* of the IMDB specific data 
    imdbinfo = n_str_result['imdbinfo'] # <-- we get runtime in just mins here

    #combine the imdbinfo KVPs into one dictionary
    dictionary_results =  {}

    # Make sure every key of the 2 dictionaries get into the final dictionary
    dictionary_results.update(nfinfo)
    dictionary_results.update(imdbinfo)

    #extract and append key:value(list) of GENRE NAMES
    dictionary_results['mgname'] = n_str_result['mgname']

    #extract and append key:value(list) of GENRE IDs
    dictionary_results['genreid'] = n_str_result['Genreid']  
    #  yes, that's a capital "G" for some reason  ^

    #extract lists of humans
    people = n_str_result['people']

    #extract and append key:value(list) of ACTORS
    actors_values = people[0].values()
    actors_list = list(actors_values)
    dictionary_results['actors'] = actors_list[0]

    #extract and append key:value(list) of CREATORS
    creators_values = people[1].values()
    creators_list = list(creators_values)
    dictionary_results['creators'] = creators_list[0]

    #extract and append key:value(list) of DIRECTORS
    directors_values = people[2].values()
    directors_list = list(directors_values)
    dictionary_results['directors'] = directors_list[0]

    #extract and append key:value(list) of 'country'<-- whatever that represents
    dictionary_results['country'] = n_str_result['country']

    #return one big flattened dictionary of all of the KVPs from the API response
    return dictionary_results
    

def get_all_films_by_person_name(input_name):
    """ Get all films with a person's name. 

    Argument can be either a full name, surname, etc. 
    Argument must be an exact match for spelling and punctuation.
    No, you can't pass "the Prince symbol" here.

    Person should supposedly return any named production role, not just an actor: 
     - actor
     - director
     - creator
    (but apparently right now the API is actually only returning actors)

    >>> get_all_films_by_person_name("Britney Spears")  
    {'Britney Spears': [{'fullname': 'Britney Spears', 'netflixid': 60022266, 'title': 'Crossroads'}]}

    >>> get_all_films_by_person_name("Peter Ostrum")
    {'Peter Ostrum': [{'fullname': 'Peter Ostrum', 'netflixid': 60020949, 'title': 'Willy Wonka and the Chocolate Factory'}]}

    >>> get_all_films_by_person_name("Wachowski")
    {'Andy Wachowski': [{'fullname': 'Andy Wachowski', 'netflixid': 60031303, 'title': 'The Matrix Revolutions'}, {'fullname': 'Andy Wachowski', 'netflixid': 70039175, 'title': 'V for Vendetta'}, {'fullname': 'Andy Wachowski', 'netflixid': 326674, 'title': 'Bound'}, {'fullname': 'Andy Wachowski', 'netflixid': 70084796, 'title': 'Speed Racer'}, {'fullname': 'Andy Wachowski', 'netflixid': 265929, 'title': 'Assassins'}, {'fullname': 'Andy Wachowski', 'netflixid': 60027495, 'title': 'The Animatrix'}, {'fullname': 'Andy Wachowski', 'netflixid': 70301367, 'title': 'Jupiter Ascending'}, {'fullname': 'Andy Wachowski', 'netflixid': 80025744, 'title': 'Sense8'}, {'fullname': 'Andy Wachowski', 'netflixid': 70248183, 'title': 'Cloud Atlas'}, {'fullname': 'Andy Wachowski', 'netflixid': 20557937, 'title': 'The Matrix'}], 'Lana Wachowski': [{'fullname': 'Lana Wachowski', 'netflixid': 60031303, 'title': 'The Matrix Revolutions'}, {'fullname': 'Lana Wachowski', 'netflixid': 70039175, 'title': 'V for Vendetta'}, {'fullname': 'Lana Wachowski', 'netflixid': 326674, 'title': 'Bound'}, {'fullname': 'Lana Wachowski', 'netflixid': 70084796, 'title': 'Speed Racer'}, {'fullname': 'Lana Wachowski', 'netflixid': 265929, 'title': 'Assassins'}, {'fullname': 'Lana Wachowski', 'netflixid': 60027495, 'title': 'The Animatrix'}, {'fullname': 'Lana Wachowski', 'netflixid': 70301367, 'title': 'Jupiter Ascending'}, {'fullname': 'Lana Wachowski', 'netflixid': 80025744, 'title': 'Sense8'}, {'fullname': 'Lana Wachowski', 'netflixid': 70248183, 'title': 'Cloud Atlas'}, {'fullname': 'Lana Wachowski', 'netflixid': 20557937, 'title': 'The Matrix'}, {'fullname': 'Lana Wachowski', 'netflixid': 60027695, 'title': 'The Matrix Reloaded'}], 'Lilly Wachowski': [{'fullname': 'Lilly Wachowski', 'netflixid': 20557937, 'title': 'The Matrix'}, {'fullname': 'Lilly Wachowski', 'netflixid': 60027695, 'title': 'The Matrix Reloaded'}, {'fullname': 'Lilly Wachowski', 'netflixid': 60031303, 'title': 'The Matrix Revolutions'}, {'fullname': 'Lilly Wachowski', 'netflixid': 70084796, 'title': 'Speed Racer'}, {'fullname': 'Lilly Wachowski', 'netflixid': 70248183, 'title': 'Cloud Atlas'}, {'fullname': 'Lilly Wachowski', 'netflixid': 70301367, 'title': 'Jupiter Ascending'}, {'fullname': 'Lilly Wachowski', 'netflixid': 80025744, 'title': 'Sense8'}]}
    """

    url = "https://unogsng.p.rapidapi.com/people"

    querystring = {"name": f"{input_name}"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    response = requests.request("GET", url, headers=headers, params=querystring)

    #take the response and unpack it into a workable format
    person_results = json.loads(response.text)
    films_with_person = person_results.values()

    #extract the embedded dictionary from 2 levels down in results
    new_list = list(films_with_person)
    result_list = new_list[2]  

    dedeuplicated_list = []
    for movie in result_list:
        if movie not in dedeuplicated_list:
            dedeuplicated_list.append(movie)

    filmography = dict()

    for movie in dedeuplicated_list:
        if movie['fullname'] in filmography:
            filmography[movie['fullname']].append(movie)

        else:
            filmography[movie['fullname']]=[movie]

    return filmography
    

def get_top10_films_by_genre_name(current_user, genre_name):
    """ Get top-10 best rated films results for a particular genre

    Argument must be the name of a genre.
    Genre names can represent either:
     - One single genre  (eg. 'Social & Cultural Documentaries')
     - One group of related genres  (eg. 'All Documentaries')

    >>> get_all_films_by_person_name("Britney Spears")  
    {'Britney Spears': [{'fullname': 'Britney Spears', 'netflixid': 60022266, 'title': 'Crossroads'}]}

    >>> get_all_films_by_person_name("Peter Ostrum")
    {'Peter Ostrum': [{'fullname': 'Peter Ostrum', 'netflixid': 60020949, 'title': 'Willy Wonka and the Chocolate Factory'}]}

    >>> get_all_films_by_person_name("Wachowski")
    {'Andy Wachowski': [{'fullname': 'Andy Wachowski', 'netflixid': 60031303, 'title': 'The Matrix Revolutions'}, {'fullname': 'Andy Wachowski', 'netflixid': 70039175, 'title': 'V for Vendetta'}, {'fullname': 'Andy Wachowski', 'netflixid': 326674, 'title': 'Bound'}, {'fullname': 'Andy Wachowski', 'netflixid': 70084796, 'title': 'Speed Racer'}, {'fullname': 'Andy Wachowski', 'netflixid': 265929, 'title': 'Assassins'}, {'fullname': 'Andy Wachowski', 'netflixid': 60027495, 'title': 'The Animatrix'}, {'fullname': 'Andy Wachowski', 'netflixid': 70301367, 'title': 'Jupiter Ascending'}, {'fullname': 'Andy Wachowski', 'netflixid': 80025744, 'title': 'Sense8'}, {'fullname': 'Andy Wachowski', 'netflixid': 70248183, 'title': 'Cloud Atlas'}, {'fullname': 'Andy Wachowski', 'netflixid': 20557937, 'title': 'The Matrix'}], 'Lana Wachowski': [{'fullname': 'Lana Wachowski', 'netflixid': 60031303, 'title': 'The Matrix Revolutions'}, {'fullname': 'Lana Wachowski', 'netflixid': 70039175, 'title': 'V for Vendetta'}, {'fullname': 'Lana Wachowski', 'netflixid': 326674, 'title': 'Bound'}, {'fullname': 'Lana Wachowski', 'netflixid': 70084796, 'title': 'Speed Racer'}, {'fullname': 'Lana Wachowski', 'netflixid': 265929, 'title': 'Assassins'}, {'fullname': 'Lana Wachowski', 'netflixid': 60027495, 'title': 'The Animatrix'}, {'fullname': 'Lana Wachowski', 'netflixid': 70301367, 'title': 'Jupiter Ascending'}, {'fullname': 'Lana Wachowski', 'netflixid': 80025744, 'title': 'Sense8'}, {'fullname': 'Lana Wachowski', 'netflixid': 70248183, 'title': 'Cloud Atlas'}, {'fullname': 'Lana Wachowski', 'netflixid': 20557937, 'title': 'The Matrix'}, {'fullname': 'Lana Wachowski', 'netflixid': 60027695, 'title': 'The Matrix Reloaded'}], 'Lilly Wachowski': [{'fullname': 'Lilly Wachowski', 'netflixid': 20557937, 'title': 'The Matrix'}, {'fullname': 'Lilly Wachowski', 'netflixid': 60027695, 'title': 'The Matrix Reloaded'}, {'fullname': 'Lilly Wachowski', 'netflixid': 60031303, 'title': 'The Matrix Revolutions'}, {'fullname': 'Lilly Wachowski', 'netflixid': 70084796, 'title': 'Speed Racer'}, {'fullname': 'Lilly Wachowski', 'netflixid': 70248183, 'title': 'Cloud Atlas'}, {'fullname': 'Lilly Wachowski', 'netflixid': 70301367, 'title': 'Jupiter Ascending'}, {'fullname': 'Lilly Wachowski', 'netflixid': 80025744, 'title': 'Sense8'}]}
    """

    url = "https://unogsng.p.rapidapi.com/search"

    genre_id = str(get_genre_id_by_name(genre_name))
    genre_id = genre_id.replace('{','')
    genre_id = genre_id.replace('}','')

    parameter_list = {"genrelist": f"{genre_id}","orderby":"rating",
    "limit":"10"}  

    querystring = {}

    # Fill in the entries one by one if they have values
    for key in parameter_list:
        if parameter_list[key]:
            if parameter_list[key] != "":
                querystring[key] = parameter_list[key]

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    response = requests.request("GET", url, headers=headers, params=querystring)

    #take the response and unpack it into a workable format
    search_results = json.loads(response.text)
    search_results_values = search_results.values()

    #extract the embedded dictionary from 2 levels down in results
    try:
        listify_results = list(search_results_values)
        result_list = listify_results[2]  

    except IndexError:
        return {"error": "your search was too specific and returned no results. please try again."}
        

    #then wrap it back into a dictionary using index/result number as key
    recommendations = dict()

    for index, movie in enumerate(result_list):
        recommendations[index + 1] = movie

    # store results, qstr, and login_user in the query_history table
    add_query_to_query_history(current_user, str(querystring), 
        str(recommendations), str(genre_id), None, None, 
        None, None, None, None, None, None)

    return recommendations


#*############################################################################*#
#*#                        QUERYHISTORY OPERATIONS                           #*#
#*############################################################################*#

def add_query_to_query_history(current_user, querystring, query_results,
        genre_list, movie_or_series, start_year, end_year, subtitle, audio,
        country_list, start_rating, end_rating):
    """Create a new entry in Query History with query results

    # TODO: update docstring with doctest
    """

    query_results = QueryHistory(user_id = current_user.id,
        query_run_date_time = datetime.datetime.now(),
        query_string = querystring,
        query_result = query_results,
        param_viewing_location = country_list,
        param_subtitle = subtitle,
        param_audio = audio,
        param_start_year = start_year,
        param_end_year = end_year,
        param_start_rating = start_rating,
        param_end_rating = end_rating,
        movie_or_series = movie_or_series,
        param_genre = genre_list)                   

    db.session.add(query_results)
    db.session.commit()

    return query_results


# def get_previous_query_from_history():                                          # TODO:  what params?
#     """Retreive only users's most recent search from the QueryHistory table"""
#   # TODO:  update docstring with doctests    

#     pass                                                                        # TODO:  complete function stub 


def get_all_query_history(user):                                                    # TODO:  what params?
    """Retreive all of a users's searches from the QueryHistory table"""        # TODO:  update docstring with doctests    

    return queryhistory.query.all(QueryHistory.user_id == user.id) # TODO:  complete function stub 


#*############################################################################*#
#*#                                DB OPERATIONS                             #*#
#*############################################################################*#

def get_all_locations():
    """ Return a dictionary of each of Netflix's service locations.

    >>> get_all_locations()[0]
    <Location id=21 location=Argenina>
    """

    url = "https://unogsng.p.rapidapi.com/countries"

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    response = requests.request("GET", url, headers=headers)

    country_results = json.loads(response.text)
    countries = country_results.values()

    return countries


def create_location(id, name, abbr, subtitle="", audio=""):
    """Create and return a new Country/Location.

    >>> create_location('78', 'United States', 'US')
    <Location id=78 location=United States>
    #"""

    location = Location(id=id, 
                name=name, 
                abbr=abbr, 
                default_subtitle = subtitle, 
                default_audio = audio)

    db.session.add(location)
    db.session.commit() 

    return location


def get_all_genres():
    """ Return a dictionary of each of Netflix's IDs and Genre names.

    >>> get_all_genres()
    <Genre genre_name_as_pk=All Action list_of_ids={10673,10702,11804,11828,1192487,1365,1568,2125,2653,43040,43048,4344,46576,75418,76501,77232,788212,801362,852490,899,9584}>, <Genre genre_name_as_pk=All Anime list_of_ids={10695,11146,2653,2729,3063,413820,452,6721,7424,9302}>, <Genre genre_name_as_pk=All Childrens list_of_ids={10056,27480,27950,28034,28083,28233,48586,5455,561,6218,6796,6962,78120,783,89513}>, <Genre genre_name_as_pk=All Classics list_of_ids={10032,11093,13158,29809,2994,31273,31574,31694,32392,46553,46560,46576,46588,47147,47465,48303,48586,48744,76186}>, <Genre genre_name_as_pk=All Comedies list_of_ids={1009,10256,10375,105,10778,11559,11755,1208951,1333288,1402,1747,17648,2030,2700,31694,3300,34157,3519,3996,4058,4195,43040,4426,4906,52104,52140,52847,5286,5475,5610,56174,58905,59169,61132,61330,6197,63092,63115,6548,711366,7120,72407,7539,77599,77907,78163,78655,79871,7992,852492,869,89585,9302,9434,9702,9736}>, <Genre genre_name_as_pk=All Cult list_of_ids={10944,3675,4734,74652,7627,9434}>, <Genre genre_name_as_pk=All Documentaries list_of_ids={10005,10105,10599,1159,15456,180,2595,26126,2760,28269,3652,3675,4006,4720,48768,49110,49547,50232,5161,5349,55087,56178,58710,60026,6839,7018,72384,77245,852494,90361,9875}>, <Genre genre_name_as_pk=All Dramas list_of_ids={11,11075,11714,1208954,1255,12994,13158,2150,25955,26009,2696,2748,2757,2893,29809,3179,31901,34204,3653,3682,384,3916,3947,4282,4425,452,4961,500,5012,52148,52904,56169,5763,58677,58755,58796,59064,6206,62235,6616,6763,68699,6889,711367,71591,72354,7243,7539,75459,76507,78628,852493,89804,9299,9847,9873}>, <Genre genre_name_as_pk=All Faith and Spirituality list_of_ids={26835,52804,751423}>, <Genre genre_name_as_pk=All Gay and Lesbian list_of_ids={3329,4720,500,5977,65263,7120}>, <Genre genre_name_as_pk=All Horror list_of_ids={10695,10944,1694,42023,45028,48303,61546,75405,75804,75930,8195,83059,8711,89585}>, <Genre genre_name_as_pk=All Independent list_of_ids={11804,3269,384,4195,56184,69192,7077,875,9916}>, <Genre genre_name_as_pk=All International list_of_ids={1192487,1195213,1208951,1208954,1218090,78367,852488,852490,852491,852492,852493,852494}>, <Genre genre_name_as_pk=All Music list_of_ids={10032,10741,1701,2222,2856,5096,52843,6031}>, <Genre genre_name_as_pk=All Musicals list_of_ids={13335,13573,32392,52852,55774,59433,84488,88635}>, <Genre genre_name_as_pk=All Romance list_of_ids={29281,36103,502675}>, <Genre genre_name_as_pk=All Sci-Fi list_of_ids={108533,11014,1372,1492,1568,1694,2595,2729,3327,3916,47147,4734,49110,50232,52780,52849,5903,6000,6926,852491}>, <Genre genre_name_as_pk=All Sports list_of_ids={180,25788,4370,5286,7243,9327}>, <Genre genre_name_as_pk=All Thrillers list_of_ids={10306,10499,10504,10719,11014,11140,1138506,1321,1774,3269,43048,46588,5505,58798,65558,6867,75390,78507,799,852488,8933,89811,9147,972}>, <Genre genre_name_as_pk=20th Century Period Pieces list_of_ids={12739}>, <Genre genre_name_as_pk=Academy Award-Winning Films list_of_ids={51063}>, <Genre genre_name_as_pk=Action list_of_ids={801362}>, <Genre genre_name_as_pk=Action & Adventure list_of_ids={1365}>, <Genre genre_name_as_pk=Action Comedies list_of_ids={43040}>, <Genre genre_name_as_pk=Action Sci-Fi & Fantasy list_of_ids={1568}>, <Genre genre_name_as_pk=Action Thrillers list_of_ids={43048}>, <Genre genre_name_as_pk=Adult Animation list_of_ids={11881}>, <Genre genre_name_as_pk=Adventures list_of_ids={7442}>, <Genre genre_name_as_pk=African Movies list_of_ids={3761}>, <Genre genre_name_as_pk=African Music list_of_ids={6031}>, <Genre genre_name_as_pk=African-American Comedies list_of_ids={4906}>, <Genre genre_name_as_pk=African-American Dramas list_of_ids={9847}>, <Genre genre_name_as_pk=African-American Stand-up Comedy list_of_ids={10778}>, <Genre genre_name_as_pk=Afro-Cuban & Latin Jazz list_of_ids={5661}>, <Genre genre_name_as_pk=Alien Sci-Fi list_of_ids={3327}>, <Genre genre_name_as_pk=American Folk & Bluegrass list_of_ids={760}>, <Genre genre_name_as_pk=Animal Tales list_of_ids={5507}>, <Genre genre_name_as_pk=Animals & Nature Reality TV list_of_ids={50462}>, <Genre genre_name_as_pk=Anime list_of_ids={7424}>, <Genre genre_name_as_pk=Anime Action list_of_ids={2653}>, <Genre genre_name_as_pk=Anime Comedies list_of_ids={9302}>, <Genre genre_name_as_pk=Anime Dramas list_of_ids={452}>, <Genre genre_name_as_pk=Anime Fantasy list_of_ids={11146}>, <Genre genre_name_as_pk=Anime Features list_of_ids={3063}>, <Genre genre_name_as_pk=Anime Horror list_of_ids={10695}>, <Genre genre_name_as_pk=Anime Sci-Fi list_of_ids={2729}>, <Genre genre_name_as_pk=Anime Sci-Fi & Fantasy list_of_ids={1433679}>, <Genre genre_name_as_pk=Anime Series list_of_ids={6721}>, <Genre genre_name_as_pk=Argentinian Dramas list_of_ids={5923}>, <Genre genre_name_as_pk=Argentinian Films list_of_ids={6133}>, <Genre genre_name_as_pk=Argentinian TV Shows list_of_ids={69616}>, <Genre genre_name_as_pk=Art House Movies list_of_ids={29764}>, <Genre genre_name_as_pk=Asian Action Movies list_of_ids={77232}>, <Genre genre_name_as_pk=Asian Movies list_of_ids={78104}>, <Genre genre_name_as_pk=Australian Comedies list_of_ids={2030}>, <Genre genre_name_as_pk=Australian Crime Films list_of_ids={3936}>, <Genre genre_name_as_pk=Australian Dramas list_of_ids={11075}>, <Genre genre_name_as_pk=Australian Movies list_of_ids={5230}>, <Genre genre_name_as_pk=Australian Thrillers list_of_ids={10719}>, <Genre genre_name_as_pk=Australian TV Programmes list_of_ids={52387}>, <Genre genre_name_as_pk=Award-winning Dramas list_of_ids={89804}>, <Genre genre_name_as_pk=Award-winning Movies list_of_ids={89844}>, <Genre genre_name_as_pk=B-Horror Movies list_of_ids={8195}>, <Genre genre_name_as_pk=BAFTA Award-Winning Films list_of_ids={69946}>, <Genre genre_name_as_pk=Baseball Movies list_of_ids={12339}>, <Genre genre_name_as_pk=Basketball Movies list_of_ids={12762}>, <Genre genre_name_as_pk=Belgian Movies list_of_ids={262}>, <Genre genre_name_as_pk=Berlin Film Festival Award-winning Movies list_of_ids={846815}>, <Genre genre_name_as_pk=Biographical Documentaries list_of_ids={3652}>, <Genre genre_name_as_pk=Biographical Dramas list_of_ids={3179}>, <Genre genre_name_as_pk=Blockbuster Movies list_of_ids={90139}>, <Genre genre_name_as_pk=Blue-collar Stand-up Comedy list_of_ids={77907}>, <Genre genre_name_as_pk=Bollywood Films list_of_ids={5480}>, <Genre genre_name_as_pk=Boxing Movies list_of_ids={12443}>, <Genre genre_name_as_pk=Brazilian Comedies list_of_ids={17648}>, <Genre genre_name_as_pk=Brazilian Documentaries list_of_ids={28269}>, <Genre genre_name_as_pk=Brazilian Dramas list_of_ids={4425}>, <Genre genre_name_as_pk=Brazilian Films list_of_ids={798}>, <Genre genre_name_as_pk=Brazilian Music & Musicals list_of_ids={84488}>, <Genre genre_name_as_pk=Brazilian Music and Concert Movies list_of_ids={84489}>, <Genre genre_name_as_pk=Brazilian TV Shows list_of_ids={69624}>, <Genre genre_name_as_pk=British Comedies list_of_ids={1009}>, <Genre genre_name_as_pk=British Crime Films list_of_ids={6051}>, <Genre genre_name_as_pk=British Dramas list_of_ids={3682}>, <Genre genre_name_as_pk=British Miniseries list_of_ids={52508}>, <Genre genre_name_as_pk=British Movies list_of_ids={10757}>, <Genre genre_name_as_pk=British Period Pieces list_of_ids={12433}>, <Genre genre_name_as_pk=British Thrillers list_of_ids={1774}>, <Genre genre_name_as_pk=British TV Comedies list_of_ids={52140}>, <Genre genre_name_as_pk=British TV Dramas list_of_ids={52148}>, <Genre genre_name_as_pk=British TV Mysteries list_of_ids={52120}>, <Genre genre_name_as_pk=British TV Shows list_of_ids={52117}>, <Genre genre_name_as_pk=British TV Sketch Comedies list_of_ids={52104}>, <Genre genre_name_as_pk=Campy Movies list_of_ids={1252}>, <Genre genre_name_as_pk=Canadian Comedies list_of_ids={56174}>, <Genre genre_name_as_pk=Canadian Documentaries list_of_ids={56178}>, <Genre genre_name_as_pk=Canadian Dramas list_of_ids={56169}>, <Genre genre_name_as_pk=Canadian Films list_of_ids={56181}>, <Genre genre_name_as_pk=Canadian French-Language Movies list_of_ids={63151}>, <Genre genre_name_as_pk=Canadian Independent Films list_of_ids={56184}>, <Genre genre_name_as_pk=Canadian TV Programmes list_of_ids={58704}>, <Genre genre_name_as_pk=Cannes Film Festival Award-winning Movies list_of_ids={846810}>, <Genre genre_name_as_pk=Cannes Film Festival Winners list_of_ids={702387}>, <Genre genre_name_as_pk=CÃ©sar Award-winning Movies list_of_ids={846807}>, <Genre genre_name_as_pk=Children & Family Movies list_of_ids={783}>, <Genre genre_name_as_pk=Chinese Movies list_of_ids={3960}>, <Genre genre_name_as_pk=Classic Action & Adventure list_of_ids={46576}>, <Genre genre_name_as_pk=Classic British Films list_of_ids={46560}>, <Genre genre_name_as_pk=Classic Children & Family Films list_of_ids={48586}>, <Genre genre_name_as_pk=Classic Comedies list_of_ids={31694}>, <Genre genre_name_as_pk=Classic Country & Western list_of_ids={2994}>, <Genre genre_name_as_pk=Classic Dramas list_of_ids={29809}>, <Genre genre_name_as_pk=Classic Foreign Movies list_of_ids={32473}>, <Genre genre_name_as_pk=Classic Horror Films list_of_ids={48303}>, <Genre genre_name_as_pk=Classic Movies list_of_ids={31574}>, <Genre genre_name_as_pk=Classic Musicals list_of_ids={32392}>, <Genre genre_name_as_pk=Classic R&B/Soul list_of_ids={11093}>, <Genre genre_name_as_pk=Classic Romantic Movies list_of_ids={31273}>, <Genre genre_name_as_pk=Classic Sci-Fi & Fantasy list_of_ids={47147}>, <Genre genre_name_as_pk=Classic Thrillers list_of_ids={46588}>, <Genre genre_name_as_pk=Classic TV Shows list_of_ids={46553}>, <Genre genre_name_as_pk=Classic War Movies list_of_ids={48744}>, <Genre genre_name_as_pk=Classic Westerns list_of_ids={47465}>, <Genre genre_name_as_pk=Classical Music list_of_ids={10032}>, <Genre genre_name_as_pk=Colombian Movies list_of_ids={69636}>, <Genre genre_name_as_pk=Comedies list_of_ids={6548}>, <Genre genre_name_as_pk=Comedy Jams list_of_ids={78163}>, <Genre genre_name_as_pk=Comic Book & Superhero TV list_of_ids={53717}>, <Genre genre_name_as_pk=Comic Book and Superhero Movies list_of_ids={10118}>, <Genre genre_name_as_pk=Competition Reality TV list_of_ids={49266}>, <Genre genre_name_as_pk=Contemporary R&B list_of_ids={7129}>, <Genre genre_name_as_pk=Country & Western/Folk list_of_ids={1105}>, <Genre genre_name_as_pk=Courtroom Dramas list_of_ids={528582748}>, <Genre genre_name_as_pk=Courtroom TV Dramas list_of_ids={25955}>, <Genre genre_name_as_pk=Creature Features list_of_ids={6895}>, <Genre genre_name_as_pk=Crime Action list_of_ids={788212}>, <Genre genre_name_as_pk=Crime Action & Adventure list_of_ids={9584}>, <Genre genre_name_as_pk=Crime Comedies list_of_ids={4058}>, <Genre genre_name_as_pk=Crime Documentaries list_of_ids={9875}>, <Genre genre_name_as_pk=Crime Dramas list_of_ids={6889}>, <Genre genre_name_as_pk=Crime Films list_of_ids={5824}>, <Genre genre_name_as_pk=Crime Films based on real life list_of_ids={10185}>, <Genre genre_name_as_pk=Crime Thrillers list_of_ids={10499}>, <Genre genre_name_as_pk=Crime TV Documentaries list_of_ids={26126}>, <Genre genre_name_as_pk=Crime TV Dramas list_of_ids={26009}>, <Genre genre_name_as_pk=Crime TV Shows list_of_ids={26146}>, <Genre genre_name_as_pk=Crime TV Soaps list_of_ids={37938}>, <Genre genre_name_as_pk=Critically-acclaimed Action & Adventure list_of_ids={899}>, <Genre genre_name_as_pk=Critically-acclaimed Comedies list_of_ids={9736}>, <Genre genre_name_as_pk=Critically-acclaimed Dramas list_of_ids={6206}>, <Genre genre_name_as_pk=Critically-acclaimed Films list_of_ids={3979}>, <Genre genre_name_as_pk=Critically-acclaimed Independent Films list_of_ids={875}>, <Genre genre_name_as_pk=Critically-acclaimed Sci-Fi & Fantasy list_of_ids={5903}>, <Genre genre_name_as_pk=Cult Comedies list_of_ids={9434}>, <Genre genre_name_as_pk=Cult Horror Movies list_of_ids={10944}>, <Genre genre_name_as_pk=Cult Movies list_of_ids={7627}>, <Genre genre_name_as_pk=Cult Sci-Fi & Fantasy list_of_ids={4734}>, <Genre genre_name_as_pk=Cult TV Shows list_of_ids={74652}>, <Genre genre_name_as_pk=Dance list_of_ids={8451}>, <Genre genre_name_as_pk=Dance & Electronica list_of_ids={5080}>, <Genre genre_name_as_pk=Danish Comedies list_of_ids={59169}>, <Genre genre_name_as_pk=Danish Crime Movies list_of_ids={60339}>, <Genre genre_name_as_pk=Danish Documentaries list_of_ids={60026}>, <Genre genre_name_as_pk=Danish Dramas list_of_ids={59064}>, <Genre genre_name_as_pk=Danish Films list_of_ids={58700}>, <Genre genre_name_as_pk=Danish TV Shows list_of_ids={77951}>, <Genre genre_name_as_pk=Dark Comedies list_of_ids={869}>, <Genre genre_name_as_pk=Deep Sea Horror Movies list_of_ids={45028}>, <Genre genre_name_as_pk=Disco list_of_ids={3493}>, <Genre genre_name_as_pk=Disney list_of_ids={67673}>, <Genre genre_name_as_pk=Disney Musicals list_of_ids={59433}>, <Genre genre_name_as_pk=Documentaries list_of_ids={6839}>, <Genre genre_name_as_pk=Dramas list_of_ids={5763}>, <Genre genre_name_as_pk=Dramas based on Books list_of_ids={4961}>, <Genre genre_name_as_pk=Dramas based on classic literature list_of_ids={13158}>, <Genre genre_name_as_pk=Dramas based on contemporary literature list_of_ids={12994}>, <Genre genre_name_as_pk=Dramas based on real life list_of_ids={3653}>, <Genre genre_name_as_pk=Dutch Children & Family Movies list_of_ids={89513}>, <Genre genre_name_as_pk=Dutch Comedies list_of_ids={79871}>, <Genre genre_name_as_pk=Dutch Dramas list_of_ids={9873}>, <Genre genre_name_as_pk=Dutch Kids TV list_of_ids={89441}>, <Genre genre_name_as_pk=Dutch Movies list_of_ids={10606}>, <Genre genre_name_as_pk=Dutch TV Shows list_of_ids={89442}>, <Genre genre_name_as_pk=Eastern European Movies list_of_ids={5254}>, <Genre genre_name_as_pk=Education for Kids list_of_ids={10659}>, <Genre genre_name_as_pk=Epics list_of_ids={52858}>, <Genre genre_name_as_pk=European Movies list_of_ids={89708}>, <Genre genre_name_as_pk=Experimental Movies list_of_ids={11079}>, <Genre genre_name_as_pk=Faith & Spirituality list_of_ids={26835}>, <Genre genre_name_as_pk=Faith & Spirituality Movies list_of_ids={52804}>, <Genre genre_name_as_pk=Family Adventures list_of_ids={52855}>, <Genre genre_name_as_pk=Family Animation list_of_ids={58879}>, <Genre genre_name_as_pk=Family Comedies list_of_ids={52847}>, <Genre genre_name_as_pk=Family Dramas list_of_ids={31901}>, <Genre genre_name_as_pk=Family Feature Animation list_of_ids={51058}>, <Genre genre_name_as_pk=Family Features list_of_ids={51056}>, <Genre genre_name_as_pk=Family Sci-Fi & Fantasy list_of_ids={52849}>, <Genre genre_name_as_pk=Fantasy Movies list_of_ids={9744}>, <Genre genre_name_as_pk=Female Stand-up Comedy list_of_ids={77599}>, <Genre genre_name_as_pk=Film Noir list_of_ids={7687}>, <Genre genre_name_as_pk=Finnish Movies list_of_ids={62285}>, <Genre genre_name_as_pk=Finnish TV Shows list_of_ids={78503}>, <Genre genre_name_as_pk=Food & Travel TV list_of_ids={72436}>, <Genre genre_name_as_pk=Food & Wine list_of_ids={3890}>, <Genre genre_name_as_pk=Football Movies list_of_ids={12803}>, <Genre genre_name_as_pk=Foreign Action & Adventure list_of_ids={11828}>, <Genre genre_name_as_pk=Foreign Comedies list_of_ids={4426}>, <Genre genre_name_as_pk=Foreign Documentaries list_of_ids={5161}>, <Genre genre_name_as_pk=Foreign Dramas list_of_ids={2150}>, <Genre genre_name_as_pk=Foreign Gay & Lesbian Movies list_of_ids={8243}>, <Genre genre_name_as_pk=Foreign Horror Movies list_of_ids={8654}>, <Genre genre_name_as_pk=Foreign Movies list_of_ids={7462}>, <Genre genre_name_as_pk=Foreign Sci-Fi & Fantasy list_of_ids={6485}>, <Genre genre_name_as_pk=Foreign Thrillers list_of_ids={10306}>, <Genre genre_name_as_pk=French Comedies list_of_ids={58905}>, <Genre genre_name_as_pk=French Documentaries list_of_ids={58710}>, <Genre genre_name_as_pk=French Dramas list_of_ids={58677}>, <Genre genre_name_as_pk=French Movies list_of_ids={58807}>, <Genre genre_name_as_pk=French Thrillers list_of_ids={58798}>, <Genre genre_name_as_pk=Gangster Movies list_of_ids={31851}>, <Genre genre_name_as_pk=Gay & Lesbian Comedies list_of_ids={7120}>, <Genre genre_name_as_pk=Gay & Lesbian Documentaries list_of_ids={4720}>, <Genre genre_name_as_pk=Gay & Lesbian Dramas list_of_ids={500}>, <Genre genre_name_as_pk=Gay & Lesbian Movies list_of_ids={5977}>, <Genre genre_name_as_pk=Gay & Lesbian TV Shows list_of_ids={65263}>, <Genre genre_name_as_pk=German Comedies list_of_ids={63115}>, <Genre genre_name_as_pk=German Dramas list_of_ids={58755}>, <Genre genre_name_as_pk=German Movies list_of_ids={58886}>, <Genre genre_name_as_pk=German TV Shows list_of_ids={65198}>, <Genre genre_name_as_pk=Golden Globe Award-winning Films list_of_ids={82489}>, <Genre genre_name_as_pk=Gory Halloween Favorites list_of_ids={867737}>, <Genre genre_name_as_pk=Gospel Music list_of_ids={5096}>, <Genre genre_name_as_pk=Greek Movies list_of_ids={61115}>, <Genre genre_name_as_pk=Halloween Favorites list_of_ids={108663}>, <Genre genre_name_as_pk=Halloween Favourites list_of_ids={108663}>, <Genre genre_name_as_pk=Hard Rock & Heavy Metal list_of_ids={9793}>, <Genre genre_name_as_pk=Heist Films list_of_ids={27018}>, <Genre genre_name_as_pk=Historical Documentaries list_of_ids={5349}>, <Genre genre_name_as_pk=Historical Dramas list_of_ids={71591}>, <Genre genre_name_as_pk=Holiday Favorites list_of_ids={107985}>, <Genre genre_name_as_pk=Holiday Fun list_of_ids={393181}>, <Genre genre_name_as_pk=Horror Comedy list_of_ids={89585}>, <Genre genre_name_as_pk=Horror Movies list_of_ids={8711}>, <Genre genre_name_as_pk=Independent Action & Adventure list_of_ids={11804}>, <Genre genre_name_as_pk=Independent Comedies list_of_ids={4195}>, <Genre genre_name_as_pk=Independent Dramas list_of_ids={384}>, <Genre genre_name_as_pk=Independent Movies list_of_ids={7077}>, <Genre genre_name_as_pk=Independent Thrillers list_of_ids={3269}>, <Genre genre_name_as_pk=Indian Comedies list_of_ids={9942}>, <Genre genre_name_as_pk=Indian Dramas list_of_ids={5051}>, <Genre genre_name_as_pk=Indian Movies list_of_ids={10463}>, <Genre genre_name_as_pk=Inspirational Music list_of_ids={2222}>, <Genre genre_name_as_pk=International Action & Adventure list_of_ids={852490}>, <Genre genre_name_as_pk=International Comedies list_of_ids={852492}>, <Genre genre_name_as_pk=International Documentaries list_of_ids={852494}>, <Genre genre_name_as_pk=International Dramas list_of_ids={852493}>, <Genre genre_name_as_pk=International Kids TV list_of_ids={1218090}>, <Genre genre_name_as_pk=International Movies list_of_ids={78367}>, <Genre genre_name_as_pk=International Sci-Fi & Fantasy list_of_ids={852491}>, <Genre genre_name_as_pk=International Thrillers list_of_ids={852488}>, <Genre genre_name_as_pk=International TV Action & Adventure list_of_ids={1192487}>, <Genre genre_name_as_pk=International TV Comedies list_of_ids={1208951}>, <Genre genre_name_as_pk=International TV Dramas list_of_ids={1208954}>, <Genre genre_name_as_pk=International TV Shows list_of_ids={1195213}>, <Genre genre_name_as_pk=Investigative Reality TV list_of_ids={48785}>, <Genre genre_name_as_pk=Irish Movies list_of_ids={58750}>, <Genre genre_name_as_pk=Italian Comedies list_of_ids={3300}>, <Genre genre_name_as_pk=Italian Dramas list_of_ids={4282}>, <Genre genre_name_as_pk=Italian Movies list_of_ids={8221}>, <Genre genre_name_as_pk=Italian Thrillers list_of_ids={6867}>, <Genre genre_name_as_pk=Japanese Academy Award-winning Movies list_of_ids={1293326}>, <Genre genre_name_as_pk=Japanese Action & Adventure list_of_ids={4344}>, <Genre genre_name_as_pk=Japanese Comedies list_of_ids={1747}>, <Genre genre_name_as_pk=Japanese Dramas list_of_ids={2893}>, <Genre genre_name_as_pk=Japanese Horror Movies list_of_ids={10750}>, <Genre genre_name_as_pk=Japanese Kids TV list_of_ids={65925}>, <Genre genre_name_as_pk=Japanese Movies list_of_ids={10398}>, <Genre genre_name_as_pk=Japanese Period Dramas list_of_ids={1402191}>, <Genre genre_name_as_pk=Japanese Sci-Fi & Fantasy list_of_ids={6000}>, <Genre genre_name_as_pk=Japanese Thrillers list_of_ids={799}>, <Genre genre_name_as_pk=Japanese TV Comedies list_of_ids={711366}>, <Genre genre_name_as_pk=Japanese TV Dramas list_of_ids={711367}>, <Genre genre_name_as_pk=Japanese TV Films list_of_ids={64256}>, <Genre genre_name_as_pk=Japanese TV Sci-Fi & Fantasy list_of_ids={1461923}>, <Genre genre_name_as_pk=Japanese TV Shows list_of_ids={64256}>, <Genre genre_name_as_pk=Japanese TV Thrillers list_of_ids={1138506}>, <Genre genre_name_as_pk=Jazz & Easy Listening list_of_ids={10271}>, <Genre genre_name_as_pk=Kids Anime list_of_ids={413820}>, <Genre genre_name_as_pk=Kids Faith & Spirituality list_of_ids={751423}>, <Genre genre_name_as_pk=Kids Music list_of_ids={52843}>, <Genre genre_name_as_pk=Kids TV for ages 0 to 2 list_of_ids={28233}>, <Genre genre_name_as_pk=Kids TV for ages 11 to 12 list_of_ids={27950}>, <Genre genre_name_as_pk=Kids TV for ages 2 to 4 list_of_ids={27480}>, <Genre genre_name_as_pk=Kids TV for ages 5 to 7 list_of_ids={28034}>, <Genre genre_name_as_pk=Kids TV for ages 8 to 10 list_of_ids={28083}>, <Genre genre_name_as_pk=Kids&#39; TV list_of_ids={27346}>, <Genre genre_name_as_pk=Korean Action & Adventure list_of_ids={8248}>, <Genre genre_name_as_pk=Korean Comedies list_of_ids={6626}>, <Genre genre_name_as_pk=Korean Dramas list_of_ids={1989}>, <Genre genre_name_as_pk=Korean Movies list_of_ids={5685}>, <Genre genre_name_as_pk=Korean Thrillers list_of_ids={11283}>, <Genre genre_name_as_pk=Korean TV Dramas list_of_ids={68699}>, <Genre genre_name_as_pk=Korean TV Shows list_of_ids={67879}>, <Genre genre_name_as_pk=Late Night Comedies list_of_ids={1402}>, <Genre genre_name_as_pk=Latin American Comedies list_of_ids={3996}>, <Genre genre_name_as_pk=Latin American Documentaries list_of_ids={15456}>, <Genre genre_name_as_pk=Latin American Dramas list_of_ids={6763}>, <Genre genre_name_as_pk=Latin American Movies list_of_ids={1613}>, <Genre genre_name_as_pk=Latin American Music & Musicals list_of_ids={88635}>, <Genre genre_name_as_pk=Latin American Police TV Shows list_of_ids={75408}>, <Genre genre_name_as_pk=Latin American TV Shows list_of_ids={67708}>, <Genre genre_name_as_pk=Latin Music list_of_ids={10741}>, <Genre genre_name_as_pk=Latino Stand-up Comedy list_of_ids={34157}>, <Genre genre_name_as_pk=Laugh-Out-Loud Comedies list_of_ids={1333288}>, <Genre genre_name_as_pk=Martial Arts Movies list_of_ids={8985}>, <Genre genre_name_as_pk=Martial Arts, Boxing & Wrestling list_of_ids={6695}>, <Genre genre_name_as_pk=Medical TV Dramas list_of_ids={34204}>, <Genre genre_name_as_pk=Mexican Comedies list_of_ids={105}>, <Genre genre_name_as_pk=Mexican Dramas list_of_ids={2757}>, <Genre genre_name_as_pk=Mexican Films list_of_ids={7825}>, <Genre genre_name_as_pk=Mexican TV Shows list_of_ids={67644}>, <Genre genre_name_as_pk=Middle Eastern Movies list_of_ids={5875}>, <Genre genre_name_as_pk=Military & War Action & Adventure list_of_ids={76501}>, <Genre genre_name_as_pk=Military & War Documentaries list_of_ids={77245}>, <Genre genre_name_as_pk=Military & War Dramas list_of_ids={76507}>, <Genre genre_name_as_pk=Military & War Movies list_of_ids={76510}>, <Genre genre_name_as_pk=Military Action & Adventure list_of_ids={2125}>, <Genre genre_name_as_pk=Military Documentaries list_of_ids={4006}>, <Genre genre_name_as_pk=Military Dramas list_of_ids={11}>, <Genre genre_name_as_pk=Military TV Shows list_of_ids={25804}>, <Genre genre_name_as_pk=Miniseries list_of_ids={4814}>, <Genre genre_name_as_pk=Mockumentaries list_of_ids={26}>, <Genre genre_name_as_pk=Modern & Alternative Rock list_of_ids={9090}>, <Genre genre_name_as_pk=Modern Classic Movies list_of_ids={76186}>, <Genre genre_name_as_pk=Monster Movies list_of_ids={947}>, <Genre genre_name_as_pk=Movies based on children&#39;s books list_of_ids={10056}>, <Genre genre_name_as_pk=Movies for ages 0 to 2 list_of_ids={6796}>, <Genre genre_name_as_pk=Movies for ages 11 to 12 list_of_ids={6962}>, <Genre genre_name_as_pk=Movies for ages 2 to 4 list_of_ids={6218}>, <Genre genre_name_as_pk=Movies for ages 5 to 7 list_of_ids={5455}>, <Genre genre_name_as_pk=Movies for ages 8 to 10 list_of_ids={561}>, <Genre genre_name_as_pk=Music list_of_ids={1701}>, <Genre genre_name_as_pk=Music & Concert Documentaries list_of_ids={90361}>, <Genre genre_name_as_pk=Music & Musicals list_of_ids={52852}>, <Genre genre_name_as_pk=Music and Concert Films list_of_ids={84483}>, <Genre genre_name_as_pk=Musicals list_of_ids={13335}>, <Genre genre_name_as_pk=Mysteries list_of_ids={9994}>, <Genre genre_name_as_pk=Nature & Ecology Documentaries list_of_ids={48768}>, <Genre genre_name_as_pk=Nature & Ecology TV Documentaries list_of_ids={49547}>, <Genre genre_name_as_pk=New Country list_of_ids={10365}>, <Genre genre_name_as_pk=New Zealand Movies list_of_ids={63782}>, <Genre genre_name_as_pk=Nollywood Movies list_of_ids={1138254}>, <Genre genre_name_as_pk=Nordic Children & Family Movies list_of_ids={78120}>, <Genre genre_name_as_pk=Nordic Comedies list_of_ids={78655}>, <Genre genre_name_as_pk=Nordic Crime Movies list_of_ids={78208}>, <Genre genre_name_as_pk=Nordic Dramas list_of_ids={78628}>, <Genre genre_name_as_pk=Nordic Thrillers list_of_ids={78321}>, <Genre genre_name_as_pk=Nordic TV Shows list_of_ids={78634}>, <Genre genre_name_as_pk=Norwegian Comedies list_of_ids={61132}>, <Genre genre_name_as_pk=Norwegian Crime Movies list_of_ids={78463}>, <Genre genre_name_as_pk=Norwegian Dramas list_of_ids={62235}>, <Genre genre_name_as_pk=Norwegian Films list_of_ids={62510}>, <Genre genre_name_as_pk=Norwegian Thrillers list_of_ids={78507}>, <Genre genre_name_as_pk=Norwegian TV list_of_ids={78373}>, <Genre genre_name_as_pk=Period Pieces list_of_ids={12123}>, <Genre genre_name_as_pk=Police Action & Adventure list_of_ids={75418}>, <Genre genre_name_as_pk=Police Detective Movies list_of_ids={79049}>, <Genre genre_name_as_pk=Police Dramas list_of_ids={75459}>, <Genre genre_name_as_pk=Police Movies list_of_ids={75436}>, <Genre genre_name_as_pk=Police Mysteries list_of_ids={75415}>, <Genre genre_name_as_pk=Police Thrillers list_of_ids={75390}>, <Genre genre_name_as_pk=Police TV Shows list_of_ids={75392}>, <Genre genre_name_as_pk=Political Comedies list_of_ids={2700}>, <Genre genre_name_as_pk=Political Documentaries list_of_ids={7018}>, <Genre genre_name_as_pk=Political Dramas list_of_ids={6616}>, <Genre genre_name_as_pk=Political Thrillers list_of_ids={10504}>, <Genre genre_name_as_pk=Political TV Documentaries list_of_ids={55087}>, <Genre genre_name_as_pk=Pop list_of_ids={2145}>, <Genre genre_name_as_pk=Psychological Thrillers list_of_ids={5505}>, <Genre genre_name_as_pk=Punk Rock list_of_ids={8721}>, <Genre genre_name_as_pk=Quirky Romance list_of_ids={36103}>, <Genre genre_name_as_pk=Rap & Hip-Hop list_of_ids={6073}>, <Genre genre_name_as_pk=Reality TV list_of_ids={9833}>, <Genre genre_name_as_pk=Reggae list_of_ids={3081}>, <Genre genre_name_as_pk=Religious Documentaries list_of_ids={10005}>, <Genre genre_name_as_pk=Retro Anime list_of_ids={1408777}>, <Genre genre_name_as_pk=Rock & Pop Concerts list_of_ids={3278}>, <Genre genre_name_as_pk=Rockumentaries list_of_ids={4649}>, <Genre genre_name_as_pk=Romantic Comedies list_of_ids={5475}>, <Genre genre_name_as_pk=Romantic Danish Movies list_of_ids={61656}>, <Genre genre_name_as_pk=Romantic Dramas list_of_ids={1255}>, <Genre genre_name_as_pk=Romantic Favorites list_of_ids={502675}>, <Genre genre_name_as_pk=Romantic Films based on a book list_of_ids={3830}>, <Genre genre_name_as_pk=Romantic Foreign Movies list_of_ids={7153}>, <Genre genre_name_as_pk=Romantic Gay & Lesbian Movies list_of_ids={3329}>, <Genre genre_name_as_pk=Romantic Independent Movies list_of_ids={9916}>, <Genre genre_name_as_pk=Romantic Japanese Films list_of_ids={17241}>, <Genre genre_name_as_pk=Romantic Japanese Movies list_of_ids={17241}>, <Genre genre_name_as_pk=Romantic Japanese TV Shows list_of_ids={1458609}>, <Genre genre_name_as_pk=Romantic Movies list_of_ids={8883}>, <Genre genre_name_as_pk=Romantic Movies based on Books list_of_ids={3830}>, <Genre genre_name_as_pk=Romantic Nordic Movies list_of_ids={78250}>, <Genre genre_name_as_pk=Romantic Swedish Movies list_of_ids={60829}>, <Genre genre_name_as_pk=Romantic TV Programmes list_of_ids={26156}>, <Genre genre_name_as_pk=Romantic TV Soaps list_of_ids={26052}>, <Genre genre_name_as_pk=Russian list_of_ids={11567}>, <Genre genre_name_as_pk=Satanic Stories list_of_ids={6998}>, <Genre genre_name_as_pk=Satires list_of_ids={4922}>, <Genre genre_name_as_pk=Scandinavian Comedies list_of_ids={11755}>, <Genre genre_name_as_pk=Scandinavian Crime Films list_of_ids={1884}>, <Genre genre_name_as_pk=Scandinavian Documentaries list_of_ids={10599}>, <Genre genre_name_as_pk=Scandinavian Dramas list_of_ids={2696}>, <Genre genre_name_as_pk=Scandinavian Independent Movies list_of_ids={69192}>, <Genre genre_name_as_pk=Scandinavian Movies list_of_ids={9292}>, <Genre genre_name_as_pk=Scandinavian Thrillers list_of_ids={1321}>, <Genre genre_name_as_pk=Scandinavian TV list_of_ids={76802}>, <Genre genre_name_as_pk=Sci-Fi list_of_ids={108533}>, <Genre genre_name_as_pk=Sci-Fi & Fantasy list_of_ids={1492}>, <Genre genre_name_as_pk=Sci-Fi Adventure list_of_ids={6926}>, <Genre genre_name_as_pk=Sci-Fi Dramas list_of_ids={3916}>, <Genre genre_name_as_pk=Sci-Fi Horror Movies list_of_ids={1694}>, <Genre genre_name_as_pk=Sci-Fi Thrillers list_of_ids={11014}>, <Genre genre_name_as_pk=Science & Nature Documentaries list_of_ids={2595}>, <Genre genre_name_as_pk=Science & Nature TV list_of_ids={52780}>, <Genre genre_name_as_pk=Science & Technology Documentaries list_of_ids={49110}>, <Genre genre_name_as_pk=Science & Technology TV Documentaries list_of_ids={50232}>, <Genre genre_name_as_pk=Screwball Comedies list_of_ids={9702}>, <Genre genre_name_as_pk=Showbiz Dramas list_of_ids={5012}>, <Genre genre_name_as_pk=Showbiz Musicals list_of_ids={13573}>, <Genre genre_name_as_pk=Silent Movies list_of_ids={53310}>, <Genre genre_name_as_pk=Singer-Songwriters list_of_ids={5608}>, <Genre genre_name_as_pk=Sitcoms list_of_ids={3903}>, <Genre genre_name_as_pk=Slapstick Comedies list_of_ids={10256}>, <Genre genre_name_as_pk=Slasher and Serial Killer Movies list_of_ids={8646}>, <Genre genre_name_as_pk=Slice of Life Anime list_of_ids={1519826}>, <Genre genre_name_as_pk=Soccer Movies list_of_ids={12549}>, <Genre genre_name_as_pk=Soccer Non-fiction list_of_ids={3215}>, <Genre genre_name_as_pk=Social & Cultural Documentaries list_of_ids={3675}>, <Genre genre_name_as_pk=Social Issue Dramas list_of_ids={3947}>, <Genre genre_name_as_pk=Southeast Asian Movies list_of_ids={9196}>, <Genre genre_name_as_pk=Spanish Comedies list_of_ids={61330}>, <Genre genre_name_as_pk=Spanish Dramas list_of_ids={58796}>, <Genre genre_name_as_pk=Spanish Horror Films list_of_ids={61546}>, <Genre genre_name_as_pk=Spanish Horror Movies list_of_ids={61546}>, <Genre genre_name_as_pk=Spanish Movies list_of_ids={58741}>, <Genre genre_name_as_pk=Spanish Thrillers list_of_ids={65558}>, <Genre genre_name_as_pk=Spanish-Language TV Shows list_of_ids={67675}>, <Genre genre_name_as_pk=Special Interest list_of_ids={6814}>, <Genre genre_name_as_pk=Spiritual Documentaries list_of_ids={2760}>, <Genre genre_name_as_pk=Sports & Fitness list_of_ids={9327}>, <Genre genre_name_as_pk=Sports Comedies list_of_ids={5286}>, <Genre genre_name_as_pk=Sports Documentaries list_of_ids={180}>, <Genre genre_name_as_pk=Sports Dramas list_of_ids={7243}>, <Genre genre_name_as_pk=Sports Movies list_of_ids={4370}>, <Genre genre_name_as_pk=Sports TV Programmes list_of_ids={25788}>, <Genre genre_name_as_pk=Spy Action & Adventure list_of_ids={10702}>, <Genre genre_name_as_pk=Spy Thrillers list_of_ids={9147}>, <Genre genre_name_as_pk=Stage Musicals list_of_ids={55774}>, <Genre genre_name_as_pk=Stand-up Comedy list_of_ids={11559}>, <Genre genre_name_as_pk=Steamy Romance list_of_ids={29281}>, <Genre genre_name_as_pk=Steamy Romantic Movies list_of_ids={35800}>, <Genre genre_name_as_pk=Steamy Thrillers list_of_ids={972}>, <Genre genre_name_as_pk=Supernatural Horror Movies list_of_ids={42023}>, <Genre genre_name_as_pk=Supernatural Thrillers list_of_ids={11140}>, <Genre genre_name_as_pk=Swedish Comedies list_of_ids={63092}>, <Genre genre_name_as_pk=Swedish Crime Movies list_of_ids={63975}>, <Genre genre_name_as_pk=Swedish Films list_of_ids={62016}>, <Genre genre_name_as_pk=Swedish TV Shows list_of_ids={76793}>, <Genre genre_name_as_pk=Talk Shows & Stand-up Comedy list_of_ids={1516534}>, <Genre genre_name_as_pk=Tearjerkers list_of_ids={6384}>, <Genre genre_name_as_pk=Teen Comedies list_of_ids={3519}>, <Genre genre_name_as_pk=Teen Dramas list_of_ids={9299}>, <Genre genre_name_as_pk=Teen Romance list_of_ids={53915}>, <Genre genre_name_as_pk=Teen Screams list_of_ids={52147}>, <Genre genre_name_as_pk=Teen TV Shows list_of_ids={60951}>, <Genre genre_name_as_pk=Theatre Arts list_of_ids={10832}>, <Genre genre_name_as_pk=Thrillers list_of_ids={8933}>, <Genre genre_name_as_pk=Travel & Adventure Documentaries list_of_ids={1159}>, <Genre genre_name_as_pk=Travel & Adventure Reality TV list_of_ids={48762}>, <Genre genre_name_as_pk=TV Action & Adventure list_of_ids={10673}>, <Genre genre_name_as_pk=TV Animated Comedies list_of_ids={7992}>, <Genre genre_name_as_pk=TV Cartoons list_of_ids={11177}>, <Genre genre_name_as_pk=TV Comedies list_of_ids={10375}>, <Genre genre_name_as_pk=TV Comedy Dramas list_of_ids={7539}>, <Genre genre_name_as_pk=TV Documentariesa list_of_ids={10105}>, <Genre genre_name_as_pk=TV Dramas list_of_ids={11714}>, <Genre genre_name_as_pk=TV Horror list_of_ids={83059}>, <Genre genre_name_as_pk=TV Mysteries list_of_ids={4366}>, <Genre genre_name_as_pk=TV Sci-Fi & Fantasy list_of_ids={1372}>, <Genre genre_name_as_pk=TV Shows list_of_ids={83}>, <Genre genre_name_as_pk=TV Sketch Comedies list_of_ids={5610}>, <Genre genre_name_as_pk=TV Soaps list_of_ids={10634}>, <Genre genre_name_as_pk=TV Soaps Featuring a Strong Female Lead list_of_ids={26105}>, <Genre genre_name_as_pk=TV Teen Dramas list_of_ids={52904}>, <Genre genre_name_as_pk=TV Thrillers list_of_ids={89811}>, <Genre genre_name_as_pk=TV Westerns list_of_ids={11522}>, <Genre genre_name_as_pk=Urban & Dance Concerts list_of_ids={9472}>, <Genre genre_name_as_pk=US Movies list_of_ids={1159493}>, <Genre genre_name_as_pk=US Police TV Shows list_of_ids={75445}>, <Genre genre_name_as_pk=US TV Comedies list_of_ids={72407}>, <Genre genre_name_as_pk=US TV Documentaries list_of_ids={72384}>, <Genre genre_name_as_pk=US TV Dramas list_of_ids={72354}>, <Genre genre_name_as_pk=US TV Programmes list_of_ids={72404}>, <Genre genre_name_as_pk=Vampire Films list_of_ids={75432}>, <Genre genre_name_as_pk=Vampire Horror Movies list_of_ids={75804}>, <Genre genre_name_as_pk=Vocal Jazz list_of_ids={5342}>, <Genre genre_name_as_pk=Vocal Pop list_of_ids={1800}>, <Genre genre_name_as_pk=Wacky Comedies list_of_ids={6197}>, <Genre genre_name_as_pk=Werewolf Horror Movies list_of_ids={75930}>, <Genre genre_name_as_pk=Westerns list_of_ids={7700}>, <Genre genre_name_as_pk=Wine & Beverage Appreciation list_of_ids={1458}>, <Genre genre_name_as_pk=World Music Concerts list_of_ids={2856}>, <Genre genre_name_as_pk=WWII Films list_of_ids={70023}>, <Genre genre_name_as_pk=Zombie Horror Movies list_of_ids={75405}>]
    """

    url = "https://unogs-unogs-v1.p.rapidapi.com/api.cgi"

    querystring = {"t":"genres"}

    headers = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
    }

    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    response = requests.request("GET", url, headers=headers, params=querystring)

    #convert the response down into a usable dictionary of genres:ids
    n_list = []
    n_payload = json.loads(response.text)
    n_list.append(n_payload)
    n_dictionary = n_list[0].values()
    
    new_list = list(n_dictionary)
    n_str_result = new_list[1]

    genre_dictionary = {}

    for item in n_str_result:
        for char in item:
            if char[0] != 'å':  # to cull out garbage, like ååVãã©ãåTVçªçµã»ã©ãå
                genre_dictionary.update(item)
    
    return genre_dictionary


def get_genre_id_by_name(genre_name):
    """Return just the ID of a genre when given a genre name.

    Name is being used as the Primary Key on the genre table.
    ID is a list.
    ID list can contain either:
     - a single string value which represents one single genre  
        eg. 'Social & Cultural Documentaries'
     - multiple strings which represnet a group of related genres
        eg. 'All Documentaries'
    
    >>> get_genre_id_by_name('Social & Cultural Documentaries')
    <Genre genre_name_as_pk=Social & Cultural Documentaries list_of_ids={3675}>

    >>> get_genre_id_by_name('All Documentaries')
    <Genre genre_name_as_pk=All Documentaries list_of_ids={10005,10105,10599,1159,15456,180,2595,26126,2760,28269,3652,3675,4006,4720,48768,49110,49547,50232,5161,5349,55087,56178,58710,60026,6839,7018,72384,77245,852494,90361,9875}>
    """

    genre = Genre.query.filter(Genre.name == genre_name).first()   

    return genre.id


def create_genre(genre_id, genre_name):
    """Create and return a new Genre.

    >>> create_genre('10118', 'Comic book and superhero movies')
    <Genre genre_name_as_pk='Comic book and superhero movies' list_of_ids=['10118']>'
    """

    genre = Genre(id=genre_id,
                name = genre_name)

    db.session.add(genre)
    db.session.commit() 

    return genre


def get_stored_genres():
    """Return all of the available genres."""
                     
    return Genre.query.filter().all()   


def create_keyword(keyword_id, keyword_name):
    """Create and return a Keyword.

    >>> create_keyword('207958', 'queer activism')
    <Keyword id=207958 keyword='queer activism'>

    >>> create_keyword('239141', 'post-racial america')
    <Keyword id=239141 keyword='post-racial america'>
    """

    keyword = TmdbKeyword(id=keyword_id,
                name = keyword_name)

    db.session.add(keyword)
    db.session.commit() 

    return keyword


def get_all_keywords():
    """Return all of the available keywords."""
                     
    return TmdbKeyword.query.filter().all()   


def get_keyword_id_by_name(keyword_name):
    """Return keyword when given keyword name.
    
    >>> get_keyword_id_by_name('suffragist movement')
    <Keyword id=207958 keyword='suffragist movement'>

    >>> get_keyword_id_by_name('anti-racism')
    <Keyword id=257456 keyword='anti-racism'>
    """
    
    keyword = TmdbKeyword.query.filter(TmdbKeyword.name == keyword_name).first() 

    return keyword.id  


def get_keyword_name_by_id(keyword_id):
    """Return keyword when given keyword ID.
    
    >>> get_keyword_name_by_id('210586')
    <Keyword id=210586 keyword='dark fairy tale'>

    >>> get_keyword_name_by_id('253306')
    <Keyword id=253306 keyword='feminist literature'>
    """
                     
    keyword = TmdbKeyword.query.filter(TmdbKeyword.id == keyword_id).first()   

    return keyword.named



#*############################################################################*#
#*#                          TMDB API OPERATIONS                             #*#
#*############################################################################*#

def get_movies_by_title(str):
    """Return movies by string of title.
    
    >>> get_movies_by_title('the last unicorn')
    {1: {'adult': False, 'backdrop_path': '/fwxOQkzYtRVKs3kzcyukdbsyIuh.jpg', 'genre_ids': [14, 16, 10751, 12], 'id': 10150, 'original_language': 'en', 'original_title': 'The Last Unicorn', 'overview': "From a riddle-speaking butterfly, a unicorn learns that she is supposedly the last of her kind, all the others having been herded away by the Red Bull. The unicorn sets out to discover the truth behind the butterfly's words. She is eventually joined on her quest by Schmendrick, a second-rate magician, and Molly Grue, a now middle-aged woman who dreamed all her life of seeing a unicorn. Their journey leads them far from home, all the way to the castle of King Haggard.", 'popularity': 9.275, 'poster_path': '/grBct9dkEaI6jnH1jJHEwt3g7T4.jpg', 'release_date': '1982-11-19', 'title': 'The Last Unicorn', 'video': False, 'vote_average': 7.2, 'vote_count': 299}}
    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by={sort_by}&page=1&include_adult=false&query='{str}'"

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    count = 1
    
    for index, title in enumerate(search_results['results']):
        recommendations[(index + 1)] = title

    return recommendations


def get_people_with_name(str):
    """Return a person(s) from string of name.

    Did you know the kid from Willy Wonka was only in one movie ever?

    >>> get_people_with_name('Peter Ostrum')
    {3462: {'adult': False, 'gender': 2, 'id': 3462, 'known_for': [{'adult': False, 'backdrop_path': '/iiusvOLB4ytkZ6FSFMlGHvt33uW.jpg', 'genre_ids': [10751, 14, 35], 'id': 252, 'media_type': 'movie', 'original_language': 'en', 'original_title': 'Willy Wonka & the Chocolate Factory', 'overview': 'Eccentric candy man Willy Wonka prompts a worldwide frenzy when he announces that golden tickets hidden inside five of his delicious candy bars will admit their lucky holders into his top-secret confectionary. But does Wonka have an agenda hidden amid a world of Oompa Loompas and chocolate rivers?', 'poster_path': '/vmpsZkrs4Uvkp9r1atL8B3frA63.jpg', 'release_date': '1971-06-29', 'title': 'Willy Wonka & the Chocolate Factory', 'video': False, 'vote_average': 7.5, 'vote_count': 2164}, {'adult': False, 'genre_ids': [99, 14], 'id': 413393, 'media_type': 'movie', 'original_language': 'en', 'original_title': "Pure Imagination: The Story of 'Willy Wonka and the Chocolate Factory'", 'overview': 'Retrospective documentary on the making of the cult classic "Willy Wonka and the Chocolate Factory."', 'poster_path': '/gbL6TucQnnVnWl5XKjFI4P2IXwu.jpg', 'release_date': '2001-11-13', 'title': "Pure Imagination: The Story of 'Willy Wonka and the Chocolate Factory'", 'video': False, 'vote_average': 6.6, 'vote_count': 12}, {'first_air_date': '2005-06-13', 'genre_ids': [], 'id': 24956, 'media_type': 'tv', 'name': '100 Greatest Kid Stars', 'origin_country': ['US'], 'original_language': 'en', 'original_name': '100 Greatest Kid Stars', 'overview': '', 'vote_average': 0, 'vote_count': 0}], 'known_for_department': 'Acting', 'name': 'Peter Ostrum', 'popularity': 0.6, 'profile_path': '/a3jbe78Rs8gjJrFxl0PoVtayNbf.jpg'}}

    >>> get_people_with_name('wachowski').keys()
    dict_keys([9340, 9339, 1737865, 1636722])
    """

    url = f"https://api.themoviedb.org/3/search/person?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query='{str}'"

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    count = 1
    
    for index, title in enumerate(search_results['results']):
        recommendations[title.get('id')] = title

    return recommendations


def get_studio_info_from_name(str):
    """Return studio/production company info from string of name.

    >>> get_studio_info_from_name('Studio Ghibli')
    {10342: {'id': 10342, 'logo_path': '/eS79pslnoKbWg7t3PMA9ayl0bGs.png', 'name': 'Studio Ghibli', 'origin_country': 'JP'}}
    """

    url = f"https://api.themoviedb.org/3/search/company?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query='{str}'"

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    count = 1
    
    for index, title in enumerate(search_results['results']):
        recommendations[title.get('id')] = title

    return recommendations


# def get_genre_with_genre_id(genre_id):
#     """Given a genre id, return genre info.
    
#     >>>get_genre_with_genre_id('10751')
    
#     """

#     pass


# def get_genre_with_type_and_name_or_id(str, movie_or_tv):
#     """Return genre info with string of genre name.
    
#     Accepts required parameters:
#         1. str: the name of the genre 
#         2. movie_or_tv: is this a series genre or film genre?
#             does this need to hit the tv endppoint or the movie endpoint?
#             e.g. 'movie',  'tv'

#     >>>get_genre_with_type_and_name_or_id('10751')

#     """

#     url = f"https://api.themoviedb.org/3/genre/{movie_or_tv}/list?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query='{str}'"

#     response = requests.get(url)

#     search_results = json.loads(response.text)

#     print(search_results)
#     print(url) 

#     # recommendations = dict()
#     # count = 1
    
#     # for index, title in enumerate(search_results['results']):
#     #     recommendations[(index + 1)] = title

#     return "" # recommendations

# print()
# print()
# print(get_genre_with_type_and_name_or_id('lgbt', 'movie'))


def get_titles_with_keyword(keyword_id):
    """Return recommendations from keyword.

    >>> get_movies_by_title('lgbt')[1]['adult']
    False
    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by={sort_by}&include_adult=false&include_video=false&page=1&with_keywords={keyword_id}"
    # TODO:  decide how to wrangle the different TV/movie endpoints??
    # https://developers.themoviedb.org/3/discover/tv-discover

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    count = 1
    
    for index, title in enumerate(search_results['results']):
        recommendations[(index + 1)] = title

    return recommendations


def get_person_bio_with_id(person_id):
    """Return person's details from people_id.
    
    >>> get_person_bio_with_id('15309')['birthday']
    '1963-10-14'
    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/person/{person_id}?language=en-US&api_key={TMDB_API_KEY}"
        # TODO:  decide how to wrangle the different TV/movie endpoints??
    # https://developers.themoviedb.org/3/discover/tv-discover

    response = requests.get(url)

    search_results = json.loads(response.text)

    search_results['person_id'] = person_id

    return search_results


def get_titles_with_person(person_id):
    """Return recommendations from people_id.
    
    >>> get_titles_with_person('3462')
    {1: {'adult': False, 'backdrop_path': '/iiusvOLB4ytkZ6FSFMlGHvt33uW.jpg', 'popularity': 26.457, 'genre_ids': [10751, 14, 35], 'title': 'Willy Wonka & the Chocolate Factory', 'original_language': 'en', 'original_title': 'Willy Wonka & the Chocolate Factory', 'poster_path': '/vmpsZkrs4Uvkp9r1atL8B3frA63.jpg', 'overview': 'Eccentric candy man Willy Wonka prompts a worldwide frenzy when he announces that golden tickets hidden inside five of his delicious candy bars will admit their lucky holders into his top-secret confectionary. But does Wonka have an agenda hidden amid a world of Oompa Loompas and chocolate rivers?', 'video': False, 'vote_average': 7.5, 'id': 252, 'vote_count': 2193, 'release_date': '1971-06-29'}, 2: {'adult': False, 'backdrop_path': None, 'popularity': 5.806, 'genre_ids': [99, 14], 'title': "Pure Imagination: The Story of 'Willy Wonka and the Chocolate Factory'", 'original_language': 'en', 'original_title': "Pure Imagination: The Story of 'Willy Wonka and the Chocolate Factory'", 'poster_path': '/gbL6TucQnnVnWl5XKjFI4P2IXwu.jpg', 'overview': 'Retrospective documentary on the making of the cult classic "Willy Wonka and the Chocolate Factory."', 'video': False, 'vote_average': 6.6, 'id': 413393, 'vote_count': 12, 'release_date': '2001-11-13'}}
    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by={sort_by}&include_adult=false&include_video=false&page=1&with_people={person_id}"
    # TODO:  decide how to wrangle the different TV/movie endpoints??
    # https://developers.themoviedb.org/3/discover/tv-discover

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    count = 1

    recommendations['biography'] = get_person_bio_with_id(person_id)
    
    for index, title in enumerate(search_results['results']):
        recommendations[(index + 1)] = title

    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print(recommendations)
    print()
    print()
    print()
    print()
    print()
    print()
    print()

    return recommendations


def get_titles_from_studio(studio_id):
    """Return recommendations from studio_id.
    
    >>> get_titles_from_studio('10342')[1]
    {'vote_average': 8.5, 'popularity': 56.698, 'vote_count': 10469, 'release_date': '2001-07-20', 'adult': False, 'backdrop_path': '/mSDsSDwaP3E7dEfUPWy4J0djt4O.jpg', 'title': 'Spirited Away', 'genre_ids': [16, 10751, 14], 'poster_path': '/eO4NHOsitcVpRw0kolJRLxXdxa2.jpg', 'original_language': 'ja', 'original_title': '千と千尋の神隠し', 'id': 129, 'overview': 'A young girl, Chihiro, becomes trapped in a strange new world of spirits. When her parents undergo a mysterious transformation, she must call upon the courage she never knew she had to free her family.', 'video': False}
    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by={sort_by}&include_adult=false&include_video=false&page=1&with_companies={studio_id}"
    # TODO:  decide how to wrangle the different TV/movie endpoints??
    # https://developers.themoviedb.org/3/discover/tv-discover

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    count = 1
    
    for index, title in enumerate(search_results['results']):
        recommendations[title['id']] = title
    
    return recommendations


def get_titles_with_genre(genre_id):
    """Return recommendations from keyword.
    
    Accepts a single string 
        get_titles_with_genre('16')

    or a list of strings
        get_titles_with_genre('[16, 10751, 14]')

    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by={sort_by}&include_adult=false&include_video=false&page=1&with_genres={genre_id}"
    # TODO:  decide how to wrangle the different TV/movie endpoints??
    # https://developers.themoviedb.org/3/discover/tv-discover

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    
    for index, title in enumerate(search_results['results']):
        recommendations[(index + 1)] = title

    return recommendations


def get_titles_with_original_language(iso_639_1_id):
    """Return recommendations from 2-letter-code.
    
    Accepts a single string of 2 char language.
    Specify an ISO 639-1 string to filter results by their original language value.

    Examples:
        ISO 639-1   English       Endonym
        en	        English       English
        es	        Spanish	      Español
        pt	        Portuguese    Português
        zh	        Chinese 	  中文, Zhōngwén
    """

    sort_by = "popularity.desc"

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by={sort_by}&include_adult=false&include_video=false&page=1&with_original_language={iso_639_1_id}"
    # TODO:  decide how to wrangle the different TV/movie endpoints??
    # https://developers.themoviedb.org/3/discover/tv-discover

    response = requests.get(url)

    search_results = json.loads(response.text)

    recommendations = dict()
    
    for index, title in enumerate(search_results['results']):
        recommendations[(index + 1)] = title

    return recommendations


def get_title_by_imdbid(imdb_id):
    """Given IMDB id return title info from TMDB.

    >>> get_title_by_imdbid('tt0084237')
    {'movie_results': [{'adult': False, 'backdrop_path': '/fwxOQkzYtRVKs3kzcyukdbsyIuh.jpg', 'genre_ids': [14, 16, 10751, 12], 'id': 10150, 'original_language': 'en', 'original_title': 'The Last Unicorn', 'overview': "From a riddle-speaking butterfly, a unicorn learns that she is supposedly the last of her kind, all the others having been herded away by the Red Bull. The unicorn sets out to discover the truth behind the butterfly's words. She is eventually joined on her quest by Schmendrick, a second-rate magician, and Molly Grue, a now middle-aged woman who dreamed all her life of seeing a unicorn. Their journey leads them far from home, all the way to the castle of King Haggard.", 'poster_path': '/grBct9dkEaI6jnH1jJHEwt3g7T4.jpg', 'release_date': '1982-11-19', 'title': 'The Last Unicorn', 'video': False, 'vote_average': 7.2, 'vote_count': 299, 'popularity': 13.503}], 'person_results': [], 'tv_results': [], 'tv_episode_results': [], 'tv_season_results': []}    
    """

    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id&"

    response = requests.get(url)

    return json.loads(response.text)


def get_IMDB_id_by_movie_id(movie_id):
    """Given TMDB id return IMDB id.

    # TODO:  decide how to wrangle the different TV/movie endpoints??
        #https://developers.themoviedb.org/3/movies/get-movie-external-ids
        #https://developers.themoviedb.org/3/tv/get-tv-external-ids

    >>> get_IMDB_id_by_TMDB_id('603')
    {'id': 603, 'imdb_id': 'tt0133093', 'facebook_id': 'TheMatrixMovie', 'instagram_id': None, 'twitter_id': None}
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids?api_key={TMDB_API_KEY}"

    response = requests.get(url)

    return json.loads(response.text)['imdb_id']


def get_netflix_id_by_IMDB_id(imdb_id):
    """ Pass 'imdbid' to *unofficial* netflix API to receive netflix 'filmid'.

    Accepts string of alpha and numeric chars
        accepts parameter: 'imdbid' which begins with two alpha chars
        returns result: 'filmid' netflix id does not contain alpha chars

    >>> search_by_id('tt0084237')
    '60035334'

    >>> search_by_id(search_by_title('the last unicorn'))
    '60035334'
    """

    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"getimdb","q":f"{imdb_id}"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    n_response = requests.request("GET", url, headers=headers, params=querystring)

    n_list = []
    n_payload = json.loads(n_response.text)
    n_list.append(n_payload)

    n_dictionary = (n_list[0])

    netflix_id = ""

    try:
        if n_dictionary['filmid']:
            netflix_id = n_dictionary['filmid']
    except KeyError:
        netflix_id = False

    return netflix_id


def get_netflix_details_by_netflix_id(netflix_id):
    """Pass 'netflix_id' to receive all KVPs

    >>> get_netflix_details_by_netflix_id('60035334')['image1']
    'https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg'
    """
    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"t":"loadvideo","q":f"{netflix_id}"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    response = requests.request("GET", url, headers=headers, params=querystring)

    n_list = []
    n_payload = json.loads(response.text)
    n_list.append(n_payload)

    n_dictionary = n_list[0].values()
    new_list = list(n_dictionary)
    n_str_result = new_list[0]

    #extract a *dictionary* of the NETFLIX specific data 
    nfinfo = n_str_result['nfinfo']
    nfinfo['runtime'] = '' # <-- strip this runtime, it's a mash of hrs and mins

    #extract a *dictionary* of the IMDB specific data 
    imdbinfo = n_str_result['imdbinfo'] # <-- we get runtime in just mins here

    #combine the imdbinfo KVPs into one dictionary
    dictionary_results =  {}

    # Make sure every key of the 2 dictionaries get into the final dictionary
    dictionary_results.update(nfinfo)
    dictionary_results.update(imdbinfo)

    #extract and append key:value(list) of GENRE NAMES
    dictionary_results['mgname'] = n_str_result['mgname']

    #extract and append key:value(list) of GENRE IDs
    dictionary_results['genreid'] = n_str_result['Genreid']  
    #  yes, that's a capital "G" for some reason  ^

    #return one big flattened dictionary of all of the KVPs from the API response
    return dictionary_results


def get_imdb_details_with_imdb_id(imdb_id):
    """Pass imdb_id to receive useful imdb rating/etc data.
    
    >>> get_imdb_details_with_imdb_id('tt0036855')['Year']
    '1944'
    """

    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

    querystring = {"i":f"{imdb_id}","r":"json"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }
    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')

    response = requests.request("GET", url, headers=headers, params=querystring)

    search_results = json.loads(response.text)

    ratings = {}

    for rating in search_results['Ratings']:
        key_name = str(rating['Source']).lower().replace(" ", "_")
        search_results["ratings_"+key_name] = rating

    return search_results


def get_image_with_movie_id(movie_id):
    """Return image types and paths from movie id.

    # TODO:  decide how to wrangle the different TV/movie endpoints??
        # https://developers.themoviedb.org/3/movies/get-movie-images
        # https://developers.themoviedb.org/3/tv/get-tv-images
        
    >>> get_image_with_movie_id(603).keys()
    dict_keys(['id', 'backdrops', 'posters'])
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={TMDB_API_KEY}"

    response = requests.get(url)

    return json.loads(response.text)


def get_keywords_with_movie_id(movie_id):
    """Return keywords for a given movie id.

    # TODO:  decide how to wrangle the different TV/movie endpoints??
        # https://developers.themoviedb.org/3/movies/get-movie-keywords
        # https://developers.themoviedb.org/3/tv/get-tv-keywords
        
    >>> get_keywords_with_movie_id(603)
    [{'id': 83, 'name': 'saving the world'}, {'id': 310, 'name': 'artificial intelligence'}, {'id': 312, 'name': 'man vs machine'}, {'id': 490, 'name': 'philosophy'}, {'id': 530, 'name': 'prophecy'}, {'id': 779, 'name': 'martial arts'}, {'id': 1430, 'name': 'self sacrifice'}, {'id': 1721, 'name': 'fight'}, {'id': 3074, 'name': 'insurgence'}, {'id': 4563, 'name': 'virtual reality'}, {'id': 4565, 'name': 'dystopia'}, {'id': 6256, 'name': 'truth'}, {'id': 12190, 'name': 'cyberpunk'}, {'id': 186789, 'name': 'dream world'}, {'id': 187056, 'name': 'woman director'}, {'id': 194063, 'name': 'messiah'}, {'id': 221385, 'name': 'gnosticism'}]
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={TMDB_API_KEY}"

    response = requests.get(url)

    search_results = json.loads(response.text)

    return search_results['keywords']


def get_providers_in_USA_with_movie_id(movie_id):
    """Return online movie providers from movie id.

    Returns US response only.
    600+ other options available.

    # TODO:  decide how to wrangle the different TV/movie endpoints??
        # https://developers.themoviedb.org/3/movies/get-movie-details
        # https://developers.themoviedb.org/3/tv/get-tv-details
        
    >>> get_providers_in_USA_with_movie_id(603).keys()
    dict_keys(['flatrate', 'rent', 'buy'])
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"

    response = requests.get(url)

    search_results = json.loads(response.text)

    providers = dict()

    # # bubble up the US service results into the top layer of dict
    try:
        if search_results['results']['US']['flatrate']:
            providers['flatrate'] = search_results['results']['US']['flatrate']
    except KeyError:
        providers['flatrate'] = None
    
    try:
        if search_results['results']['US']['rent']:
            providers['rent'] = search_results['results']['US']['rent']
    except KeyError:
        providers['rent'] = None
    
    try:
        if search_results['results']['US']['buy']:
            providers['buy'] = search_results['results']['US']['buy']
    except KeyError:
        providers['buy'] = None

    return providers


def get_person_details_from_person_id(person_id):
    """Return recommendations from people_id.

    # https://developers.themoviedb.org/3/people/get-person-details
    # https://developers.themoviedb.org/3/people/get-person-combined-credits
    # https://developers.themoviedb.org/3/people/get-person-external-ids
    
    >>> get_person_details_from_person_id(15309)['name']
    'Lori Petty'
    """

    url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={TMDB_API_KEY}&append_to_response=combined_credits,external_ids"

    response = requests.get(url)

    search_results = json.loads(response.text)

    # bubble up the IDs into the top layer of dict
    for external_source in search_results['external_ids'].keys():
        search_results[external_source] = search_results['external_ids'][external_source]

    return search_results


def get_top_10_cast_from_credits_with_movie_id(movie_id):
    """ Return the top 10 cast by popularity for given movie.

    >>> get_top_10_cast_from_credits_with_movie_id(550)['actors'][0]['id']
    287
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"

    response = requests.get(url)

    search_results = json.loads(response.text)

    layer = {}

    for person in search_results['cast']:
        layer[person['popularity']] = person

    dictionary_items = layer.items()

    sorted_cast = sorted(layer.items())
    
    actors = []
    # append top 10 cast
    for person in sorted_cast[-1:-11:-1]:
        actors.append(person[1])

    directors = []
    # append directors
    for index, person in enumerate(search_results['crew']):
        if 'job' in person.keys():
            if 'Director' in person.values():
                directors.append(person)

    composers = []
    # append composers
    for index, person in enumerate(search_results['crew']):
        if 'job' in person.keys():
            if 'Original Music Composer' in person.values():
                composers.append(person)

    people = {}

    people['actors'] = actors
    people['directors'] = directors
    people['composers'] = composers

    return people


def get_basic_details_with_movie_id(movie_id):
    """Return preliminary movie details from movie id.

    # TODO:  decide how to wrangle the different TV/movie endpoints??
        # https://developers.themoviedb.org/3/movies/get-movie-details
        # https://developers.themoviedb.org/3/tv/get-tv-details
        
    >>> get_basic_details_with_movie_id(603)
    {'adult': False, 'backdrop_path': '/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg', 'belongs_to_collection': {'id': 2344, 'name': 'The Matrix Collection', 'poster_path': '/lh4aGpd3U9rm9B8Oqr6CUgQLtZL.jpg', 'backdrop_path': '/bRm2DEgUiYciDw3myHuYFInD7la.jpg'}, 'budget': 63000000, 'genres': [{'id': 28, 'name': 'Action'}, {'id': 878, 'name': 'Science Fiction'}], 'homepage': 'http://www.warnerbros.com/matrix', 'id': 603, 'imdb_id': 'tt0133093', 'original_language': 'en', 'original_title': 'The Matrix', 'overview': 'Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.', 'popularity': 49.914, 'poster_path': '/vybQQ7w7vGvF53IsGD0y0JSgIsA.jpg', 'production_companies': [{'id': 79, 'logo_path': '/tpFpsqbleCzEE2p5EgvUq6ozfCA.png', 'name': 'Village Roadshow Pictures', 'origin_country': 'US'}, {'id': 372, 'logo_path': None, 'name': 'Groucho II Film Partnership', 'origin_country': ''}, {'id': 1885, 'logo_path': '/xlvoOZr4s1PygosrwZyolIFe5xs.png', 'name': 'Silver Pictures', 'origin_country': 'US'}, {'id': 174, 'logo_path': '/IuAlhI9eVC9Z8UQWOIDdWRKSEJ.png', 'name': 'Warner Bros. Pictures', 'origin_country': 'US'}], 'production_countries': [{'iso_3166_1': 'AU', 'name': 'Australia'}, {'iso_3166_1': 'US', 'name': 'United States of America'}], 'release_date': '1999-03-30', 'revenue': 463517383, 'runtime': 136, 'spoken_languages': [{'english_name': 'English', 'iso_639_1': 'en', 'name': 'English'}], 'status': 'Released', 'tagline': 'Welcome to the Real World.', 'title': 'The Matrix', 'video': False, 'vote_average': 8.1, 'vote_count': 18136}
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

    response = requests.get(url)

    search_results = json.loads(response.text)

    return search_results


def get_full_details_with_movie_id(movie_id, language_id='en'):
    """Return comprehensive movie details from movie id.

    # TODO:  decide how to wrangle the different TV/movie endpoints??
        # https://developers.themoviedb.org/3/movies/get-movie-details
        # https://developers.themoviedb.org/3/tv/get-tv-details
        
    >>> get_full_details_with_movie_id(603)['title']
    The Matrix

    >>> get_full_details_with_movie_id(603)['keywords']
    {'keywords': [{'id': 83, 'name': 'saving the world'}, {'id': 310, 'name': 'artificial intelligence'}, {'id': 312, 'name': 'man vs machine'}, {'id': 490, 'name': 'philosophy'}, {'id': 530, 'name': 'prophecy'}, {'id': 779, 'name': 'martial arts'}, {'id': 1430, 'name': 'self sacrifice'}, {'id': 1721, 'name': 'fight'}, {'id': 3074, 'name': 'insurgence'}, {'id': 4563, 'name': 'virtual reality'}, {'id': 4565, 'name': 'dystopia'}, {'id': 6256, 'name': 'truth'}, {'id': 12190, 'name': 'cyberpunk'}, {'id': 186789, 'name': 'dream world'}, {'id': 187056, 'name': 'woman director'}, {'id': 194063, 'name': 'messiah'}, {'id': 221385, 'name': 'gnosticism'}]}

    >>> get_full_details_with_movie_id(603, 'zh')['images']['posters']
    [{'aspect_ratio': 0.6706349206349206, 'file_path': '/qwFRLa87lFLhuXi0Is33jMBSuUB.jpg', 'height': 1008, 'iso_639_1': None, 'vote_average': 5.312, 'vote_count': 1, 'width': 676}, {'aspect_ratio': 0.6708407871198568, 'file_path': '/vsTC6jddyfy25GirpCVtZ7GOB7A.jpg', 'height': 1118, 'iso_639_1': 'zh', 'vote_average': 0.0, 'vote_count': 0, 'width': 750}, {'aspect_ratio': 0.6741573033707865, 'file_path': '/uSgDJaLSFh2oOUMRevaxJWwbh4b.jpg', 'height': 1780, 'iso_639_1': 'zh', 'vote_average': 0.0, 'vote_count': 0, 'width': 1200}]
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=similar,images&include_image_language={language_id},null"

    response = requests.get(url)

    search_results = json.loads(response.text)

    # pull "similar" nested info up a level, so it can be displayed in jinja
    similar_titles = dict()

    try:
        for title in search_results['similar']['results']:
            similar_titles[title['id']] = title

    except KeyError:
        pass

    search_results['similar'] = similar_titles

    # append the keyword data so it ends up in the same level of the dict as the 
    # rest of the data/KVPs
    try:
        search_results['keywords'] = get_keywords_with_movie_id(movie_id)

    except KeyError:
        pass
    
    # append the people data so it ends up in the same level of the dict
    try:
        people = get_top_10_cast_from_credits_with_movie_id(movie_id)

        for key, value in people.items():
            search_results[key] = value

    except KeyError:
        pass
    
    # append the provider data so it ends up in the same level of the dict
    try:
        providers = get_providers_in_USA_with_movie_id(movie_id)

        for key, value in providers.items():
            search_results[key] = value

    except KeyError:
        pass

    # append Netflix data if Netflix is an available provider
    try:
        if providers['flatrate'] != None:
            for provider in providers['flatrate']:
                if provider['provider_name'] == 'Netflix':

                    imdb_id = search_results['imdb_id']
                    search_results['netflix_id'] = get_netflix_id_by_IMDB_id(imdb_id)
                    netflix_info = get_netflix_details_by_netflix_id(search_results['netflix_id'])
        
                    search_results['netflix_matlevel'] = netflix_info['matlevel']
                    search_results['netflix_matlabel'] = netflix_info['matlabel']
                    search_results['netflix_type'] = netflix_info['type']
                    search_results['netflix_downloadable'] = netflix_info['download']
                    search_results['netflix_metascore'] = netflix_info['metascore']
                    search_results['netflix_awards'] = netflix_info['awards']
                    search_results['netflix_genres'] = netflix_info['mgname']
                    search_results['netflix_genreids'] = netflix_info['genreid']
                    search_results['netflix_image1'] = netflix_info['image1']
                    search_results['netflix_image2'] = netflix_info['image2']

    except KeyError:
        pass

    # append IMDb info with better ratings data, etc
    try:
        imdb_data = get_imdb_details_with_imdb_id(search_results['imdb_id'])
        
        for key, value in imdb_data.items():
            
            # key_term = str(key)
            key_phrase = "imdb_" + str(key).lower()

            search_results[key_phrase] = value

    except KeyError:
        pass

    return search_results

    # TODO: debug items that aren't actually found
    # TODO: {'success': False, 'status_code': 34, 'status_message': 'The resource you requested could not be found.', 'similar': {}, 'flatrate': None, 'rent': None, 'buy': None}


def discover_films_by_parameters(current_user, movie_or_series, audio, end_year, start_rating, genre_list):
    """ Return a number of results based on parameters from User.

    All of the front end parameters are optional.
    Some ordering/sorting will be handled on the front end instead of via querystring parameter
    """
    base_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=popularity.desc&include_adult=false&page=5"

    print()
    print()
    print()
    print()
    print()
    print(audio)
    print()
    print()
    print()
    print()

    if audio != "any":
        base_url = f"{base_url}&with_original_language={audio}"

    # if start_year != "any":
    #     base_url = f"{base_url}&release_date.gte={start_year}"

    print()
    print()
    print()
    print()
    print()
    print(base_url)
    print()
    print()
    print()
    print()

    if end_year != "any":
        base_url = f"{base_url}&release_date.lte={end_year}"

    if start_rating != "any":
        base_url = f"{base_url}&vote_average.gte={start_rating}"

    if genre_list != "any":
        base_url = f"{base_url}&&with_genres={genre_list}"

    response = requests.get(base_url)

    search_results = json.loads(response.text)

    print()
    print()
    print()
    print()
    print()
    print(base_url)
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print(search_results)
    print()
    print()
    print()
    print()



    recommendations = dict()
    count = 1
    
    for index, title in enumerate(search_results['results']):
        recommendations[title['id']] = title
    


    print()
    print()
    print()
    print()
    print()
    print(recommendations)
    print()
    print()
    print()
    print()

    return recommendations



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    import doctest
    doctest.testmod()
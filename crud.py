"""CRUD operations."""

from model import db, User, Preference, QueryHistory, Location, Genre, GenrePreference, connect_to_db
import datetime
import os
import sys
import requests
import json
from urllib.parse import quote, unquote
from sqlalchemy import update

LANGUAGES = {"audio": ["Arabic", "Cantonese", "Croatian", "English", "Filipino", "French", "German", "Gujarati", "Hebrew", "Hindi", "Italian", "Japanese", "Khmer", "Korean", "Mandarin", "Persian", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", "Tagalog", "Thai", "Urdu", "Vietnamese", "Yiddish"], "subtitles": ["Croatian", "English", "Filipino", "French", "German", "Hebrew", "Hindi", "Italian", "Japanese", "Korean", "Persian", "Polish", "Portuguese", "Russian", "Spanish", "Tagalog", "Thai", "Traditional Chinese", "Vietnamese"]}

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
    db.session.commit()  #TODO:  going to need to loop through a second pass to set PURL_name = User.ID

    return user


# def get_all_users():
#     """Return all users."""

#     return User.query.all()


def get_user_by_email(email):
    """Return a user by unique email address.
    
    >>> get_user_by_email(jane.doe@email.com)
    <User id=1 email=jane.doe@email.com>
    """

    return User.query.filter(User.email == email).first()    
                       

def update_user_fname(user_id, name):
    """Update the fname of an existing user.
    
    The new name will be captured via user input field.

    >>> update_user_name("1", "jane")
    # TODO: update docstring
    """

    user = User.query.get(user_id)
    user.fname = name
    db.session.commit()

    return user

def update_user_email(user_id, email):
    """Update the email of an existing user.
    
    The new email will be captured via user input field.
    Validation will happen upstream.

    >>> update_user_name(user, "jane@email.com")
    # TODO: update docstring
    """

    user = User.query.get(user_id)
    user.email = email
    db.session.commit()

    return user

def update_user_password(user_id, password):
    """Update the password of an existing user.
    
    The new password will be captured via user input field.
    Validation will happen upstream.

    >>> update_user_name(user, "JANESpassword1")
    # TODO: update docstring
    """

    user = User.query.get(user_id)
    user.password = password
    db.session.commit()

    return user


#  don't forget to update line 74, too.  need to set an intial unique default for successful page load
# def update_user_purl(user_id, name):
#     """Update the unique PURL parameter of an existing user.
    
#     The new parameter/alias/string/name will be captured via user input field.
#     Validation will happen upstream.

#     >>> update_user_name(user, "wombat")
#     # TODO: update docstring
#     """

#     user = User.query.get(user_id)
#     user.purl_name = name
#     db.session.commit()

#     return user


#*############################################################################*#
#*#                           USERNETWORK OPERATIONS                         #*#
#*############################################################################*#

def add_user_connection(requestee, user):                                       # // TODO:  what params?
    """Create and store a user's social network connection invitation.

    new connection should get created:
    >>> add_user_connection(1, 2)
    <UserNetwork id=1 status="Pending" requestor_id:1 requestee_id:2>           # TODO: validate docstring response

    user shouldn't be both requestor and requestee                              # TODO:  add in this logic with if statement?
    >>> add_user_connection(1, 2)
    <UserNetwork id=1 status="Pending" requestor_id:1 requestee_id:2>           # TODO: validate docstring response

    only one record should exist per requestor+requestee+status combination     # TODO:  add in this logic with if statement?
    >>> add_user_connection(1, 2)
    <UserNetwork id=1 status="Pending" requestor_id:1 requestee_id:2>           # TODO: validate docstring response
    """

    user_connection = db.UserNetwork(requestor_id = User.query.get(id),
                                    requestee_id = requestee.id,
                                    status = "Pending",
                                    connection_date = datetime.datetime.now())                   

    db.session.add(user_connection)
    db.session.commit()

    return user_connection

# def update_user_connection_by_id(connection_id):
#     """Update a UserNetwork by primary key

#     # TODO: update docstring with doctest
#     """

#     pass


def get_connections_by_user(user):                                              # TODO: implement new feature later to update/"approve" pending connection requests
    """Return all of a User's requested connections.

    Should return all requested connections, regardless of outcome/status.

    # TODO: update docstring with doctest
    """

    return UserNetwork.query.filter(UserNetwork.requestor_id == (User.id))

    
# def get_pending_connections_by_user(user):                                    # TODO: implement new feature later to approve pending connection requests
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

def add_user_preference_to_preferences(user, param_subtitle="any",                 # TODO:  what params?
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


def add_genre_preference(user, param_genre):
    """ Create a genre preference for a user.

    >>> add_genre_preference('1', '[7442]')
    {self.id}
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
    """Return the most recent collection of this User's default preferences."""
    
    current_user_prefs = Preference.query.filter(Preference.user_id==User.id)  

    return current_user_prefs                                                                   # TODO:  get only the most recent entry in the table, like, the largest ID?


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
    <GenrePreference id={self.id} user="1" genre='[7442]' isActive=False>'
    """

    user_genre_preference = GenrePreference.query.filter(user_id, genre_id, isActive != false).all()
    genre_prefs.isActive = False
    db.session.commit()

    return user_genre_preference


#*############################################################################*#
#*#                            QUERY OPERATIONS                              #*#
#*############################################################################*#

def search_by_title(str):
    """ Pass movie title to unofficial imdb API to receive imdb 'id'.

    should begin with two alpha chars

    >>> search_by_title('the last unicorn')
    tt0084237
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
    60035334

    >>> search_by_id(search_by_title('the last unicorn'))
    60035334
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

    >>> get_by_filmid('60035334')
    {"RESULT":{"nfinfo":{"image1":"https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg","title":"The Last Unicorn","synopsis":"This animated tale follows a unicorn who believes she may be the last of her species and is searching high and low for someone just like her.","matlevel":"35","matlabel":"Contains nothing in theme, language, nudity, sex, violence or other matters that, in the view of the Rating Board, would offend parents whose younger children view the motion picture","avgrating":"3.8214536","type":"movie","updated":"","unogsdate":"2015-07-10 01:09:00","released":"1982","netflixid":"60035334","runtime":"1h32m","image2":"https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg","download":"1"},"imdbinfo":{"rating":"7.5","votes":"23234","metascore":"70","genre":"Animation, Adventure, Drama, Family, Fantasy","awards":"1 nomination.","runtime":"92 min","plot":"From a riddle-speaking butterfly, a unicorn learns that she is supposedly the last of her kind, all the others having been herded away by the Red Bull. The unicorn sets out to discover the truth behind the butterfly&amp;#39;s words. She is eventually joined on her quest by Schmendrick, a second-rate magician, and Molly Grue, a now middle-aged woman who dreamed all her life of seeing a unicorn. Their journey leads them far from home, all the way to the castle of King Haggard...","country":"UK, France, West Germany, Japan, USA","language":"English, German","imdbid":"tt0084237"},"mgname":["Animal Tales","Family Sci-Fi & Fantasy","Children & Family Films","Films for ages 8 to 10","Films based on childrens books","Films for ages 11 to 12"],"Genreid":["5507","52849","783","561","10056","6962"],"people":[{"actor":["Alan Arkin","Jeff Bridges","Mia Farrow","Tammy Grimes","Angela Lansbury","Robert Klein","Keenan Wynn","Christopher Lee","Rene Auberjonois","Paul Frees","Jack Lester","Brother Theodore","Don Messick","Ed Peck","Kenneth Jennings","Nellie Bellflower"]},{"creator":["Peter S. Beagle"]},{"director":["Jules Bass","Arthur Rankin Jr."]}],"country":[]}}

    >>> search_by_id(search_by_title('the last unicorn'))
    60035334
    """
    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    #querystring = {"t":"loadvideo","q":f"{str}"}                               # TODO:  rawr!  figure out how to unpack dicts that are 3-layers deep
    querystring = {"t":"getimdb","q":f"{str}"}                                  # this one is the imdb info, not the netflix info

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

    print(imdb_dictionary)
    return imdb_dictionary


def get_movie_details_by_filmid(str):
    """Pass 'filmid' to receive all KVPs

    >>> get_nfinfo_details_by_filmid('60035334')
    {'image1': \
    'https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg', \
    'title': 'The Last Unicorn', 'synopsis': 'This animated tale follows a \
    unicorn who believes she may be the last of her species and is  searching \
    high and low for someone just like her.', 'matlevel': '35', 'matlabel': \
    'Contains nothing in theme, language, nudity, sex, violence or other \
    matters that, in the view of the Rating Board, would offend parents whose \
    younger children view the motion picture', 'avgrating': '3.8214536', \
    'type': 'movie', 'updated': '', 'unogsdate': '2015-07-10 01:09:00', \
    'released': '1982', 'netflixid': '60035334', 'runtime': '92 min', \
    'image2': 'https://art-s.nflximg.net/2c5cb/e26fea88e4b62bc7f1eeeb8db2a7268e6dd2c5cb.jpg', \
    'download': '1', 'rating': '7.5', 'votes': '23234', 'metascore': '70', \
    'genre': 'Animation, Adventure, Drama, Family, Fantasy', 'awards': \
    '1 nomination.', 'plot': 'From a riddle-speaking butterfly, a unicorn \
    learns that she is supposedly the last of her kind, all the others having \
    been herded away by the Red Bull. The unicorn sets out to discover the \
    truth behind the butterfly&amp;#39;s words. She is eventually joined on \
    her quest by Schmendrick, a second-rate magician, and Molly Grue, a now \
    middle-aged woman who dreamed all her life of seeing a unicorn. Their \
    journey leads them far from home, all the way to the castle of King \
    Haggard...', 'country': [], 'language': 'English, German', 'imdbid': \
    'tt0084237', 'mgname': ['Animal Tales', 'Family Sci-Fi & Fantasy', \
    'Children & Family Films', 'Films for ages 8 to 10', 'Films based on \
    childrens books', 'Films for ages 11 to 12'], 'genreid': ['5507', '52849', \
    '783', '561', '10056', '6962'], 'actors': ['Alan Arkin', 'Jeff Bridges', \
    'Mia Farrow', 'Tammy Grimes', 'Angela Lansbury', 'Robert Klein', \
    'Keenan Wynn', 'Christopher Lee', 'Rene Auberjonois', 'Paul Frees', \
    'Jack Lester', 'Brother Theodore', 'Don Messick', 'Ed Peck', \
    'Kenneth Jennings', 'Nellie Bellflower'], 'creators': ['Peter S. Beagle'], \
    'directors': ['Jules Bass', 'Arthur Rankin Jr.']}
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
    


#* TEST TO RETURN A MOVIE BASED ON A STRING OF IT'S TITLE:
#current_result = crud.get_by_filmid((crud.search_by_id(crud.search_by_title('the last unicorn'))))


#*############################################################################*#
#*#                        QUERYHISTORY OPERATIONS                           #*#
#*############################################################################*#

def add_query_to_query_history(user, query_string, 
    payload, param_subtitle="", param_audio="", param_genre="", 
    param_release_date_start="", param_release_date_end="", param_duration="", 
    param_total_seasons=""):          # TODO:  what params?
    """Create a new entry in Query History with query results                   # TODO: update docstring with doctest
    """

    query = QueryHistory(user_id = (User.query.get(id)),
        query_run_date_time = datetime.datetime.now(),
        query_string = query_string,
        payload = payload,
        param_subtitle = param_subtitle,
        param_audio = param_audio,
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


#*############################################################################*#
#*#                                DB OPERATIONS                             #*#
#*############################################################################*#

def get_all_locations():
    """ Return a dictionary of each of Netflix's service locations.

    #>>>get_all_locations()
    # TODO:  erm, is there a way to limit to, like, top1 result here?
    # that would be:
    #{'All Action': [10673, 10702, 11804, 11828, 1192487, 1365, 1568, 2125, 2653, 43040, 43048, 4344, 46576, 75418, 76501, 77232, 788212, 801362, 852490, 899, 9584]}
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
    # TODO: update docstring"""

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

    #>>>get_all_genres()
    # TODO:  erm, is there a way to limit to, like, top1 result here?
    # that would be:
    #{'All Action': [10673, 10702, 11804, 11828, 1192487, 1365, 1568, 2125, 2653, 43040, 43048, 4344, 46576, 75418, 76501, 77232, 788212, 801362, 852490, 899, 9584]}
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


def create_genre(genre_id, genre_name):
    """Create and return a new Genre.

    >>> create_genre('10118', 'Comic book and superhero movies')
    # TODO: update docstring"""

    genre = Genre(id=genre_id,
                name = genre_name)

    db.session.add(genre)
    db.session.commit() 

    return genre


def get_all_genres():
    """Return all of the available genres."""
                   
    #return User.query.filter(User.email == email).first()    
    return Genre.query.filter().all()   




if __name__ == '__main__':
    from server import app
    connect_to_db(app)
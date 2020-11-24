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

def search_films_by_parameters(search_term, genre_list, movie_or_series, start_rating, end_rating, start_year, end_year, new_date, subtitle, audio, country_list):
    """ Return a number of results based on parameters from User.

    All of the front end parameters are optional.
    Ordering/sorting will be handled on the front end instead of via querystring parameter

    >>> search_films_by_parameters("the last Unicorn", "", "", 5, 10, 1970, 2020, "", "", "", "")
    [{'vtype': 'series', 'img': 'https://occ-0-2218-2219.1.nflxso.net/dnm/api/v6/evlCitJPPCVCry0BZlEFb5-QjKc/AAAABf_yO5gOqfvRDqXfZchg9ysuqquBHNcUGu7I4OrjoH0az-nZA95YDPowaJ62xdKREiX43b-6DiIHLm5WWTaEN0GAPg.jpg?r=004', 'nfid': 81190627, 'imdbid': 'tt10329028', 'title': 'The Unicorn', 'clist': '"US":"United States"', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjMyZTdlNjAtODZmOC00OGI2LTliOWEtNThmYjNiN2E2Njk2XkEyXkFqcGdeQXVyNjg4NzAyOTA@._V1_SX300.jpg', 'imdbrating': 7.1, 'top250tv': 0, 'synopsis': 'A widowed father of two girls navigates the world of dating, surprised to learn that many women consider him a hot commodity.', 'titledate': '2020-11-03', 'avgrating': 0.0, 'year': 2019, 'runtime': 0, 'top250': 0, 'id': 67089}, {'vtype': 'movie', 'img': 'https://occ-0-2851-38.1.nflxso.net/dnm/api/v6/evlCitJPPCVCry0BZlEFb5-QjKc/AAAABc001T5vhL0kgjnVsvwBAotinqk-GwLwGliKtwmCh44P_U4tXxGjmzMNqW_bTY8hUC7yIE9LcVAu__JsF7wakKDyBagtnuLDVA-BG7lJAWK4tt-AFjgEb5H_fiQ.jpg?r=cb3', 'nfid': 81034317, 'imdbid': 'tt2338454', 'title': 'Unicorn Store', 'clist': '"CA":"Canada","FR":"France","DE":"Germany","NL":"Netherlands","PL":"Poland","GB":"United Kingdom","US":"United States","AR":"Argentina","AU":"Australia","BE":"Belgium","more":"+22"', 'poster': 'https://m.media-amazon.com/images/M/MV5BMjUyMTY2OTkwMF5BMl5BanBnXkFtZTgwODEyODA3NzM@._V1_SX300.jpg', 'imdbrating': 5.5, 'top250tv': 0, 'synopsis': 'After failing out of art school and taking a humdrum office job, a whimsical painter gets a chance to fulfill her lifelong dream of adopting a unicorn.', 'titledate': '2019-04-05', 'avgrating': 0.0, 'year': 2019, 'runtime': 5513, 'top250': 0, 'id': 61649}]

    """


    url = "https://unogsng.p.rapidapi.com/search"

    #OPTIONAL PARAMETERS
    query_param = search_term           # any string you want to search (fulltext against the title) 
    genre_list = genre_list     # comma-separated list of Netflix genre id's (see genre endpoint for list)
    movie_or_series = movie_or_series # movie or series?

    start_rating = start_rating # imdb rating 0-10
    end_rating = end_rating     # imdb rating 0-10

    start_year = start_year     # 4 digit year
    end_year = end_year         # 4 digit year

    new_date = new_date         # something new-ish where streaming began after this date 

    subtitle = subtitle        # *ONE* valid language type
    audio = audio              # *ONE* valid language type
    audiosubtitle_andor = ""    # ehhhh... 
                                #after testing, it turns out this parameter doesn't actually impact results -- at all

    country_list = country_list # comma-separated list of uNoGS country ID's (from country endpoint) leave blank for all country search
    country_andorunique = "or"  # returns results based on user locations (and/or/unique)
                                # setting to "or" to return results matching any country in the list 

    order_by = ""                # orderby string (date,rating,title,type,runtime)
    limit = "100"                  # Limit of returned items default (MAX 100)
    offset = "0"                 # Starting Number of results (Default is 0)

    # querystring = {"newdate": f"{new_date}","genrelist": f"{genre_list}","type": f"{movie_or_series}","start_year": f"{start_year}","orderby": f"{order_by}","audiosubtitle_andor": f"{audiosubtitle_andor}","start_rating": f"{start_rating}","limit": f"{limit}","end_rating": f"{end_rating}","subtitle": f"{subtitle}","countrylist": f"{country_list}","query": f"{query_param}","audio": f"{audio}","country_andorunique": f"{country_andorunique}","offset": f"{offset}","end_year": f"{end_year}"}

    querystring = {"newdate": f"","genrelist": f"","type": f"movie","start_year": f"","orderby": f"","audiosubtitle_andor": f"","start_rating": f"","limit": f"","end_rating": f"","subtitle": f"","countrylist": f"","query": f"unicorn","audio": f"","country_andorunique": f"","offset": f"","end_year": f""}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    headers['x-rapidapi-key'] = os.environ.get('API_TOKEN_1')  

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    print(response)

    #take the response and unpack it into a workable format
    search_results = json.loads(response.text)
    search_results_values = search_results.values()

    #extract the embedded dictionary from 2 levels down in results
    listify_results = list(search_results_values)
    result_list = listify_results[2]  
    
    print(querystring)
    print(result_list)

    return result_list


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
    

def get_all_films_by_person_name(input_name):
    """ Get all films with a person's name. 

    Argument can be either a full name, surname, etc. 
    Argument must be an exact match for spelling and punctuation.
    No, you can't pass "the Prince symbol" here.

    Person should be able to be any named production role, not just an actor: #but apparenlty right now it's only pulling actors
     - actor
     - director
     - creator

    >>> get_all_films_by_person_name("Britney Spears")  
    {'fullname': 'Britney Spears', 'netflixid': 60022266, 'title': 'Crossroads'}

    >>> get_all_films_by_person_name("Peter Ostrum")
    {'fullname': 'Peter Ostrum', 'netflixid': 60020949, 'title': 'Willy Wonka and the Chocolate Factory'}
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
    
    return result_list


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

    >>> get_all_locations()
    [{'country': 'Argentina ', 'id': 21, 'countrycode': 'AR'}, {'country': 'Australia ', 'id': 23, 'countrycode': 'AU'}, {'country': 'Belgium ', 'id': 26, 'countrycode': 'BE'}, {'country': 'Brazil ', 'id': 29, 'countrycode': 'BR'}, {'country': 'Canada ', 'id': 33, 'countrycode': 'CA'}, {'country': 'Switzerland ', 'id': 34, 'countrycode': 'CH'}, {'country': 'Germany ', 'id': 39, 'countrycode': 'DE'}, {'country': 'France ', 'id': 45, 'countrycode': 'FR'}, {'country': 'United Kingdom', 'id': 46, 'countrycode': 'GB'}, {'country': 'Mexico ', 'id': 65, 'countrycode': 'MX'}, {'country': 'Netherlands ', 'id': 67, 'countrycode': 'NL'}, {'country': 'Sweden ', 'id': 73, 'countrycode': 'SE'}, {'country': 'United States', 'id': 78, 'countrycode': 'US'}, {'country': 'Iceland ', 'id': 265, 'countrycode': 'IS'}, {'country': 'Japan ', 'id': 267, 'countrycode': 'JP'}, {'country': 'Portugal ', 'id': 268, 'countrycode': 'PT'}, {'country': 'Italy ', 'id': 269, 'countrycode': 'IT'}, {'country': 'Spain ', 'id': 270, 'countrycode': 'ES'}, {'country': 'Czech Republic ', 'id': 307, 'countrycode': 'CZ'}, {'country': 'Greece ', 'id': 327, 'countrycode': 'GR'}, {'country': 'Hong Kong ', 'id': 331, 'countrycode': 'HK'}, {'country': 'Hungary ', 'id': 334, 'countrycode': 'HU'}, {'country': 'Israel ', 'id': 336, 'countrycode': 'IL'}, {'country': 'India ', 'id': 337, 'countrycode': 'IN'}, {'country': 'South Korea', 'id': 348, 'countrycode': 'KR'}, {'country': 'Lithuania ', 'id': 357, 'countrycode': 'LT'}, {'country': 'Poland ', 'id': 392, 'countrycode': 'PL'}, {'country': 'Romania ', 'id': 400, 'countrycode': 'RO'}, {'country': 'Russia', 'id': 402, 'countrycode': 'RU'}, {'country': 'Singapore ', 'id': 408, 'countrycode': 'SG'}, {'country': 'Slovakia ', 'id': 412, 'countrycode': 'SK'}, {'country': 'Thailand ', 'id': 425, 'countrycode': 'TH'}, {'country': 'Turkey ', 'id': 432, 'countrycode': 'TR'}, {'country': 'South Africa', 'id': 447, 'countrycode': 'ZA'}]
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


def create_genre(genre_id, genre_name):
    """Create and return a new Genre.

    >>> create_genre('10118', 'Comic book and superhero movies')
    <GenrePreference id=5 user=1 genre_name=Comic Book and Superhero Movies isActive=True>
    """

    genre = Genre(id=genre_id,
                name = genre_name)

    db.session.add(genre)
    db.session.commit() 

    return genre


def get_stored_genres():
    """Return all of the available genres."""
                     
    return Genre.query.filter().all()   




if __name__ == '__main__':
    from server import app
    connect_to_db(app)
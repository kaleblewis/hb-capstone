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

GENRE_GROUPS = {'All Action': [10673, 10702, 11804, 11828, 1192487, 1365, 1568, 2125, 2653, 43040, 43048, 4344, 46576, 75418, 76501, 77232, 788212, 801362, 852490, 899, 9584], 'All Anime': [10695, 11146, 2653, 2729, 3063, 413820, 452, 6721, 7424, 9302], 'All Childrens': [10056, 27480, 27950, 28034, 28083, 28233, 48586, 5455, 561, 6218, 6796, 6962, 78120, 783, 89513], 'All Classics': [10032, 11093, 13158, 29809, 2994, 31273, 31574, 31694, 32392, 46553, 46560, 46576, 46588, 47147, 47465, 48303, 48586, 48744, 76186], 'All Comedies': [1009, 10256, 10375, 105, 10778, 11559, 11755, 1208951, 1333288, 1402, 1747, 17648, 2030, 2700, 31694, 3300, 34157, 3519, 3996, 4058, 4195, 43040, 4426, 4906, 52104, 52140, 52847, 5286, 5475, 5610, 56174, 58905, 59169, 61132, 61330, 6197, 63092, 63115, 6548, 711366, 7120, 72407, 7539, 77599, 77907, 78163, 78655, 79871, 7992, 852492, 869, 89585, 9302, 9434, 9702, 9736], 'All Cult': [10944, 3675, 4734, 74652, 7627, 9434], 'All Documentaries': [10005, 10105, 10599, 1159, 15456, 180, 2595, 26126, 2760, 28269, 3652, 3675, 4006, 4720, 48768, 49110, 49547, 50232, 5161, 5349, 55087, 56178, 58710, 60026, 6839, 7018, 72384, 77245, 852494, 90361, 9875], 'All Dramas': [11, 11075, 11714, 1208954, 1255, 12994, 13158, 2150, 25955, 26009, 2696, 2748, 2757, 2893, 29809, 3179, 31901, 34204, 3653, 3682, 384, 3916, 3947, 4282, 4425, 452, 4961, 500, 5012, 52148, 52904, 56169, 5763, 58677, 58755, 58796, 59064, 6206, 62235, 6616, 6763, 68699, 6889, 711367, 71591, 72354, 7243, 7539, 75459, 76507, 78628, 852493, 89804, 9299, 9847, 9873], 'All Faith and Spirituality': [26835, 52804, 751423], 'All Gay and Lesbian': [3329, 4720, 500, 5977, 65263, 7120], 'All Horror': [10695, 10944, 1694, 42023, 45028, 48303, 61546, 75405, 75804, 75930, 8195, 83059, 8711, 89585], 'All Independent': [11804, 3269, 384, 4195, 56184, 69192, 7077, 875, 9916], 'All International': [1192487, 1195213, 1208951, 1208954, 1218090, 78367, 852488, 852490, 852491, 852492, 852493, 852494], 'All Music': [10032, 10741, 1701, 2222, 2856, 5096, 52843, 6031], 'All Musicals': [13335, 13573, 32392, 52852, 55774, 59433, 84488, 88635], 'All Romance': [29281, 36103, 502675], 'All Sci-Fi': [108533, 11014, 1372, 1492, 1568, 1694, 2595, 2729, 3327, 3916, 47147, 4734, 49110, 50232, 52780, 52849, 5903, 6000, 6926, 852491], 'All Sports': [180, 25788, 4370, 5286, 7243, 9327], 'All Thrillers': [10306, 10499, 10504, 10719, 11014, 11140, 1138506, 1321, 1774, 3269, 43048, 46588, 5505, 58798, 65558, 6867, 75390, 78507, 799, 852488, 8933, 89811, 9147, 972]}

GENRES = {'20th Century Period Pieces': [12739], 'Academy Award-Winning Films': [51063], 'Action': [801362], 'Action & Adventure': [1365], 'Action Comedies': [43040], 'Action Sci-Fi & Fantasy': [1568], 'Action Thrillers': [43048], 'Adult Animation': [11881], 'Adventures': [7442], 'African Movies': [3761], 'African Music': [6031], 'African-American Comedies': [4906], 'African-American Dramas': [9847], 'African-American Stand-up Comedy': [10778], 'Afro-Cuban & Latin Jazz': [5661], 'Alien Sci-Fi': [3327], 'American Folk & Bluegrass': [760], 'Animal Tales': [5507], 'Animals & Nature Reality TV': [50462], 'Anime': [7424], 'Anime Action': [2653], 'Anime Comedies': [9302], 'Anime Dramas': [452], 'Anime Fantasy': [11146], 'Anime Features': [3063], 'Anime Horror': [10695], 'Anime Sci-Fi': [2729], 'Anime Sci-Fi & Fantasy': [1433679], 'Anime Series': [6721], 'Argentinian Dramas': [5923], 'Argentinian Films': [6133], 'Argentinian TV Shows': [69616], 'Art House Movies': [29764], 'Asian Action Movies': [77232], 'Asian Movies': [78104], 'Australian Comedies': [2030], 'Australian Crime Films': [3936], 'Australian Dramas': [11075], 'Australian Movies': [5230], 'Australian Thrillers': [10719], 'Australian TV Programmes': [52387], 'Award-winning Dramas': [89804], 'Award-winning Movies': [89844], 'B-Horror Movies': [8195], 'BAFTA Award-Winning Films': [69946], 'Baseball Movies': [12339], 'Basketball Movies': [12762], 'Belgian Movies': [262], 'Berlin Film Festival Award-winning Movies': [846815], 'Biographical Documentaries': [3652], 'Biographical Dramas': [3179], 'Blockbuster Movies': [90139], 'Blue-collar Stand-up Comedy': [77907], 'Bollywood Films': [5480], 'Boxing Movies': [12443], 'Brazilian Comedies': [17648], 'Brazilian Documentaries': [28269], 'Brazilian Dramas': [4425], 'Brazilian Films': [798], 'Brazilian Music & Musicals': [84488], 'Brazilian Music and Concert Movies': [84489], 'Brazilian TV Shows': [69624], 'British Comedies': [1009], 'British Crime Films': [6051], 'British Dramas': [3682], 'British Miniseries': [52508], 'British Movies': [10757], 'British Period Pieces': [12433], 'British Thrillers': [1774], 'British TV Comedies': [52140], 'British TV Dramas': [52148], 'British TV Mysteries': [52120], 'British TV Shows': [52117], 'British TV Sketch Comedies': [52104], 'Campy Movies': [1252], 'Canadian Comedies': [56174], 'Canadian Documentaries': [56178], 'Canadian Dramas': [56169], 'Canadian Films': [56181], 'Canadian French-Language Movies': [63151], 'Canadian Independent Films': [56184], 'Canadian TV Programmes': [58704], 'Cannes Film Festival Award-winning Movies': [846810], 'Cannes Film Festival Winners': [702387], 'CÃ©sar Award-winning Movies': [846807], 'Children & Family Movies': [783], 'Chinese Movies': [3960], 'Classic Action & Adventure': [46576], 'Classic British Films': [46560], 'Classic Children & Family Films': [48586], 'Classic Comedies': [31694], 'Classic Country & Western': [2994], 'Classic Dramas': [29809], 'Classic Foreign Movies': [32473], 'Classic Horror Films': [48303], 'Classic Movies': [31574], 'Classic Musicals': [32392], 'Classic R&B/Soul': [11093], 'Classic Romantic Movies': [31273], 'Classic Sci-Fi & Fantasy': [47147], 'Classic Thrillers': [46588], 'Classic TV Shows': [46553], 'Classic War Movies': [48744], 'Classic Westerns': [47465], 'Classical Music': [10032], 'Colombian Movies': [69636], 'Comedies': [6548], 'Comedy Jams': [78163], 'Comic Book & Superhero TV': [53717], 'Comic Book and Superhero Movies': [10118], 'Competition Reality TV': [49266], 'Contemporary R&B': [7129], 'Country & Western/Folk': [1105], 'Courtroom Dramas': [528582748], 'Courtroom TV Dramas': [25955], 'Creature Features': [6895], 'Crime Action': [788212], 'Crime Action & Adventure': [9584], 'Crime Comedies': [4058], 'Crime Documentaries': [9875], 'Crime Dramas': [6889], 'Crime Films': [5824], 'Crime Films based on real life': [10185], 'Crime Thrillers': [10499], 'Crime TV Documentaries': [26126], 'Crime TV Dramas': [26009], 'Crime TV Shows': [26146], 'Crime TV Soaps': [37938], 'Critically-acclaimed Action & Adventure': [899], 'Critically-acclaimed Comedies': [9736], 'Critically-acclaimed Dramas': [6206], 'Critically-acclaimed Films': [3979], 'Critically-acclaimed Independent Films': [875], 'Critically-acclaimed Sci-Fi & Fantasy': [5903], 'Cult Comedies': [9434], 'Cult Horror Movies': [10944], 'Cult Movies': [7627], 'Cult Sci-Fi & Fantasy': [4734], 'Cult TV Shows': [74652], 'Dance': [8451], 'Dance & Electronica': [5080], 'Danish Comedies': [59169], 'Danish Crime Movies': [60339], 'Danish Documentaries': [60026], 'Danish Dramas': [59064], 'Danish Films': [58700], 'Danish TV Shows': [77951], 'Dark Comedies': [869], 'Deep Sea Horror Movies': [45028], 'Disco': [3493], 'Disney': [67673], 'Disney Musicals': [59433], 'Documentaries': [6839], 'Dramas': [5763], 'Dramas based on Books': [4961], 'Dramas based on classic literature': [13158], 'Dramas based on contemporary literature': [12994], 'Dramas based on real life': [3653], 'Dutch Children & Family Movies': [89513], 'Dutch Comedies': [79871], 'Dutch Dramas': [9873], 'Dutch Kids TV': [89441], 'Dutch Movies': [10606], 'Dutch TV Shows': [89442], 'Eastern European Movies': [5254], 'Education for Kids': [10659], 'Epics': [52858], 'European Movies': [89708], 'Experimental Movies': [11079], 'Faith & Spirituality': [26835], 'Faith & Spirituality Movies': [52804], 'Family Adventures': [52855], 'Family Animation': [58879], 'Family Comedies': [52847], 'Family Dramas': [31901], 'Family Feature Animation': [51058], 'Family Features': [51056], 'Family Sci-Fi & Fantasy': [52849], 'Fantasy Movies': [9744], 'Female Stand-up Comedy': [77599], 'Film Noir': [7687], 'Finnish Movies': [62285], 'Finnish TV Shows': [78503], 'Food & Travel TV': [72436], 'Food & Wine': [3890], 'Football Movies': [12803], 'Foreign Action & Adventure': [11828], 'Foreign Comedies': [4426], 'Foreign Documentaries': [5161], 'Foreign Dramas': [2150], 'Foreign Gay & Lesbian Movies': [8243], 'Foreign Horror Movies ': [8654], 'Foreign Movies': [7462], 'Foreign Sci-Fi & Fantasy': [6485], 'Foreign Thrillers': [10306], 'French Comedies': [58905], 'French Documentaries': [58710], 'French Dramas': [58677], 'French Movies': [58807], 'French Thrillers': [58798], 'Gangster Movies': [31851], 'Gay & Lesbian Comedies': [7120], 'Gay & Lesbian Documentaries': [4720], 'Gay & Lesbian Dramas': [500], 'Gay & Lesbian Movies': [5977], 'Gay & Lesbian TV Shows': [65263], 'German Comedies': [63115], 'German Dramas': [58755], 'German Movies': [58886], 'German TV Shows': [65198], 'Golden Globe Award-winning Films': [82489], 'Gory Halloween Favorites': [867737], 'Gospel Music': [5096], 'Greek Movies': [61115], 'Halloween Favorites': [108663], 'Halloween Favourites': [108663], 'Hard Rock & Heavy Metal': [9793], 'Heist Films': [27018], 'Historical Documentaries': [5349], 'Historical Dramas': [71591], 'Holiday Favorites': [107985], 'Holiday Fun': [393181], 'Horror Comedy': [89585], 'Horror Movies': [8711], 'Independent Action & Adventure': [11804], 'Independent Comedies': [4195], 'Independent Dramas': [384], 'Independent Movies': [7077], 'Independent Thrillers': [3269], 'Indian Comedies': [9942], 'Indian Dramas': [5051], 'Indian Movies': [10463], 'Inspirational Music': [2222], 'International Action & Adventure': [852490], 'International Comedies': [852492], 'International Documentaries': [852494], 'International Dramas': [852493], 'International Kids TV': [1218090], 'International Movies': [78367], 'International Sci-Fi & Fantasy': [852491], 'International Thrillers': [852488], 'International TV Action & Adventure': [1192487], 'International TV Comedies': [1208951], 'International TV Dramas': [1208954], 'International TV Shows': [1195213], 'Investigative Reality TV': [48785], 'Irish Movies': [58750], 'Italian Comedies': [3300], 'Italian Dramas': [4282], 'Italian Movies': [8221], 'Italian Thrillers': [6867], 'Japanese Academy Award-winning Movies': [1293326], 'Japanese Action & Adventure': [4344], 'Japanese Comedies': [1747], 'Japanese Dramas': [2893], 'Japanese Horror Movies': [10750], 'Japanese Kids TV': [65925], 'Japanese Movies': [10398], 'Japanese Period Dramas': [1402191], 'Japanese Sci-Fi & Fantasy': [6000], 'Japanese Thrillers': [799], 'Japanese TV Comedies': [711366], 'Japanese TV Dramas': [711367], 'Japanese TV Films': [64256], 'Japanese TV Sci-Fi & Fantasy': [1461923], 'Japanese TV Shows': [64256], 'Japanese TV Thrillers': [1138506], 'Jazz & Easy Listening': [10271], 'Kids Anime': [413820], 'Kids Faith & Spirituality': [751423], 'Kids Music': [52843], 'Kids TV for ages 0 to 2': [28233], 'Kids TV for ages 11 to 12': [27950], 'Kids TV for ages 2 to 4': [27480], 'Kids TV for ages 5 to 7': [28034], 'Kids TV for ages 8 to 10': [28083], 'Kids&#39; TV': [27346], 'Korean Action & Adventure': [8248], 'Korean Comedies': [6626], 'Korean Dramas': [1989], 'Korean Movies': [5685], 'Korean Thrillers': [11283], 'Korean TV Dramas': [68699], 'Korean TV Shows': [67879], 'Late Night Comedies': [1402], 'Latin American Comedies': [3996], 'Latin American Documentaries': [15456], 'Latin American Dramas': [6763], 'Latin American Movies': [1613], 'Latin American Music & Musicals': [88635], 'Latin American Police TV Shows': [75408], 'Latin American TV Shows': [67708], 'Latin Music': [10741], 'Latino Stand-up Comedy': [34157], 'Laugh-Out-Loud Comedies': [1333288], 'Martial Arts Movies': [8985], 'Martial Arts, Boxing & Wrestling': [6695], 'Medical TV Dramas': [34204], 'Mexican Comedies': [105], 'Mexican Dramas': [2757], 'Mexican Films': [7825], 'Mexican TV Shows': [67644], 'Middle Eastern Movies': [5875], 'Military & War Action & Adventure': [76501], 'Military & War Documentaries': [77245], 'Military & War Dramas': [76507], 'Military & War Movies': [76510], 'Military Action & Adventure': [2125], 'Military Documentaries': [4006], 'Military Dramas': [11], 'Military TV Shows': [25804], 'Miniseries': [4814], 'Mockumentaries': [26], 'Modern & Alternative Rock': [9090], 'Modern Classic Movies': [76186], 'Monster Movies': [947], 'Movies based on children&#39;s books': [10056], 'Movies for ages 0 to 2': [6796], 'Movies for ages 11 to 12': [6962], 'Movies for ages 2 to 4': [6218], 'Movies for ages 5 to 7': [5455], 'Movies for ages 8 to 10': [561], 'Music': [1701], 'Music & Concert Documentaries': [90361], 'Music & Musicals': [52852], 'Music and Concert Films': [84483], 'Musicals': [13335], 'Mysteries': [9994], 'Nature & Ecology Documentaries': [48768], 'Nature & Ecology TV Documentaries': [49547], 'New Country': [10365], 'New Zealand Movies': [63782], 'Nollywood Movies': [1138254], 'Nordic Children & Family Movies': [78120], 'Nordic Comedies': [78655], 'Nordic Crime Movies': [78208], 'Nordic Dramas': [78628], 'Nordic Thrillers': [78321], 'Nordic TV Shows': [78634], 'Norwegian Comedies': [61132], 'Norwegian Crime Movies': [78463], 'Norwegian Dramas': [62235], 'Norwegian Films': [62510], 'Norwegian Thrillers': [78507], 'Norwegian TV': [78373], 'Period Pieces': [12123], 'Police Action & Adventure': [75418], 'Police Detective Movies': [79049], 'Police Dramas': [75459], 'Police Movies': [75436], 'Police Mysteries': [75415], 'Police Thrillers': [75390], 'Police TV Shows': [75392], 'Political Comedies': [2700], 'Political Documentaries': [7018], 'Political Dramas': [6616], 'Political Thrillers': [10504], 'Political TV Documentaries': [55087], 'Pop': [2145], 'Psychological Thrillers': [5505], 'Punk Rock': [8721], 'Quirky Romance': [36103], 'Rap & Hip-Hop': [6073], 'Reality TV': [9833], 'Reggae': [3081], 'Religious Documentaries': [10005], 'Retro Anime': [1408777], 'Rock & Pop Concerts': [3278], 'Rockumentaries': [4649], 'Romantic Comedies': [5475], 'Romantic Danish Movies': [61656], 'Romantic Dramas': [1255], 'Romantic Favorites': [502675], 'Romantic Films based on a book': [3830], 'Romantic Foreign Movies': [7153], 'Romantic Gay & Lesbian Movies': [3329], 'Romantic Independent Movies': [9916], 'Romantic Japanese Films': [17241], 'Romantic Japanese Movies': [17241], 'Romantic Japanese TV Shows': [1458609], 'Romantic Movies': [8883], 'Romantic Movies based on Books': [3830], 'Romantic Nordic Movies': [78250], 'Romantic Swedish Movies': [60829], 'Romantic TV Programmes': [26156], 'Romantic TV Soaps': [26052], 'Russian': [11567], 'Satanic Stories': [6998], 'Satires': [4922], 'Scandinavian Comedies': [11755], 'Scandinavian Crime Films': [1884], 'Scandinavian Documentaries': [10599], 'Scandinavian Dramas': [2696], 'Scandinavian Independent Movies': [69192], 'Scandinavian Movies': [9292], 'Scandinavian Thrillers': [1321], 'Scandinavian TV': [76802], 'Sci-Fi': [108533], 'Sci-Fi & Fantasy': [1492], 'Sci-Fi Adventure': [6926], 'Sci-Fi Dramas': [3916], 'Sci-Fi Horror Movies': [1694], 'Sci-Fi Thrillers': [11014], 'Science & Nature Documentaries': [2595], 'Science & Nature TV': [52780], 'Science & Technology Documentaries': [49110], 'Science & Technology TV Documentaries': [50232], 'Screwball Comedies': [9702], 'Showbiz Dramas': [5012], 'Showbiz Musicals': [13573], 'Silent Movies': [53310], 'Singer-Songwriters': [5608], 'Sitcoms': [3903], 'Slapstick Comedies': [10256], 'Slasher and Serial Killer Movies': [8646], 'Slice of Life Anime': [1519826], 'Soccer Movies': [12549], 'Soccer Non-fiction': [3215], 'Social & Cultural Documentaries': [3675], 'Social Issue Dramas': [3947], 'Southeast Asian Movies': [9196], 'Spanish Comedies': [61330], 'Spanish Dramas': [58796], 'Spanish Horror Films': [61546], 'Spanish Horror Movies': [61546], 'Spanish Movies': [58741], 'Spanish Thrillers': [65558], 'Spanish-Language TV Shows': [67675], 'Special Interest': [6814], 'Spiritual Documentaries': [2760], 'Sports & Fitness': [9327], 'Sports Comedies': [5286], 'Sports Documentaries': [180], 'Sports Dramas': [7243], 'Sports Movies': [4370], 'Sports TV Programmes': [25788], 'Spy Action & Adventure': [10702], 'Spy Thrillers': [9147], 'Stage Musicals': [55774], 'Stand-up Comedy': [11559], 'Steamy Romance': [29281], 'Steamy Romantic Movies': [35800], 'Steamy Thrillers': [972], 'Supernatural Horror Movies': [42023], 'Supernatural Thrillers': [11140], 'Swedish Comedies': [63092], 'Swedish Crime Movies': [63975], 'Swedish Films': [62016], 'Swedish TV Shows': [76793], 'Talk Shows & Stand-up Comedy': [1516534], 'Tearjerkers': [6384], 'Teen Comedies': [3519], 'Teen Dramas': [9299], 'Teen Romance': [53915], 'Teen Screams': [52147], 'Teen TV Shows': [60951], 'Theatre Arts': [10832], 'Thrillers': [8933], 'Travel & Adventure Documentaries': [1159], 'Travel & Adventure Reality TV': [48762], 'TV Action & Adventure': [10673], 'TV Animated Comedies': [7992], 'TV Cartoons': [11177], 'TV Comedies': [10375], 'TV Comedy Dramas': [7539], 'TV Documentariesa': [10105], 'TV Dramas': [11714], 'TV Horror': [83059], 'TV Mysteries': [4366], 'TV Sci-Fi & Fantasy': [1372], 'TV Shows': [83], 'TV Sketch Comedies': [5610], 'TV Soaps': [10634], 'TV Soaps Featuring a Strong Female Lead': [26105], 'TV Teen Dramas': [52904], 'TV Thrillers': [89811], 'TV Westerns': [11522], 'Urban & Dance Concerts': [9472], 'US Movies': [1159493], 'US Police TV Shows': [75445], 'US TV Comedies': [72407], 'US TV Documentaries': [72384], 'US TV Dramas': [72354], 'US TV Programmes': [72404], 'Vampire Films': [75432], 'Vampire Horror Movies': [75804], 'Vocal Jazz': [5342], 'Vocal Pop': [1800], 'Wacky Comedies': [6197], 'Werewolf Horror Movies': [75930], 'Westerns': [7700], 'Wine & Beverage Appreciation': [1458], 'World Music Concerts': [2856], 'WWII Films': [70023], 'Zombie Horror Movies': [75405], 'Japanese TV Dramas': [711367], 'Japanese TV Shows': [64256], 'Japanese Dramas': [2893]}

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
    #user_prefs = user.preferences
    #user_prefs = crud.get_current_user_preferences(login_user)
   

    if login_user:
        return render_template('profile.html', user=login_user, genres=GENRES, \
            genre_groups=GENRE_GROUPS, languages=LANGUAGES)

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



import json
from flask import Flask, redirect, request, jsonify, session, render_template
import requests
import urllib.parse
import secrets
#import artists
from datetime import datetime
import math

global artists_dict
artists_dict = {
    "SZA" : {
        "genres" : ["contemporary-rnb","jazz","soul","contemporary-pop"],
        "image" : "/static/sza.jpg"
    },
    "Tems" : {
        "genres" : ["afrobeat","contemporary-rnb"],
        "image" : "/static/tems.jpeg"
    }, 
    "Drake" : {
        "genres" : ["contemporary-rnb","contemporary-pop","soul","2000s-hip-hop"],
        "image" : "/static/drake.jpeg"
    }, 
    "Rod Wave": {
        "genres" : ["soul","contemporary-rnb","alt-trap","trap-guitar"],
        "image" : "/static/rod-wave.jpeg"
    },
    "J. Cole" : {
        "genres" : ["soul","introspective","jazz"],
        "image" : "/static/j-cole.jpeg"
    },
    "Brent Faiyaz" : {
        "genres" : ["contemporary-rnb","soul","jersey-club"],
        "image" : "/static/brent.jpeg"
    },
    "Michael Jackson" : {
        "genres" : ["classic-pop","soul","jazz","20th-century-rnb"],
        "image" : "/static/michael-jackson.jpeg"
    },
    "Beyonce" : {
        "genres" : ["classic-pop","soul","jazz","2000s-rnb"],
        "image" : "/static/beyonce.jpeg"
    },
    "Lil Yatchy" : {
        "genres" : ["alt-trap","contemporary-pop","melodic-trap","introspective"],
        "image" : "/static/lil-yatchy.jpeg"
    }, 
    "BabyTron" : {
        "genres" : ["alt-trap","introspective"],
        "image" : "/static/baby-tron.jpeg"
    }, 
    "Future" : {
        "genres" : ["trap"],
        "image" : "/static/future.jpeg"
    }, 
    "21 Savage" : {
        "genres" : ["trap"],
        "image" : "/static/21-savage.jpeg"
    }, 
    "Kanye West" : {
        "genres" : ["jazz","soul","introspective","2000s-hip-hop"],
        "image" : "/static/kanye.jpeg"
    }, 
    "Autumn!" : {
        "genres" : ["pluggnb","alt-trap","trap","psychedelic"],
        "image" : "/static/autumn.jpeg"
    },
    "Summrs" : {
        "genres" : ["pluggnb","alt-trap","trap","psychedelic"],
        "image" : "/static/summrs.jpg"
    }, 
    "Yeat" : {
        "genres" : ["alt-trap","trap","psychedelic"],
        "image" : ""
    }, 
    "LUCKI" : {
        "genres" : ["alt-trap","trap","psychedelic"],
        "image" : ""
    }, 
    "Juice WRLD" : {
        "genres" : ["alt-trap","melodic-trap","trap","psychedelic"],
        "image" : ""
    }, 
    "Lil Uzi Vert" : {
        "genres" : ["alt-trap","melodic-trap","trap","psychedelic","contemporary-pop"],
        "image" : ""
    }, 
    "Whitney Houston" : {
        "genres" : ["soul","classic-pop","20th-century-rnb"],
        "image" : ""
    }, 
    "Alicia Keys" : {
        "genres" : ["soul","classic-pop","2000s-rnb"],
        "image" : ""
    }, 
    "Mary J Blige" : {
        "genres" : ["2000s-rnb","2000s-hip-hop","soul","classic-pop"],
        "image" : ""
    },
    "USHER" : {
        "genres" : ["2000s-rnb","2000s-hip-hop","soul","contemporary-pop"],
        "image" : ""
    }, 
    "Prince" : {
        "genres" : ["classic-pop","soul","jazz","20th-century-rnb","classic-rock"],
        "image" : ""
    }, 
    "The Weeknd" : {
        "genres" : ["contemporary-pop","contemporary-rnb"],
        "image" : ""
    }, 
    "Childish Gambino" : {
        "genres" : ["soul","contemporary-pop","jazz"],
        "image" : ""
    }, 
    "Gunna" : {
        "genres" : ["trap"],
        "image" : ""
    }, 
    "Young Thug" : {
        "genres" : ["trap"],
        "image" : ""
    },
    "Tyler, The Creator" : {
        "genres" : ["trap","alt-trap","contemporary-pop","melodic-trap"],
        "image" : ""
    }, 
    "Lil Tecca" : {
        "genres" : ["trap","melodic-trap","contemporary-pop"],
        "image" : ""
    }, 
    "Playboi Carti" : {
        "genres" : ["trap","melodic-trap","opium","alt-trap"],
        "image" : ""
    }, 
    "Ken Carson" : {
        "genres" : ["trap","alt-trap","opium"],
        "image" : ""
    }, 
    "Destroy Lonely" : {
        "genres" : ["trap","alt-trap","opium"],
        "image" : ""
    }, 
    "KANKAN" : {
        "genres" : ["pluggnb","alt-trap","psychedelic"],
        "image" : ""
    }, 
    "Travis Scott" : {
        "genres" : ["trap","lofi"],
        "image" : ""
    }, 
    "Kendrick Lamar" : {
        "genres" : ["introspective","soul"],
        "image" : ""
    },
    "JID" : {
        "genres" : ["trap","soul","introspective"],
        "image" : ""
    }, 
    "Ariana Grande" : {
        "genres" : ["contemporary-pop","contemporary-rnb"],
        "image" : ""
    }, 
    "Olivia Rodrigo" : {
        "genres" : ["contemporary-pop"],
        "image" : ""
    }, 
    "PinkPanthress" : {
        "genres" : ["contemporary-pop","jersey-club"],
        "image" : ""
    }, 
    "Ice Spice" : {
        "genres" : ["contemporary-pop","drill","jersey-club"],
        "image" : ""
    }, 
    "Wu-Tang Clan" : {
        "genres" : ["introspective","soul","jazz"],
        "image" : ""
    }, 
    "Nujabes" : {
        "genres" : ["introspective","soul","jazz","lofi"],
        "image" : ""
    }, 
    "Nas" : {
        "genres" : ["introspective","soul","jazz"],
        "image" : ""
    }, 
    "MF DOOM" : {
        "genres" : ["introspective","soul","jazz","2000s-hip-hop"],
        "image" : ""
    },
    "Tupac" : {
        "genres" : ["introspective","soul"],
        "image" : ""
    }, 
    "N.W.A" : {
        "genres" : ["metal"],
        "image" : ""
    }, 
    "Ice Cube" : {
        "genres" : ["introspective","soul","2000s-hip-hop"],
        "image" : ""
    }, 
    "The Notorious B.I.G" : {
        "genres" : ["introspective","soul"],
        "image" : ""
    }, 
    "Lil Baby" : {
        "genres" : ["trap"],
        "image" : ""
    }, 
    "Giveon" : {
        "genres" : ["jazz","soul","contemporary-rnb"],
        "image" : ""
    }, 
    "Tay-K" : {
        "genres" : ["trap"],
        "image" : ""
    }, 
    "XXXTentacion" : {
        "genres" : ["metal","classic-rock","grunge","trap-guitar","trap","alt-trap","melodic-trap"],
        "image" : ""
    }, 
    "Jay-Z" : {
        "genres" : ["introspective","jazz","soul"],
        "image" : ""
    }, 
    "Daniel Caesar" : {
        "genres" : ["contemporary-rnb","contemporary-pop","soul","classic-rock"],
        "image" : ""
    }, 
    "Boogie Wit Da Hoodie" : {
        "genres" : ["contemporary-rnb","trap-gutiar","trap"],
        "image" : ""
    }, 
    "Nirvana" : {
        "genres" : ["grunge"],
        "image" : ""
    }, 
    "Queen" : {
        "genres" : ["classic-pop","metal","classic-rock"],
        "image" : ""
    }, 
    "Burna Boy" : {
        "genres" : ["afrobeat","contemporary-rnb"],
        "image" : ""
    }, 
    "Rema" : {
        "genres" : ["afrobeat","contemporary-rnb","contemporary-pop"],
        "image" : ""
    }, 
    "J Hus" : {
        "genres" : ["afrobeat","contemporary-rnb"],
        "image" : ""
    }, 
    "Central Cee" : {
        "genres" : ["drill"],
        "image" : ""
    }, 
    "Dave" : {
        "genres" : ["drill","introspective","afrobeat"],
        "image" : ""
    }, 
    "Kodak Black" : {
        "genres" : ["trap"],
        "image" : ""
    }, 
    "Polo G" : {
        "genres" : ["trap","melodic-trap","trap-guitar"],
        "image" : ""
    }, 
    "Frank Ocean" : {
        "genres" : ["contemporary-rnb","contemporary-pop","soul"],
        "image" : ""
    }, 
    "keshi" : {
        "genres" : ["contemporary-rnb","lofi"],
        "image" : ""
    }, 
    "Rihana" : {
        "genres" : ["contemporary-rnb","classic-pop"],
        "image" : ""
    }, 
    "DEAN" : {
        "genres" : ["k-pop","contemporary-rnb"],
        "image" : ""
    }, 
    "NewJeans" : {
        "genres" : ["k-pop","contemporary-pop","jersey-club"],
        "image" : ""
    }, 
    "LE SSERAFIM" : {
        "genres" : ["k-pop","contemporary-pop"],
        "image" : ""
    }, 
    "TWICE" : {
        "genres" : ["k-pop","contemporary-pop","contemporary-rnb"],
        "image" : ""
    }, 
    "BTS" : {
        "genres" : ["k-pop","contemporary-pop"],
        "image" : ""
    }, 
    "Jung Kook" : {
        "genres" : ["k-pop","contemporary-pop"],
        "image" : ""
    }, 
    "Tee Grizzley" : {
        "genres" : ["trap","introspective","drill"],
        "image" : ""
    }, 
    "Ms. Lauryn Hill" : {
        "genres" : ["soul","introspective","20th-century-rnb"],
        "image" : ""
    }, 
    "Cochise" : {
        "genres" : ["alt-trap","trap","contemporary-pop"],
        "image" : ""
    }, 
    "Sleepy Hallow" : {
        "genres" : ["trap-guitar","drill","lofi"],
        "image" : ""
    }, 
    "Sheff G" : {
        "genres" : ["drill"],
        "image" : ""
    }, 
    "Kyle Richh" : {
        "genres" : ["drill","jersey-club"],
        "image" : ""
    }, 
    "Chief Keef" : {
        "genres" : ["drill","trap"],
        "image" : ""
    }, 
    "redveil" : {
        "genres" : ["jazz","soul","introspective","trap"],
        "image" : ""
    }, 
    "Destiny's Child" : {
        "genres" : [""],
        "image" : ""
    }, 
    "Bandmanrill" : {
        "genres" : ["jersey-club","drill"],
        "image" : ""
    }, 
    "Fivio Foreign" : {
        "genres" : ["drill","soul"],
        "image" : ""
    }, 
    "NBA Young Boy" : {
        "genres" : ["drill","trap"],
        "image" : ""
    }, 
    "Sha Gz" : {
        "genres" : ["drill","jersey-club"],
        "image" : ""
    }, 
    "Kay Flock" : {
        "genres" : ["drill"],
        "image" : ""
    }, 
    "2Rare" : {
        "genres" : ["jersey-club"],
        "image" : ""
    }, 
    "King Von" : {
        "genres" : ["drill"],
        "image" : ""
    }, 
    "Draft Day" : {
        "genres" : ["alt-trap","introspective","trap"],
        "image" : ""
    }, 
    "Tyla" : {
        "genres" : ["contemporary-pop","afrobeat"],
        "image" : ""
    }, 
    "Arya Starr" : {
        "genres" : ["contemporary-pop","afrobeat","contemporary-rnb"],
        "image" : ""
    }, 
}

class ArtistList:
    def __init__(self,genres,songs):
        self.genres = genres
        self.artists_displayed = {}
        artists_list = []
        for key in artists_dict:
            curr = Artist(key,self.genres)
            if curr.total_intersections >= 1 and len(artists_list) < songs:
                artists_list.append(curr)
        artists_list = sorted(artists_list, key = lambda Artist : Artist.total_intersections)
        artists_list.reverse()
        for i in artists_list:
            name = i.artist
            self.artists_displayed[name] = artists_dict[name]
    def getArtists(self):
        return self.artists_displayed
        

class Artist:
    def __init__(self,artist_name,genres):
        self.artist = artist_name
        self.genres = genres
        self.total_intersections = 0
        for i in artists_dict[self.artist]["genres"]:
            if i in self.genres:
                self.total_intersections += 1
        
        

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

login_uri = "/login"
client_id = '97f702fed6bf4a5fa68256d7d35e8b1e'
client_secret = '6169db01ba0d407a82c2b3c4125b68fb'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
api_base_url = 'https://api.spotify.com/v1/'

global name_of_playlist
name_of_playlist = ""
global num_of_songs_in_playlist
num_of_songs_in_playlist = 0
playlist_description = ""
global artists_selected
artists_selected = []

@app.route('/')
def home():
   return render_template("index.html")

@app.route('/genres', methods=["GET","POST"])
def display_genres_page():
    first_form = request.form
    number = first_form["num-of-songs"]
    global num_of_songs_in_playlist
    num_of_songs_in_playlist = int(number)
    global name_of_playlist
    name_of_playlist = first_form["name-of-playlist"]
    return render_template("genres.html", number=number, nameOfPlaylist=name_of_playlist)

@app.route('/artists', methods=["GET","POST"])
def display_artists_page():
    genres_json = request.form
    genres = []
    for key in genres_json:
        genres.append(genres_json[key])
    curr = ArtistList(genres,num_of_songs_in_playlist)
    artists_displayed = curr.getArtists()
    return render_template("artists.html",artists_data=artists_displayed)

@app.route('/temp',methods=["GET","POST"])
def display_artists_data():
    artists_data = request.form
    for key in artists_data:
        artists_selected.append(artists_data[key])
    return redirect('/login')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-modify-public'

    params = {
        'client_id' : client_id,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True 
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(
            token_url,
            data=req_body
        )
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.utcnow().timestamp() + token_info['expires_in']

        return redirect('/playlists')
    
@app.route('/playlists')
def create_playlist():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.utcnow().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    global remainder
    remainder = num_of_songs_in_playlist % len(artists_selected)
    track_ids = []

    for i in artists_selected:
        response = requests.get(api_base_url + 'search?q=' + i + '&type=artist', headers=headers)
        json_resp = response.json()
        artist_id = json_resp["artists"]["items"][0]["id"]
        responseTwo = requests.get(
            api_base_url + 'artists/' + artist_id + '/top-tracks?market=ES',
            headers=headers
        )
        json_resp_two = responseTwo.json()
        artist_songs = songs_per_artsit()
        if artist_songs > len(json_resp_two["tracks"]):
            for j in range(len(json_resp_two["tracks"])):
                track_name = json_resp_two["tracks"][j]["name"]
                track_id = json_resp_two["tracks"][j]["uri"]
                track_ids.append(track_id)
        elif artist_songs < len(json_resp_two["tracks"]):
            for j in range(int(artist_songs)):
                track_name = json_resp_two["tracks"][j]["name"]
                track_id = json_resp_two["tracks"][j]["uri"]
                track_ids.append(track_id)
        else:
            for j in range(int(artist_songs)):
                track_name = json_resp_two["tracks"][j]["name"]
                track_id = json_resp_two["tracks"][j]["uri"]
                track_ids.append(track_id)
    headers_two = {
        'Authorization': f"Bearer {session['access_token']}",
        'Content-Type': 'application/json'
    }
    
    playlist_creation_url = api_base_url + "me/playlists"
    playlist_data = {
        'name' : name_of_playlist,
        'description' : playlist_description
    }
    playlist_created = requests.post(url=playlist_creation_url,headers=headers_two,data=json.dumps(playlist_data))
    temp = playlist_created.json()
    new_playlist_id = temp["id"]
    add_tracks_url = f"{api_base_url}playlists/{new_playlist_id}/tracks"
    track_data = json.dumps({
        'uris' : track_ids
    })
    tracks_added = requests.post(url=add_tracks_url,headers=headers_two,data=track_data)
    tracks_added.raise_for_status()
    return render_template("temp.html",name=name_of_playlist)

def songs_per_artsit():
    global remainder
    songs_for_artist = 0
    if num_of_songs_in_playlist % len(artists_selected) != 0 :
        songs_for_artist  = math.floor(num_of_songs_in_playlist / len(artists_selected))
        if remainder > 0:
            songs_for_artist += 1
            remainder -=1
    else:
        songs_for_artist = num_of_songs_in_playlist / len(artists_selected)
    return songs_for_artist

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.utcnow().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(token_url, data = req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.utcnow().timestamp() + new_token_info['expires_in']

        return redirect('/playlists')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

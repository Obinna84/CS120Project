
import json
from flask import Flask, redirect, request, jsonify, session, render_template
import requests
import urllib.parse
import secrets
#import artists
from datetime import datetime
import math
"""
CS Project Idea (Backup: Playlist creator):
- User selects genre (Prompt with artists in genre)
- Have them select from a few
- compile playlist of songs based on the responses


Decisions:
- Display 2 artists at a time they choose against
- Or display list of artists and have them select a couple from it *

To Think About:
- Do we have a premade list of artists from each genre

python3 project.py

- Is our goal to compile a playlist of artists they already like or playlist of artists that make similar music (expose them to underground shit)

Brainstorm:
- **Scratch game
- palindrome, roman numeral converter
- buzzfeed quiz
- alarm clock
- interactive dice roller
- notes and task manager
- Crime rate predictor
- mass shooting tracker
- mp3 player
- resume organizer
"""

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

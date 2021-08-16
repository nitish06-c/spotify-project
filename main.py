import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id='/',
                              client_secret='/',
                              redirect_uri='/',
                              scope="user-top-read"))

results = sp.current_user_top_tracks()
top_tracks_short = sp.current_user_top_tracks(limit=10, offset=0,
                                              time_range="short_term")


def track_id(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids


track_ids = track_id(top_tracks_short)


def track_features(id):
    meta = sp.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info


def convert_to_df(track_ids):
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = track_features(track_ids[i])
        tracks.append(track)

    df = pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'spotify_url',
                                       'album_cover'])
    df.to_csv(f'{time_period}.csv')


time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0,
                                            time_range=time_period)
    track_ids = track_id(top_tracks)
    convert_to_df(track_ids)

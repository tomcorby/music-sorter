#!/usr/bin/env python3

import re
import spotipy
import statistics
import requests

from spotipy.oauth2 import SpotifyClientCredentials
from classes import Strings
from models import Track, Album

# temp
import dotenv
import os
dotenv.load_dotenv()

# @todo make other APIs to check tracks

class Discogs:
    def search(artist, track, album):
        params = {'token': os.getenv('DISCOGS_TOKEN'), 'artist': artist, 'track': track, 'release_title': album}

        results = requests.get('https://api.discogs.com/database/search', params).json()

        for i, result in enumerate(results['results']):
            print(result)

        return False


class Spotify:
    def __init__(self, args):
        self.args = args
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def playlist_uris_from_user(self, user):
        playlists = self.sp.user_playlists(user)
        uris = []

        while playlists:
            for i, playlist in enumerate(playlists['items']):
                print(playlist['uri'])
                uris.append(playlist['uri'])
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None

        return uris

    def search_track(self, track, artist='', album=''):
        if artist:
            results = self.sp.search(q=artist + ' ' + track, type='track')
        else:
            results = self.sp.search(q=track, type='track')

        if len(results['tracks']['items']):
            for i, result in enumerate(results['tracks']['items']):
                total_matches = []

                # @todo: move all the mean_match stuff to another method where you just pass as many args as you want and their matches
                result['track_match'] = Strings.fuzzy_match(result['name'], track)
                total_matches.append(result['track_match'])
                # track without features etc
                total_matches.append(Strings.fuzzy_match(re.sub(r'\([^)]*\)', '', result['name']), track))

                if album:
                    result['album']['album_match'] = Strings.fuzzy_match(result['album']['name'], album)
                    total_matches.append(result['album']['album_match'])

                if artist:
                    if album:
                        for album_artist in result['album']['artists']:
                            album_artist['album_artist_match'] = Strings.fuzzy_match(album_artist['name'], artist)
                            total_matches.append(album_artist['album_artist_match'])

                    for track_artist in result['artists']:
                        track_artist['track_artist'] = Strings.fuzzy_match(track_artist['name'], artist)
                        total_matches.append(track_artist['track_artist'])

                mean_match = statistics.mean(total_matches)

                if mean_match >= 50:
                    return Track.create()

        return False

    def search_album(self, album, artist='', tracks=[]):
        results = self.sp.search(q=album + ' ' + artist, type='album')

        if len(results['albums']['items']):
            for result in results['albums']['items']:
                total_matches = []

                result['album_match'] = Strings.fuzzy_match(result['name'], album)
                total_matches.append(result['album_match'])

                if artist:
                    for album_artist in result['artists']:
                        album_artist['album_artist_match'] = Strings.fuzzy_match(album_artist['name'], artist)
                        total_matches.append(album_artist['album_artist_match'])

                mean_match = statistics.mean(total_matches)

                if mean_match >= 50:
                    # @todo: return actual Album class
                    return album

        return False

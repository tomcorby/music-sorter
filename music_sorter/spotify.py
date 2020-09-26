#!/usr/bin/python3

import common
import re
import spotipy
import statistics

from spotipy.oauth2 import SpotifyClientCredentials

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


    def searchTrack(self, track, artist = '', album = ''):
        if (artist):
            results = self.sp.search(q=artist + ' ' + track, type='track')
        else:
            results = self.sp.search(q=track, type='track')

        if (len(results['tracks']['items'])):
            for i, result in enumerate(results['tracks']['items']):
                totalMatches = []

                result['trackMatch'] = common.fuzzy_match_strings(result['name'], track)
                totalMatches.append(result['trackMatch'])
                totalMatches.append(common.fuzzy_match_strings(re.sub(r'\([^)]*\)', '', result['name']), track)) # track without features etc

                if (album):
                    result['album']['albumMatch'] = common.fuzzy_match_strings(result['album']['name'], album)
                    totalMatches.append(result['album']['albumMatch'])

                if (artist):
                    if (album):
                        for albumArtist in result['album']['artists']:
                            albumArtist['albumArtistMatch'] = common.fuzzy_match_strings(albumArtist['name'], artist)
                            totalMatches.append(albumArtist['albumArtistMatch'])

                    for trackArtist in result['artists']:
                        trackArtist['trackArtist'] = common.fuzzy_match_strings(trackArtist['name'], artist)
                        totalMatches.append(trackArtist['trackArtist'])


                meanMatch = statistics.mean(totalMatches)

                print(meanMatch)
                print(result)

                if (meanMatch >= 50):
                    # @todo: return actual Track class
                    return result

        return False


    def searchAlbum(self, album, artist = '', tracks = []):
        results = self.sp.search(q=album + ' ' + artist, type='album')

        if (len(results['albums']['items'])):
            for result in results['albums']['items']:
                totalMatches = []

                result['albumMatch'] = common.fuzzy_match_strings(result['name'], album)
                totalMatches.append(result['albumMatch'])

                if (artist):
                    for albumArtist in result['artists']:
                        albumArtist['albumArtistMatch'] = common.fuzzy_match_strings(albumArtist['name'], artist)
                        totalMatches.append(albumArtist['albumArtistMatch'])


                meanMatch = statistics.mean(totalMatches)

                if (meanMatch >= 50):
                    # @todo: return actual Album class
                    return album

        return False
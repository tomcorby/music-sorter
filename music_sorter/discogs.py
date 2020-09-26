#!/usr/bin/python3

import requests
# temp
import dotenv
import os
dotenv.load_dotenv()


def search(artist, track, album):
    params = {'token': os.getenv('DISCOGS_TOKEN'), 'artist': artist, 'track': track, 'release_title': album}

    results = requests.get('https://api.discogs.com/database/search', params).json()

    for i, result in enumerate(results['results']):
        print(result)

    return False


search('Eminem', 'The Real Slim Shady', '')
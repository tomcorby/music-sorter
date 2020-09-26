#!/usr/bin/python3

# temp
import dotenv
import os
dotenv.load_dotenv()

import requests

def search(artist, track, album):
    params = {'token': os.getenv('DISCOGS_TOKEN'), 'artist': artist, 'track': track, 'release_title': album}

    results = requests.get('https://api.discogs.com/database/search', params).json()

    for i, result in enumerate(results['results']):


    return False


search('Eminem', 'The Real Slim Shady', '')
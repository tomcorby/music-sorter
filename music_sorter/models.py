#!/usr/bin/python3

import datetime

from peewee import *


class Database:
    db = SqliteDatabase('music-sorter.db')


class BaseModel(Model):
    class Meta:
        database = Database.db


class UnsortedMusic(BaseModel):
    path = TextField()
    date_added = DateTimeField(default=datetime.datetime.now)


class SortedMusic(BaseModel):
    path = TextField()
    format = TextField()
    date_added = DateTimeField()
    date_sorted = DateTimeField(default=datetime.datetime.now)


class Album(BaseModel):
    title = TextField()
    artist = TextField()
    album = TextField()
    year = TextField()
    genre = TextField()
    compilation = BooleanField()
    spotify_playlist = TextField()
#     tracks
#     artists
    spotify_uri = TextField()
    release_date = DateTimeField()
    date_added = DateTimeField(default=datetime.datetime.now)


class Artist(BaseModel):
    name = TextField()
#     albums
    spotify_uri = TextField()
    date_added = DateTimeField(default=datetime.datetime.now)


class Track(BaseModel):
    title = TextField()
    artist = TextField()
    album = TextField()
    year = TextField()
    genre = TextField()
    compilation = BooleanField()
    spotify_playlist = TextField()
    play_counter = IntegerField()
    beats_per_minute = DecimalField()
#     artists
#     album
    genre = TextField()
    spotify_uri = TextField()
    date_added = DateTimeField(default=datetime.datetime.now)

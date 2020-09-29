#!/usr/bin/env python3

import datetime

from peewee import *

db = SqliteDatabase('music-sorter.db')


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class UnsortedMusic(BaseModel):
    path = TextField(unique=True)
    date_added = DateTimeField(default=datetime.datetime.now)


class Album(BaseModel):
    title = TextField(index=True)
    artist = TextField(index=True)
    album = TextField(null=True)
    release_date = DateField()
    genre = TextField()
    compilation = BooleanField()
    spotify_playlist = TextField()
    path = TextField(unique=True)
    spotify_uri = TextField(null=True, index=True, unique=True)
    date_added = DateTimeField(default=datetime.datetime.now)


class Artist(BaseModel):
    name = TextField(index=True)
    spotify_uri = TextField(null=True, index=True, unique=True)
    date_added = DateTimeField(default=datetime.datetime.now)


class Track(BaseModel):
    title = TextField(index=True)
    artist = TextField(index=True)
    album = TextField(null=True)
    release_date = DateField()
    genre = TextField()
    compilation = BooleanField()
    spotify_playlist = TextField()
    play_counter = IntegerField()
    beats_per_minute = DecimalField()
    spotify_uri = TextField(null=True, index=True, unique=True)
    path = TextField(unique=True)
    date_added = DateTimeField(default=datetime.datetime.now)


class AlbumTracks(BaseModel):
    album_id = ForeignKeyField(Album)
    track_id = ForeignKeyField(Track)


class AlbumArtists(BaseModel):
    album_id = ForeignKeyField(Album)
    artist_id = ForeignKeyField(Artist)


class TrackArtists(BaseModel):
    track_id = ForeignKeyField(Track)
    artist_id = ForeignKeyField(Artist)
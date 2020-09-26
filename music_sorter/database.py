#!/usr/bin/python3

import os
import sys
import sqlite3
from peewee import *


class Database:
    def __init__(self, args):
        self.args = args
        self.connection = sqlite3.connect('music-sorter.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Make sure tables exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS unsortedMusic
                            (id INTEGER PRIMARY KEY, path TEXT UNIQUE, dateAdded DATE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sortedMusic
                            (id INTEGER PRIMARY KEY, path TEXT UNIQUE, extension TEXT, dateAdded DATE)''')

    def insert_unsorted_music(self, unsorted_music):
        self.cursor.execute('select count(*) from unsortedMusic')
        pre_count = self.cursor.fetchone()

        self.cursor.executemany('INSERT OR IGNORE INTO unsortedMusic (path, dateAdded) VALUES (?, datetime())',
                                unsorted_music)

        self.cursor.execute('select count(*) from unsortedMusic')
        post_count = self.cursor.fetchone()

        return post_count[0]-pre_count[0]

    def move_unsorted_to_sorted_db(self, old_path, new_path, extension):
        self.cursor.execute('INSERT OR IGNORE INTO sortedMusic (path, extension, dateAdded) VALUES (?, ?, datetime())', (
            new_path, extension
        ))
        self.cursor.execute('DELETE FROM unsortedMusic WHERE path = ?', [old_path])

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()
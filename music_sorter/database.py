#!/usr/bin/python3

import os
import sys
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
                            (id INTEGER PRIMARY KEY, path TEXT UNIQUE, format TEXT, dateAdded DATE)''')


    def insert_unsorted_music(self, unsortedMusic):
        self.cursor.execute('select count(*) from unsortedMusic')
        preCount = self.cursor.fetchone()

        self.cursor.executemany('INSERT OR IGNORE INTO unsortedMusic (path, dateAdded) VALUES (?, datetime())', unsortedMusic)

        self.cursor.execute('select count(*) from unsortedMusic')
        postCount = self.cursor.fetchone()

        return postCount[0]-preCount[0]


    def move_unsorted_to_sorted_db(self, oldPath, newPath, format):
        self.cursor.execute('INSERT OR IGNORE INTO sortedMusic (path, format, dateAdded) VALUES (?, ?, datetime())', (newPath, format))
        self.cursor.execute('DELETE FROM unsortedMusic WHERE path = ?', [oldPath])


    def commit(self):
        self.connection.commit()


    def close(self):
        self.connection.close()


    def __del__(self):
        self.close()
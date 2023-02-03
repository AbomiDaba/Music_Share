from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re

class Song:
    def __init__(self, data):
        self.id = data['id']
        self.artist = data['artist']
        self.name = data['name']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.likers = []

    @classmethod
    def get_one_song(cls, data):
        query = 'SELECT * FROM songs WHERE songs.id = %(id)s'
        result = connectToMySQL('railway').query_db(query, data)
        song = cls(result[0])
        return song

    @classmethod
    def get_songs_with_users_and_likers(cls):
        query = 'SELECT * FROM songs JOIN users ON songs.user_id = users.id LEFT JOIN likes ON songs.id = likes.song_id LEFT JOIN users as likers ON likers.id = likes.FK_likes_users ORDER BY songs.created_at DESC'
        results = connectToMySQL('railway').query_db(query)
        print(results)
        songs = []
        for row in results:
            new_song = True
            user_2_data = {
                'id' : row['likers.id'],
                'first_name' : row['likers.first_name'],
                'last_name' : row['likers.last_name'],
                'email' : row['likers.email'],
                'password' : row['likers.password'],
                'created_at' : row['likers.created_at'],
                'updated_at' : row['likers.updated_at']
            }
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            print(f"current row id: {row['id']}")
            if songs:
                print(f"previous song id: {songs[len(songs) - 1].id}")
                print(f"song_list length: {len(songs)}")
            if len(songs) > 0 and songs[len(songs) - 1].id == row['id']:
                songs[len(songs) - 1].likers.append(user.User(user_2_data))
                new_song = False


            if new_song:
                s = cls(row)
                s.user = user.User(user_data)
                if row['likers.id'] is not None:
                    s.likers.append(user.User(user_2_data))
                songs.append(s)
        return songs

    @classmethod
    def get_liked_songs(cls, data):
        query = 'SELECT song_id FROM likes JOIN users on likes.user_id = users.id WHERE users.id = %(id)s'
        results = connectToMySQL('railway').query_db(query, data)
        liked_songs = []
        if results != False:
            for row in results:
                liked_songs.append(row['song_id'])
        print(print(liked_songs))
        return liked_songs


    @classmethod
    def create_song(cls, data):
        query ='INSERT INTO songs (artist, name, genre, created_at, updated_at, user_id) VALUES(%(artist)s, %(name)s, %(genre)s, NOW(), NOW(), %(user_id)s)'
        song = connectToMySQL('railway').query_db(query, data)
        return song

    @classmethod
    def create_like(cls, data):
        query ='INSERT INTO likes (song_id, FK_likes_users) VALUES(%(song_id)s, %(FK_likes_users)s)'
        like = connectToMySQL('railway').query_db(query, data)
        return like

    @classmethod
    def destroy_like(cls, data):
        query = 'DELETE FROM likes WHERE likes.song_id = %(song_id)s and likes.FK_likes_users =  %(FK_likers_users)s'
        delete = connectToMySQL('railway').query_db(query, data)
        return delete

    @classmethod
    def edit_song(cls, data):
        query = 'UPDATE songs SET artist = %(artist)s, name = %(name)s, genre = %(genre)s WHERE songs.id = %(id)s'
        edit = connectToMySQL('railway').query_db(query, data)
        return edit

    @classmethod
    def destroy_song(cls, data):
        query = 'DELETE FROM songs WHERE songs.id = %(id)s'
        delete = connectToMySQL('railway').query_db(query, data)
        return delete


    @staticmethod
    def validate_songs(data):
        is_valid = True
        if len(data['artist']) < 1:
            flash('Enter Artist', 'song')
            is_valid = False

        if len(data['name']) < 1:
            flash('Enter Song name', 'song')
            is_valid = False

        if len(data['genre']) < 3:
            flash('Enter Genre', 'song')
            is_valid = False
        return is_valid
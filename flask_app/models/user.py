from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import song

import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.songs = []

    def get_all(cls):
        connection = connectToMySQL('solo_project')
        query = 'select * from users'
        results = connection.query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def save(cls, data):
        connection = connectToMySQL('solo_project')
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connection.query_db( query, data )

    @classmethod
    def get_one(cls, data):
        connection = connectToMySQL('solo_project')
        query = 'select * from users where id = %(id)s'
        result = connection.query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_with_songs(cls):
        connection = connectToMySQL('solo_project')
        query = 'SELECT * FROM users JOIN songs ON users.id = songs.user_id'
        result = connection.query_db(query)
        users = []
        for row in result:
            # new_user = True
            data = {
                'id' : row['songs.id'],
                'artist' : row['artist'],
                'name' : row['name'],
                'genre' : row['genre'],
                'created_at' : row['songs.created_at'],
                'updated_at' : row['songs.updated_at'],
                'user_id' : row['user_id'],
                'user' : None
            }
            # if len(users) > 0 and users[len(users) -1].id == row['id']:
            #     users[len(users) -1].songs.append(song.Song(data))
            #     new_user = False
            # if new_user:
            user = cls(row)
            user.songs.append(song.Song(data))
            users.append(user)
            print(users)
        return users
    @classmethod
    def update(cls, data):
        connection = connectToMySQL('solo_project')
        query = 'update users set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, where id = %(id)s'
        return connection.query_db(query,data)

    @classmethod
    def destroy(cls, data):
        connection = connectToMySQL('solo_project')
        query = 'delete from users where id = %(id)s'
        return connection.query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users where email = %(email)s'
        result = connectToMySQL('solo_project').query_db(query, data)
        if result != False:
            if len(result) < 1:
                return False
            else:
                return cls(result[0])

    @staticmethod
    def validate_user(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name']) < 3:
            flash('First Name must be at least 3 characters', 'register')
            is_valid = False

        if len(data['last_name']) < 3:
            flash('Last Name must be at least 3 characters', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False

        query = 'SELECT * FROM users where email = %(email)s'
        result = connectToMySQL('solo_project').query_db(query, data)
        if len(result) >= 1:
            flash('Email alreaedy in use', 'register')
            is_valid = False

        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid= False

        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'register')
            is_valid = False

        return is_valid
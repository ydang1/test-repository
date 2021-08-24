
import sqlite3
from db import db

class  UserModel(db.Model):

    # create table and get the table columns

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(80))

    password = db.Column(db.String(80))


    def __init__(self, username, password):

        self.username = username

        self.password = password


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):

        return cls.query.filter_by(username = username).first()
        # return cls.query.filter_by(name = name).first() # SELECT * FROM items WHERE name = name
        

        # connection = sqlite3.connect('data.db')

        # cursor = connection.cursor()


        # query = "SELECT * FROM users WHERE username=?"

        # result = cursor.execute(query, (username,)) # (5 + 3) * 8

        # row = result.fetchone()

        # if row:
        #     user = cls(*row)

        # else:

        #     user = None

        # connection.close()

        # return user


    
    @classmethod
    def find_by_id(cls, _id):

        return cls.query.filter_by(id = _id).first()

        # connection = sqlite3.connect('data.db')

        # cursor = connection.cursor()


        # query = "SELECT * FROM users WHERE id=?"

        # result = cursor.execute(query, (_id,)) # (5 + 3) * 8

        # row = result.fetchone()

        # if row:
        #     user = cls(*row)

        # else:

        #     user = None

        # connection.close()

        # return user
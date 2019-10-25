import datetime
import uuid

from flask import session

from src.common.database import Database
from src.models.blog import Blog

__author__ = 'chansen'


class User(object):
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_username(cls, username):
        """
            Search database for account attached to given username

        :param username:    username to search by
        :return:            User Object instance w/ data attached to username
        """
        data = Database.find_one('users', {'username': username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        """
            Search database for account attached to given email address

            :param email:   email address to search by
            :return:        User Object instance w/ data attached to email
        """
        data = Database.find_one('users', {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        """
            Search database for account attached to given ID

            :param _id:   id to search by
            :return:      User Object instance w/ data attached to _id
        """
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(username, password):
        """
            Check password matches User account attached to email given


            :param username:    email to create account with
            :param password:    password to verify
            :return:            True/False if email and password are confirmed
        """
        user = User.get_by_username(username)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @staticmethod
    def login_email_valid(email, password):
        """
            Check password matches User account attached to email given


            :param email:       email to create account with
            :param password:    password to verify
            :return:            True/False if email and password are confirmed
        """
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @classmethod
    def register_valid(cls, username, email, password):
        """
            Create new user if one doesn't exist for given email

            :param username:    username for account
            :param email:       email to create account with
            :param password:    password for new account
            :return:            True/False if user doesn't exist
        """
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist so we can create it
            new_user = cls(username, email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # from session: author, author_id
        # from website: title, description
        blog = Blog(author=self.email,
                    author_id=self._id,
                    title=title,
                    description=description)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        # from website: blog_id, title, content
        # default:      date or set on website
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }

    def save_to_mongo(self):
        Database.insert('users', self.json())


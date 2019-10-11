import uuid
from src.common.database import Database

__author__ = 'chansen'


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

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
    def login_valid(email, password):
        """
            Check password matches User account attached to email given


            :param email:       email to create account with
            :param password:    password to verify
            :return:            True/False if email and password are confirmed
        """
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user['password'] == password
        return False

    @classmethod
    def register(cls, email, password):
        """
            Create new user if one doesn't exist for given email

            :param email:       email to create account with
            :param password:    password for new account
            :return:            True/False if user doesn't exist
        """
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            return True
        else:
            # User exists
            return False

    def login(self):
        pass

    def get_blogs(self):
        pass

    def json(self):
        return {
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='users',
                        data=self.json())


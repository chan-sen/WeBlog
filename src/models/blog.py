__author__ = 'chansen'

import datetime
import uuid

from src.common.database import Database
from src.models.post import Post


class Blog(object):

    def __init__(self, author, title, description, _id=None):

        self.author = author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': _id})
        return cls(**blog_data)

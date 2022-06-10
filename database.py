from datetime import datetime
from decouple import config
import hashlib

from peewee import *

database = MySQLDatabase("db_movies_review",
                         user=config("DB_USER"),
                         password=config("DB_PASSWORD"),
                         host=config("DB_HOST"), port=3306)


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = "users"

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode("utf-8"))

        return h.hexdigest()


class Movie(Model):
    title = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = "movies"


class Review(Model):
    user = ForeignKeyField(User, backref="reviews")
    movie = ForeignKeyField(Movie, backref="reviews")
    review_text = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Rating: {self.score}"

    class Meta:
        database = database
        table_name = "reviews"

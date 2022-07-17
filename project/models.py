from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey(Genre.id), nullable=False)
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey(Director.id), nullable=False)
    director = relationship("Director")


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre = Column(Integer, ForeignKey(Genre.id))
    f_genre = relationship("Genre")


class FavoriteMovie(models.Base):
    __tablename__ = 'favorite_user_movies'

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User")
    movie_id = Column(Integer, ForeignKey(Movie.id))
    movie = relationship("Movie")

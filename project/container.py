from project.dao import GenresDAO, DirectorsDao, MoviesDao, UsersDAO, FavoriteMoviesDAO

from project.services import *
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDao(db.session)
movie_dao = MoviesDao(db.session)
user_dao = UsersDAO(db.session)
favorite_movies_dao = FavoriteMoviesDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
auth_service = AuthService(user_service=user_service)
favorite_movies_service = FavoriteMoviesService(dao=favorite_movies_dao)

from typing import Optional, List, TypeVar

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User, FavoriteMovie
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDao(BaseDAO[Director]):
    __model__ = Director


class MoviesDao(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_movies(self, page: Optional[int] = None, status: Optional[str] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if status == 'new':
            try:
                stmt = stmt.order_by(desc(self.__model__.year))
            except NotFound:
                return []

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []

        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, user_data):

        user = self.__model__(**user_data)

        self._db_session.add(user)
        self._db_session.commit()

        return user

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()


class FavoriteMoviesDAO(BaseDAO[FavoriteMovie]):
    __model__ = FavoriteMovie

    def create(self, data):

        favorite_movie = self.__model__(**data)

        self._db_session.add(favorite_movie)
        self._db_session.commit()

        return favorite_movie

    def get_by_user_and_movie(self, user_id, movie_id):
        return self._db_session.query(self.__model__).filter(
            self.__model__.user_id == user_id,
            self.__model__.movie_id == movie_id,
        ).first()

    def delete(self, favorite_movie):

        self._db_session.delete(favorite_movie)
        self._db_session.commit()

    def get_by_user_id(self, user_id):
        return self._db_session.query(self.__model__).filter(
            self.__model__.user_id == user_id
        ).all()

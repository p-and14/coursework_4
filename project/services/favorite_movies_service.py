from ..dao.main import FavoriteMoviesDAO
from ..models import User


class FavoriteMoviesService:
    def __init__(self, dao: FavoriteMoviesDAO):
        self.dao = dao

    def create(self, user: User, movie_id: int):
        data = {"user_id": user.id, "movie_id": movie_id}
        return self.dao.create(data)

    def delete(self, user: User, movie_id: int):
        favorite_movie = self.dao.get_by_user_and_movie(user.id, movie_id)
        self.dao.delete(favorite_movie)

    def get_by_user_id(self, user: User):
        return self.dao.get_by_user_id(user.id)

import pytest

from project.dao import MoviesDao
from project.models import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDao(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(
            title="Йеллоустоун",
            description="Владелец ранчо пытается сохранить землю своих предков.",
            trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
            year=2015,
            rating=8.6,
            genre_id=17,
            director_id=1,
        )
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(
            title="Омерзительная восьмерка",
            description="США после Гражданской войны.",
            trailer="https://www.youtube.com/watch?v=lmB9VWm0okU",
            year=2018,
            rating=7.8,
            genre_id=4,
            director_id=2,
        )
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all_movies() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []

    def test_get_movies_by_status(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all_movies(status="new") == [movie_2, movie_1]

    def test_get_movies_by_page_and_status(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all_movies(page=1, status="new") == [movie_2]
        assert movies_dao.get_all_movies(page=2, status="new") == [movie_1]
        assert movies_dao.get_all_movies(page=3, status="new") == []

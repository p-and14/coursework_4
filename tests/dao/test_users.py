import pytest

from project.dao import UsersDAO
from project.models import User


class TestUsersDAO:

    @pytest.fixture
    def users_dao(self, db):
        return UsersDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(
            email="sasha",
            password="3HST0iK5G5VvzhiFbn69IZPLhd/oca4Qpm36dXFkJls=",
            name="Sasha",
            surname="Petrov",
            favorite_genre=1,
        )
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(
            email="qwerty",
            password="yHdeSvdh6Ht7nrAaDz+11ylvovoWKttb9hIM65wEIF4=",
            name="Egor",
            surname="Ivanov",
            favorite_genre=2,
        )
        db.session.add(u)
        db.session.commit()
        return u

    def test_get_user_by_id(self, users_dao, user_1):
        assert users_dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self, users_dao):
        assert not users_dao.get_by_id(1)

    def test_get_all_users(self, users_dao, user_1, user_2):
        assert users_dao.get_all() == [user_1, user_2]

    def test_get_users_by_page(self, app, users_dao, user_1, user_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert users_dao.get_all(page=1) == [user_1]
        assert users_dao.get_all(page=2) == [user_2]
        assert users_dao.get_all(page=3) == []

    def test_create_user(self, users_dao):
        u = {
            "email": "sasha",
            "password": "qwerty",
        }
        user = users_dao.create(u)
        assert user.id == 1
        assert user.email == "sasha"

    def test_update_user(self, users_dao, user_1):
        user_1.email = "user@mail.ru"
        user_1.name = "Andrey"

        users_dao.update(user_1)

        assert user_1.email == "user@mail.ru"
        assert user_1.name == "Andrey"

    def test_get_user_by_email(self, users_dao, user_1):
        assert users_dao.get_by_email(user_1.email) == user_1

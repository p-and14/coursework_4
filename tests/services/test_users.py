from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import User
from project.services import UsersService


class TestUsersService:

    @pytest.fixture()
    @patch('project.dao.UsersDAO')
    def users_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = User(
            id=1,
            email='test_email_1',
            password=b'test_password_1',
        )
        dao.get_all.return_value = [
            User(
                id=1,
                email='test_email_1',
                password=b'test_password_1',
            ),
            User(
                id=2,
                email='test_email_2',
                password=b'test_password_2',
            ),
        ]
        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UsersService(dao=users_dao_mock)

    @pytest.fixture
    def user(self, db):
        obj = User(
            email='test_email_1',
            password=b'test_password_1',
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_user(self, users_dao_mock, users_service, user):
        assert users_service.get_by_id(user.id) == users_dao_mock.get_by_id.return_value

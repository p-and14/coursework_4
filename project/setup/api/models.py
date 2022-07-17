from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссёр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=200, example='Тейлор Шеридан'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example='Йеллоустоун'),
    'description': fields.String(required=True, max_length=400, example='Владелец ранчо пытается сохранить землю '
                                                                        'своих предков. Кевин Костнер в неовестерне '
                                                                        'от автора «Ветреной реки»'),
    'trailer': fields.String(required=True, max_length=255, example='https://www.youtube.com/watch?v=UKei_d0cbP4'),
    'year': fields.Integer(required=True, example=2018),
    'rating': fields.Float(required=True, example=8.6),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, example='new_user@skypro.ru'),
    'password': fields.String(required=True, example=''),
    'name': fields.String(example='Иван'),
    'surname': fields.String(example='Иванов'),
    'favorite_genre': fields.String(example='Комедия'),
    'f_genre': fields.Nested(genre),
})

favorite_user_movies: Model = api.model('Избранный фильм', {
    'id': fields.Integer(required=True, example=1),
    'user_id': fields.Integer(required=True, example=1),
    'user': fields.Nested(user),
    'movie_id': fields.Integer(required=True, example=1),
    'movie': fields.Nested(movie),
})

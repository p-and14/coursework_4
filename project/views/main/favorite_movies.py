from flask_restx import Namespace, Resource

from project.container import auth_service, favorite_movies_service, user_service
from project.setup.api.models import favorite_user_movies
from project.setup.api.parsers import headers_parser

api = Namespace('favorites')


@api.route('/movies/')
class FavoriteMovies(Resource):
    @auth_service.auth_required
    @api.expect(headers_parser)
    @api.marshal_with(favorite_user_movies, code=200, description='OK')
    def get(self):
        """
        Get favorite movies for user
        """
        auth_data = headers_parser.parse_args()["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        user = user_service.get_by_email(email)

        return favorite_movies_service.get_by_user_id(user)


@api.route('/movies/<int:movie_id>/')
class FavoriteMovies(Resource):
    @auth_service.auth_required
    @api.expect(headers_parser)
    @api.marshal_with(favorite_user_movies, code=200, description='OK')
    def post(self, movie_id: int):
        """
        Add favorite movie
        """
        auth_data = headers_parser.parse_args()["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        user = user_service.get_by_email(email)

        return favorite_movies_service.create(user, movie_id)

    @auth_service.auth_required
    @api.expect(headers_parser)
    @api.marshal_with(favorite_user_movies, code=200, description='OK')
    def delete(self, movie_id: int):
        """
        Delete favorite movie
        """
        auth_data = headers_parser.parse_args()["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        user = user_service.get_by_email(email)

        return favorite_movies_service.delete(user, movie_id)

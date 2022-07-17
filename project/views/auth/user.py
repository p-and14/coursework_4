from flask_restx import Namespace, Resource

from project.container import user_service, auth_service
from project.setup.api.models import user
from project.setup.api.parsers import headers_parser, user_add_info_parser, user_passwords_parser

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @auth_service.auth_required
    @api.expect(headers_parser)
    @api.marshal_with(user, code=200, description='OK')
    def get(self):
        """
        User profile
        """
        auth_data = headers_parser.parse_args()["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        return user_service.get_by_email(email)

    @auth_service.auth_required
    @api.expect(headers_parser, user_add_info_parser)
    @api.marshal_with(user, code=201, description='OK')
    def patch(self):
        """
        Changes user information
        """
        auth_data = headers_parser.parse_args()["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        user = user_service.get_by_email(email)
        data = user_add_info_parser.parse_args()

        user.name = data["name"]
        user.surname = data["surname"]
        user.favorite_genre = data["favourite_genre"]

        return user_service.update(user)


@api.route('/password/')
class UserPassword(Resource):
    @auth_service.auth_required
    @api.expect(headers_parser, user_passwords_parser)
    @api.marshal_with(user, code=201, description='OK')
    def put(self):
        """
        Changes user password
        """
        auth_data = headers_parser.parse_args()["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_token(token)

        user = user_service.get_by_email(email)
        data = user_passwords_parser.parse_args()

        return user_service.update(user_service.change_password(user, data))

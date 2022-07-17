from flask_restx import Namespace, Resource

from ...container import auth_service
from ...setup.api.parsers import user_info_parser, tokens_parser
from project.setup.api.models import user
from project.container import user_service

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @api.expect(user_info_parser)
    @api.marshal_with(user, code=201, description='OK')
    def post(self):
        """
        Register new user
        """
        return user_service.create(user_info_parser.parse_args())


@api.route('/login/')
class AuthView(Resource):
    @api.expect(user_info_parser)
    def post(self):
        """
        Login user
        """
        data = user_info_parser.parse_args()
        email = data["email"]
        password = data["password"]
        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    @api.expect(tokens_parser)
    def put(self):
        """
        Refresh token
        """
        refresh_token = tokens_parser.parse_args()["refresh_token"]

        tokens = auth_service.approve_tokens(refresh_token)

        return tokens, 201

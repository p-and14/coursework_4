from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

movies_parser: RequestParser = RequestParser()
movies_parser.add_argument(name='page', type=int, location='args', required=False)
movies_parser.add_argument(name='status', type=str, location='args', required=False)

user_info_parser: RequestParser = RequestParser()
user_info_parser.add_argument(name='email', type=str, location='json', required=True)
user_info_parser.add_argument(name='password', type=str, location='json', required=True)

tokens_parser: RequestParser = RequestParser()
tokens_parser.add_argument(name='access_token', type=str, location='json', required=True)
tokens_parser.add_argument(name='refresh_token', type=str, location='json', required=True)

headers_parser: RequestParser = RequestParser()
headers_parser.add_argument(name='Authorization', type=str, location='headers', required=True)

user_add_info_parser: RequestParser = RequestParser()
user_add_info_parser.add_argument(name='name', type=str, location='json', required=False)
user_add_info_parser.add_argument(name='surname', type=str, location='json', required=False)
user_add_info_parser.add_argument(name='favourite_genre', type=str, location='json', required=False)

user_passwords_parser: RequestParser = RequestParser()
user_passwords_parser.add_argument(name='old_password', type=str, location='json', required=True)
user_passwords_parser.add_argument(name='new_password', type=str, location='json', required=True)

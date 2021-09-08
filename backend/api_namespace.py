import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from backend import config
from backend.models import ThoughtModel
from backend.token_validation import validate_token_header
from backend.db import db
from flask import abort

api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLICKEY)
    if username is None:
        abort(401)

    return username


authentication_parser = api_namespace.parser()
authentication_parser.add_argument(
    'Authentication', location='headers', type=str, help='Bearer Access Token')

thought_parser = authentication_parser.copy()
thought_parser.add_argument(
    'text', type=str, required=True, help='Text of the thouhgt')

search_parser = api_namespace.parser()
search_parser.add_argument(
    'search', type=str, required=False, help='Search in the text of thoughts.')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'text': fields.String(),
    'timestamp': fields.DateTime()
}

thought_model = api_namespace.model('Thought', model)


@api_namespace.route('/me/thouhgt/')
class MeThoughtListCreate(Resource):
    pass


@api_namespace.route('/thoughts/')
class ThoughtList(Resource):
    @api_namespace.doc('list_thoughts')
    @api_namespace.marshal_with(thought_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        """Retrieves all the thoughts

        Returns:
            thoughts: A list of all current thought
        """
        args = search_parser.parse_args()
        search_param = args['search']
        query = ThoughtModel.query
        if search_param:
            query = (query.filter(ThoughtModel.text.contains(search_param)))

        query = query.order_by('id')
        thoughts = query.all()
        return thoughts


@api_namespace.route('/thoughts/<int:thought_id>')
class ThoughtsRetrieve(Resource):
    @api_namespace.doc('retrieve_thought')
    @api_namespace.marshal_with(thought_model)
    def get(self, thought_id):
        """Retrieve a thought

        Args:
            thought_id (str): Id of thought
        """
        thought = ThoughtModel.query.get(thought_id)
        if not thought:
            return '', http.client.NOT_FOUND

        return thought

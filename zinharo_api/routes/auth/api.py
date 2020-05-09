from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from zinharo_api import limiter
from zinharo_api.models import db, Client
from zinharo_api.schemas import client_schema
from webargs.flaskparser import use_args
from .schemas import AuthPostSchema, AuthGetSchema

auth_api_blueprint = Blueprint("auth_api", __name__)
auth_restful = Api(auth_api_blueprint, "/auth")


class AuthApi(Resource):
    """Authorization path for clients to sign up and log in to get their jwt
    session tokens"""

    decorators = [limiter.limit("2 per minute, 4 per day", methods=["POST"])]

    @use_args(AuthPostSchema())
    def post(self, args):
        """Client sign-up (currently disabled for debug)"""

        found_dupe = Client.query.filter_by(username=args["username"]).first()

        if found_dupe:
            return {"status": "username taken"}, 403

        bio = args["bio"] if "bio" in args else None

        new_client = Client(args["username"], args["password"], bio)

        db.session.add(new_client)
        db.session.commit()

        return (
            {
                "status": "success",
                "body": {
                    "client": client_schema.dump(new_client),
                    "token": create_access_token(new_client.id),
                },
            },
            200,
        )

    @use_args(AuthGetSchema(), location="querystring")
    def get(self, args):
        """Logs client in"""

        got_client = Client.query.filter_by(username=args["username"]).first()

        if not got_client or not got_client.compare_passwords(args["password"]):
            return {"status": "invalid username or password"}, 403

        return (
            {
                "status": "success",
                "body": {"token": create_access_token(got_client.id),},
            },
            200,
        )


auth_restful.add_resource(AuthApi, "/")

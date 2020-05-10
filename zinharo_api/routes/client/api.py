from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from zinharo_api import limiter
from zinharo_api.models import db, Client
from zinharo_api.schemas import client_schema
from webargs.flaskparser import use_args
from .schemas import ClientGetSchema, ClientPatchSchema

client_api_blueprint = Blueprint("client_api", __name__)
client_restful = Api(client_api_blueprint, "/client")


class ClientApi(Resource):
    """Client API endpoint for managing your client model with RUD of CRUD."""

    decorators = [limiter.limit("3 per minute, 12 per day", methods=["PATCH"])]

    @use_args(ClientGetSchema(), location="querystring")
    def get(self, args):
        """Query for a client"""

        if len(args) == 0:
            return {"status": "no query provided"}, 400
        elif "id" in args: # favour id
            got_client = Client.query.get(args["id"])
        elif "username" in args:
            got_client = Client.query.filter_by(username=args["username"]).first()

        if got_client is not None:
            return (
                {
                    "status": "success",
                    "body": {"client": client_schema.dump(got_client)},
                },
                200,
            )

        return {"status": "not found"}, 404

    @jwt_required
    @use_args(ClientPatchSchema())
    def patch(self, args):
        """Updating user"""

        if len(args) == 0:
            return {"status": "no updates provided"}, 400

        current_client = Client.query.get(get_jwt_identity())

        if "bio" in args:
            current_client.bio = args["bio"]

        if "password" in args:
            current_client.password = current_client.gen_password(args["password"])

        db.session.commit()

        return {"status": "success", "body": {"client": client_schema.dump(current_client)}}, 200

    @jwt_required
    def delete(self):
        """Deletes user"""

        current_client = Client.query.get(get_jwt_identity())

        db.session.remove(current_client)
        db.session.commit()

        return (
            {
                "status": "success",
                "body": {"client": client_schema.dump(current_client)},
            },
            200,
        )


client_restful.add_resource(ClientApi, "/")

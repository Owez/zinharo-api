import sys
import base64
from zinharo_api import limiter
from flask import Blueprint
from flask_restful import Api, Resource
from zinharo_api import limiter
from zinharo_api.models import db, Hash
from zinharo_api.schemas import hash_schema
from webargs.flaskparser import use_args
from .schemas import HashGetSchema, HashPostSchema

hash_api_blueprint = Blueprint("hash_api", __name__)
hash_restful = Api(hash_api_blueprint, "/hash")


class HashApi(Resource):
    """
    Hash api for the main CRUD operations of hashes from a user standpoint,
    please see JobApi for client interactivity.
    
    There are no PATCH or DELETE as users should not be allowed to update/delete
    hashes; only clients with a valid, identifiabsle passkey
    """

    decorators = [
        limiter.limit("2 per minute, 10 per day", methods=["POST"]),
        limiter.limit("10 per minute, 20 per hour, 100 per day", methods=["GET"])
    ]

    @use_args(HashPostSchema())
    def post(self, args):
        """Query/assign hash to queue (get hash)"""

        try:
            base64.b64decode(
                args["cap"]
            )  # decode to ensure valid base64 (but don't use it)
        except:
            return {"status": "not valid base64"}, 400

        got_hash = Hash.query.filter_by(cap=args["cap"]).first()

        if got_hash is None:
            got_hash = Hash(args["cap"])

            db.session.add(got_hash)
            db.session.commit()

            return (
                {"status": "success", "body": {"hash": hash_schema.dump(got_hash)}},
                200,
            )  # make new hash
        elif len(got_hash.jobs) != 0:
            return (
                {"status": "completed", "body": {"hash": hash_schema.dump(got_hash)}},
                200,
            )  # if hash has finished jobs
        else:
            return (
                {"status": "queued", "body": {"hash": hash_schema.dump(got_hash)}},
                202,
            )  # if hash is already queued

    @use_args(HashGetSchema(), location="querystring")
    def get(self, args):
        """Gets a hash"""

        if len(args) == 0:
            return {"status": "no query provided"}, 400

        if args["id"]:
            got_hash = Hash.query.get(args["id"])
        elif args["password"]:
            got_hash = Hash.query.filter_by(password=args["password"]).first()

        if got_hash is None:
            return {"status": "no hash found"}, 404

        return {"status": "success", "body": {"hash": hash_schema.dump(got_hash)}}, 200


hash_restful.add_resource(HashApi, "/")

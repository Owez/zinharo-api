from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from zinharo_api import limiter
from zinharo_api.models import db, Client, Hash, Job
from zinharo_api.schemas import job_schema, job_queued_schema
from webargs.flaskparser import use_args
from .schemas import JobPostSchema

job_api_blueprint = Blueprint("job_api", __name__)
job_restful = Api(job_api_blueprint, "/job")


class JobApi(Resource):
    """Job API endpoint for clients to connect to for retrevial of hashes to
    crack and publish when finished, hence only allowing GET and POST with DELETE
    coming in the future for cancelling jobs"""

    decorators = [
        limiter.limit("2 per minute", methods=["POST"]),
        limiter.limit("5 per minute, 35 per hour", methods=["GET"]),
    ]

    @jwt_required
    @use_args(JobPostSchema())
    def post(self, args):
        """For finalising and uploaded the completed job"""

        current_client = Client.query.get(get_jwt_identity())

        got_hash = Hash.query.get(args["id"])

        finished_job = Job(args["password"])

        finished_job.client_id = current_client.id
        finished_job.hash_id = got_hash.id

        db.session.add(finished_job)
        db.session.commit()

        return (
            {"status": "success", "body": {"job": job_schema.dump(finished_job)}},
            200,
        )

    @jwt_required
    def get(self):
        """Auto-assign a job"""

        current_client = Client.query.get(get_jwt_identity())

        # got_hash = Hash.query.order_by(Hash.created.desc()).first() # NOTE: used for untrusted clients
        # got_hash = Hash.query.filter_by(jobs=None) # NOTE: used for trusted clients
        possible_hashes = Hash.query.all()

        # TODO make more efficiant, this is horribly so
        for got_hash in possible_hashes:
            job_ids = [i.client_id for i in got_hash.jobs]
            report_ids = [i.client_id for i in got_hash.reports]

            if (
                len(got_hash.jobs) < 2
                and len(got_hash.reports) < 2
                and current_client.id not in job_ids
                and current_client.id not in report_ids
            ):
                return (
                    {
                        "status": "success",
                        "body": {"queued": job_queued_schema.dump(got_hash)},
                    },
                    200,
                )

        return {"status": "no jobs avalible"}, 404


job_restful.add_resource(JobApi, "/")

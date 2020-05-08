from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from zinharo_api import limiter
from zinharo_api.models import db, Client, Report, Hash
from zinharo_api.schemas import report_schema
from webargs.flaskparser import use_args
from .schemas import ReportGetSchema, ReportPostSchema

report_api_blueprint = Blueprint("report_api", __name__)
report_restful = Api(report_api_blueprint, "/report")


class ReportApi(Resource):
    """Report API endpoint for primarily adding reports to bad jobs"""

    decorators = [limiter.limit("2 per minute", methods=["POST"])]

    @jwt_required
    @use_args(ReportPostSchema())
    def post(self, args):
        """Add a report to a job"""

        info = args["info"] if "info" in args else None

        current_client = Client.query.get(get_jwt_identity())
        got_hash = Hash.query.get(args["hash_id"])

        if got_hash is None:
            return {"status": "invalid hash"}, 400

        new_report = Report(info)

        new_report.client_id = current_client.id
        new_report.hash_id = got_hash.id

        db.session.add(new_report)
        db.session.commit()

        return (
            {"status": "success", "body": {"report": report_schema.dump(new_report)}},
            200,
        )

    @use_args(ReportGetSchema(), location="querystring")
    def get(self, args):
        """Query for an existing report"""

        got_report = Report.query.get(args["id"])

        if got_report is not None:
            return (
                {
                    "status": "success",
                    "body": {"report": report_schema.dump(got_report)},
                },
                200,
            )

        return {"status": "report not found"}, 404


report_restful.add_resource(ReportApi, "/")

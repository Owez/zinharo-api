"""Contains global, commonly-used schemas that are shared between routes"""

from . import ma


class ReportSchema(ma.Schema):
    """A schema for a single report issued by a user. This can be used in bulk
    as this is a simple model"""

    created = ma.DateTime(format="%Y-%m-%dT%H:%M:%S+00:00")

    class Meta:
        fields = ("id", "client_id", "hash_id", "info", "created")


class JobSchema(ma.Schema):
    """A finished job (password)"""

    created = ma.DateTime(format="%Y-%m-%dT%H:%M:%S+00:00")

    class Meta:
        fields = ("id", "password", "client_id", "hash_id", "created")


class HashSchema(ma.Schema):
    """Generalized hash schema, displaying all public info"""

    jobs = ma.Nested("JobSchema", many=True, exclude=("hash_id",))
    reports = ma.Nested("ReportSchema", many=True, exclude=("hash_id",))
    created = ma.DateTime(format="%Y-%m-%dT%H:%M:%S+00:00")

    class Meta:
        fields = ("id", "pcap", "passwords", "created", "jobs", "reports")


class ClientSchema(ma.Schema):
    """A client connected to the API"""

    # like HashSchema's but with x_id switched
    jobs = ma.Nested("JobSchema", many=True, exclude=("client_id",))
    reports = ma.Nested("ReportSchema", many=True, exclude=("client_id",))
    created = ma.DateTime(format="%Y-%m-%dT%H:%M:%S+00:00")

    class Meta:
        fields = ("id", "username", "bio", "created", "jobs", "reports")


class JobQueuedSchema(ma.Schema):
    """A subset of HashSchema that will turn into a Job, basically a newly
    assigned job"""

    created = ma.DateTime(format="%Y-%m-%dT%H:%M:%S+00:00")

    class Meta:
        fields = ("id", "pcap", "created")


report_schema = ReportSchema()
job_schema = JobSchema()
hash_schema = HashSchema()
client_schema = ClientSchema()
job_queued_schema = JobQueuedSchema()

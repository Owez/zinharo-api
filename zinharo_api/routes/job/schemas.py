from zinharo_api import ma


class JobPostSchema(ma.Schema):
    """Schema for finishing a job"""

    id = ma.Integer(required=True)
    password = ma.String(required=True)

    class Meta:
        strict = True

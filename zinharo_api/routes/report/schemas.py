from zinharo_api import ma

class ReportPostSchema(ma.Schema):
    """Schema for adding a report"""

    hash_id = ma.Integer(required=True)
    info = ma.String(required=False)

    class Meta:
        strict = True

class ReportGetSchema(ma.Schema):
    """Schema for querying for a report"""

    id = ma.Integer(required=True)

    class Meta:
        strict = True

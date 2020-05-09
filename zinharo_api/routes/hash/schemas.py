from flask_marshmallow.fields import fields
from zinharo_api import ma

class HashPostSchema(ma.Schema):
    """Schema for adding a hash"""

    cap = ma.String(required=True, validate=fields.validate.Length(max=3500000)) # base64 only, max 2.5mb

    class Meta:
        strict = True


class HashGetSchema(ma.Schema):
    """Schema for fetching a hash, it can use any one of the three shown below"""

    id = ma.Integer(required=False)
    password = ma.String(required=False)

    class Meta:
        strict = True


class HashDeleteSchema(ma.Schema):
    """Schema for deleting a hash, it can use any one of the three shown below,
    similar to HashGetSchema"""

    id = ma.Integer(required=False)
    password = ma.String(required=False)

    class Meta:
        strict = True

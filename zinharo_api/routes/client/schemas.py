from zinharo_api import ma


class ClientGetSchema(ma.Schema):
    """Schema for querying for a client"""

    id = ma.Integer(required=False)
    username = ma.String(required=False)

    class Meta:
        strict = True


class ClientPatchSchema(ma.Schema):
    """Schema for updating a client"""

    bio = ma.String(required=False)
    password = ma.String(required=False)

    class Meta:
        strict = True

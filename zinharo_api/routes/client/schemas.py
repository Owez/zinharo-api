from zinharo_api import ma


class ClientGetSchema(ma.Schema):
    """Schema for querying for a client"""

    username = ma.String(required=True)

    class Meta:
        strict = True


class ClientPatchSchema(ma.Schema):
    """Schema for updating a client"""

    bio = ma.String(required=False)
    password = ma.String(required=False)

    class Meta:
        strict = True

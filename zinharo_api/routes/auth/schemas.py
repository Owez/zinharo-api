from zinharo_api import ma


class AuthPostSchema(ma.Schema):
    """Client signup schema"""

    username = ma.String(required=True)
    password = ma.String(required=True)
    bio = ma.String(required=False)

    class Meta:
        strict = True


class AuthGetSchema(ma.Schema):
    """Schema for signing/logging a client in"""

    username = ma.String(required=True)
    password = ma.String(required=True)

    class Meta:
        strict = True
from zinharo_api import ma


# NOTE: not used for debug
# class AuthPostSchema(ma.Schema):
#     """Client signup schema"""

#     # TODO: this

#     class Meta:
#         strict = True


class AuthGetSchema(ma.Schema):
    """Schema for signing/logging a client in"""

    username = ma.String(required=True)
    password = ma.String(required=True)

    class Meta:
        strict = True
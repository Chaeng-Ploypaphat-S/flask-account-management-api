from marhmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    email = fields.Str(required=True, validate=lambda x: len(x) <= 100)
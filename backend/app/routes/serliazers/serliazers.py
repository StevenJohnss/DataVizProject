from marshmallow import Schema, fields, validate

class UserSchema(Schema):
  email = fields.String(required=True, validate=validate.Length(min=3, max=30))
  password = fields.String(required=True, validate=validate.Length(min=6))
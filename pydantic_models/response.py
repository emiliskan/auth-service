from config.app import ma
from marshmallow import fields


class ResponseSchema(ma.SQLAlchemySchema):
    code = fields.Int()
    message = fields.Str()

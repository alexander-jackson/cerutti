from marshmallow import Schema, fields, post_load


class Registration:
    def __init__(self, name: str):
        self.name = name


class RegistrationSchema(Schema):
    name = fields.Str()

    @post_load
    def make_registration(self, data, **kwargs):
        return Registration(**data)

from marshmallow import Schema, fields, validate, ValidationError
from src.models.user import User
from src.models.curso import Curso

class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class CursoSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    descricao = fields.Str(allow_none=True)

class TopicoCreateSchema(Schema):
    titulo = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    mensagem = fields.Str(required=True, validate=validate.Length(min=10))
    curso_nome = fields.Str(required=True, validate=validate.Length(min=2, max=100))

class TopicoUpdateSchema(Schema):
    titulo = fields.Str(validate=validate.Length(min=5, max=200))
    mensagem = fields.Str(validate=validate.Length(min=10))
    curso_nome = fields.Str(validate=validate.Length(min=2, max=100))


from datetime import datetime

from extensions import db

class Colaborador(db.Model):

    __tablename__ = 'colaboradores'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    matricula = db.Column(
        db.String(20),
        nullable=False
    )

    rfid_tag = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    cargo = db.Column(
        db.String(50),
        nullable=False
    )

    acesso_permitido = db.Column(
        db.Boolean,
        default=False
    )

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
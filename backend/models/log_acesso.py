from datetime import datetime

from extensions import db

class LogAcesso(db.Model):

    __tablename__ = 'logs_acesso'

    id = db.Column(db.Integer, primary_key=True)

    colaborador_id = db.Column(
        db.Integer,
        db.ForeignKey('colaboradores.id')
    )

    nome_tag_nao_cadastrada = db.Column(
        db.String(100)
    )

    rfid_tag_lida = db.Column(
        db.String(50)
    )

    tipo_evento = db.Column(
        db.String(20)
    )

    data_hora = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    observacao = db.Column(
        db.Text
    )
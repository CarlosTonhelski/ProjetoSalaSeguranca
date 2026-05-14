from flask import Blueprint, jsonify
from models.colaborador import Colaborador
from models.log_acesso import LogAcesso

monitoramento_bp = Blueprint('monitoramento', __name__)

@monitoramento_bp.route('/logs')
def listar_logs():
    logs = LogAcesso.query.order_by(LogAcesso.id.desc()).all()
    lista = []
    for log in logs:
        lista.append({
            'id': log.id,
            'colaborador_id': log.colaborador_id,
            'tag': log.rfid_tag_lida,
            'tipo_evento': log.tipo_evento,
            'observacao': log.observacao,
            'data_hora': log.data_hora.isoformat() if log.data_hora else None
        })
    return jsonify(lista)

@monitoramento_bp.route('/monitoramento')
def monitoramento():
    logs = LogAcesso.query.order_by(LogAcesso.id.desc()).limit(10).all()
    lista = []
    for log in logs:
        lista.append({
            'tag': log.rfid_tag_lida,
            'evento': log.tipo_evento,
            'data': log.data_hora.isoformat() if log.data_hora else None,
            'observacao': log.observacao
        })
    return jsonify(lista)

@monitoramento_bp.route('/sala')
def colaboradores_na_sala():
    logs = LogAcesso.query.order_by(LogAcesso.id.asc()).all()
    dentro = {}
    for log in logs:
        if log.colaborador_id:
            colaborador = Colaborador.query.get(log.colaborador_id)
            if colaborador:
                if log.tipo_evento == 'ENTRADA':
                    dentro[colaborador.nome] = True
                elif log.tipo_evento == 'SAIDA':
                    if colaborador.nome in dentro:
                        del dentro[colaborador.nome]
    return jsonify(list(dentro.keys()))
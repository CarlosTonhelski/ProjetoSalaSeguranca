import pandas as pd

from flask import Blueprint, jsonify

from models.log_acesso import LogAcesso

export_bp = Blueprint(
    'export',
    __name__
)

# EXPORTAR CSV
@export_bp.route('/exportar')
def exportar_csv():

    logs = LogAcesso.query.all()

    dados = []

    for log in logs:

        dados.append({
            'id': log.id,
            'colaborador_id': log.colaborador_id,
            'tag': log.rfid_tag_lida,
            'evento': log.tipo_evento,
            'observacao': log.observacao,
            'data_hora': log.data_hora
        })

    df = pd.DataFrame(dados)

    df.to_csv(
        'logs.csv',
        index=False
    )

    return jsonify({
        'mensagem': 'CSV exportado com sucesso'
    })
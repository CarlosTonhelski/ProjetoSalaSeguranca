from flask import Blueprint, request, jsonify

from datetime import datetime

from extensions import db

from models.colaborador import Colaborador
from models.log_acesso import LogAcesso

rfid_bp = Blueprint(
    'rfid',
    __name__
)

# RFID
@rfid_bp.route('/rfid', methods=['POST'])
def receber_rfid():

    dados = request.get_json()

    if not dados.get('rfid_tag'):

        return jsonify({
            'erro': 'RFID obrigatória'
        }), 400

    tag = dados.get('rfid_tag')

    colaborador = Colaborador.query.filter_by(
        rfid_tag=tag
    ).first()

    # TAG CADASTRADA
    if colaborador:

        # INATIVO
        if not colaborador.ativo:

            log = LogAcesso(
                colaborador_id=colaborador.id,
                rfid_tag_lida=tag,
                tipo_evento='NEGADO',
                observacao='Colaborador inativo'
            )

            db.session.add(log)
            db.session.commit()

            return jsonify({
                'status': 'negado',
                'mensagem': 'Colaborador inativo'
            }), 403

        # AUTORIZADO
        if colaborador.acesso_permitido:

            ultimo_log = LogAcesso.query.filter_by(
                colaborador_id=colaborador.id
            ).order_by(
                LogAcesso.id.desc()
            ).first()

            hoje = datetime.utcnow().date()

            entrada_hoje = LogAcesso.query.filter(
                LogAcesso.colaborador_id == colaborador.id,
                LogAcesso.tipo_evento == 'ENTRADA'
            ).all()

            ja_entrou_hoje = False

            for entrada in entrada_hoje:

                if entrada.data_hora.date() == hoje:

                    ja_entrou_hoje = True
                    break

            # ENTRADA
            if not ultimo_log or ultimo_log.tipo_evento == 'SAIDA':

                log = LogAcesso(
                    colaborador_id=colaborador.id,
                    rfid_tag_lida=tag,
                    tipo_evento='ENTRADA',
                    observacao='Entrada autorizada'
                )

                db.session.add(log)
                db.session.commit()

                mensagem = 'Bem-vindo'

                if ja_entrou_hoje:

                    mensagem = (
                        f'Bem-vindo de volta, '
                        f'{colaborador.nome}'
                    )

                else:

                    mensagem = (
                        f'Bem-vindo, '
                        f'{colaborador.nome}'
                    )

                return jsonify({
                    'status': 'permitido',
                    'nome': colaborador.nome,
                    'mensagem': mensagem,
                    'tipo_evento': 'ENTRADA',
                    'data_hora': log.data_hora
                }), 201

            # SAIDA
            else:

                log = LogAcesso(
                    colaborador_id=colaborador.id,
                    rfid_tag_lida=tag,
                    tipo_evento='SAIDA',
                    observacao='Saida registrada'
                )

                db.session.add(log)
                db.session.commit()

                tempo_permanencia = (
                    log.data_hora - ultimo_log.data_hora
                )

                return jsonify({
                    'status': 'saida',
                    'nome': colaborador.nome,
                    'mensagem': 'Saida registrada',
                    'tipo_evento': 'SAIDA',
                    'tempo_permanencia': str(
                        tempo_permanencia
                    ),
                    'data_hora': log.data_hora
                }), 201

        # NEGADO
        else:

            log = LogAcesso(
                colaborador_id=colaborador.id,
                rfid_tag_lida=tag,
                tipo_evento='NEGADO',
                observacao='Colaborador sem permissao'
            )

            db.session.add(log)
            db.session.commit()

            return jsonify({
                'status': 'negado',
                'nome': colaborador.nome,
                'mensagem': 'Acesso negado',
                'tipo_evento': 'NEGADO',
                'data_hora': log.data_hora
            }), 403

    # INVASAO
    else:

        log = LogAcesso(
            nome_tag_nao_cadastrada='Desconhecido',
            rfid_tag_lida=tag,
            tipo_evento='INVASAO',
            observacao='RFID nao cadastrada'
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            'status': 'invasao',
            'mensagem': 'Tentativa de invasao detectada',
            'tipo_evento': 'INVASAO',
            'data_hora': log.data_hora
        }), 404
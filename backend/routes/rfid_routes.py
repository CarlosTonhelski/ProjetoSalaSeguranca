from flask import Blueprint, request, jsonify
from datetime import datetime
from extensions import db
from models.colaborador import Colaborador
from models.log_acesso import LogAcesso

rfid_bp = Blueprint('rfid', __name__)

@rfid_bp.route('/rfid', methods=['POST'])
def receber_rfid():

    dados = request.get_json()

    if not dados or not dados.get('rfid_tag'):
        return jsonify({'erro': 'RFID obrigatoria'}), 400

    tag = dados.get('rfid_tag', '').strip().upper()

    colaborador = Colaborador.query.filter_by(rfid_tag=tag).first()

    if colaborador:

        if not colaborador.ativo:
            log = LogAcesso(
                colaborador_id=colaborador.id,
                rfid_tag_lida=tag,
                tipo_evento='NEGADO',
                observacao='Colaborador inativo',
                data_hora=datetime.utcnow()
            )
            db.session.add(log)
            db.session.commit()
            return jsonify({
                'status': 'negado',
                'mensagem': 'Colaborador inativo',
                'tipo_evento': 'NEGADO',
                'data_hora': log.data_hora.isoformat()
            }), 403

        if colaborador.acesso_permitido:

            ultimo_log = LogAcesso.query.filter(
                LogAcesso.colaborador_id == colaborador.id,
                LogAcesso.tipo_evento.in_(['ENTRADA', 'SAIDA'])
            ).order_by(LogAcesso.id.desc()).first()

            hoje = datetime.utcnow().date()
            entradas_hoje = LogAcesso.query.filter(
                LogAcesso.colaborador_id == colaborador.id,
                LogAcesso.tipo_evento == 'ENTRADA'
            ).all()
            ja_entrou_hoje = any(
                e.data_hora.date() == hoje for e in entradas_hoje
            )

            if not ultimo_log or ultimo_log.tipo_evento == 'SAIDA':
                log = LogAcesso(
                    colaborador_id=colaborador.id,
                    rfid_tag_lida=tag,
                    tipo_evento='ENTRADA',
                    observacao='Entrada autorizada',
                    data_hora=datetime.utcnow()
                )
                db.session.add(log)
                db.session.commit()

                mensagem = (
                    f'Bem-vindo de volta, {colaborador.nome}'
                    if ja_entrou_hoje
                    else f'Bem-vindo, {colaborador.nome}'
                )
                return jsonify({
                    'status': 'permitido',
                    'nome': colaborador.nome,
                    'mensagem': mensagem,
                    'tipo_evento': 'ENTRADA',
                    'data_hora': log.data_hora.isoformat()
                }), 201

            else:
                agora = datetime.utcnow()
                log = LogAcesso(
                    colaborador_id=colaborador.id,
                    rfid_tag_lida=tag,
                    tipo_evento='SAIDA',
                    observacao='Saida registrada',
                    data_hora=agora
                )
                db.session.add(log)
                db.session.commit()

                tempo_permanencia = log.data_hora - ultimo_log.data_hora
                return jsonify({
                    'status': 'saida',
                    'nome': colaborador.nome,
                    'mensagem': 'Saida registrada',
                    'tipo_evento': 'SAIDA',
                    'tempo_permanencia': str(tempo_permanencia),
                    'data_hora': log.data_hora.isoformat()
                }), 201

        else:
            log = LogAcesso(
                colaborador_id=colaborador.id,
                rfid_tag_lida=tag,
                tipo_evento='NEGADO',
                observacao='Colaborador sem permissao',
                data_hora=datetime.utcnow()
            )
            db.session.add(log)
            db.session.commit()
            return jsonify({
                'status': 'negado',
                'nome': colaborador.nome,
                'mensagem': 'Acesso negado',
                'tipo_evento': 'NEGADO',
                'data_hora': log.data_hora.isoformat()
            }), 403

    else:
        log = LogAcesso(
            nome_tag_nao_cadastrada='Desconhecido',
            rfid_tag_lida=tag,
            tipo_evento='INVASAO',
            observacao='RFID nao cadastrada',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({
            'status': 'invasao',
            'mensagem': 'Tentativa de invasao detectada',
            'tipo_evento': 'INVASAO',
            'data_hora': log.data_hora.isoformat()
        }), 404
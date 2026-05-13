from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from flask_cors import CORS

# FLASK
app = Flask(__name__)
CORS(app)
# POSTGRESQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:admin123@localhost:5432/sala_seguranca'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DATABASE
db = SQLAlchemy(app)

# MODELS
class Colaborador(db.Model):

    __tablename__ = 'colaboradores'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    matricula = db.Column(db.String(20), nullable=False)

    rfid_tag = db.Column(db.String(50), unique=True, nullable=False)

    cargo = db.Column(db.String(50), nullable=False)

    acesso_permitido = db.Column(db.Boolean, default=False)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class LogAcesso(db.Model):

    __tablename__ = 'logs_acesso'

    id = db.Column(db.Integer, primary_key=True)

    colaborador_id = db.Column(
        db.Integer,
        db.ForeignKey('colaboradores.id')
    )

    nome_tag_nao_cadastrada = db.Column(db.String(100))

    rfid_tag_lida = db.Column(db.String(50))

    tipo_evento = db.Column(db.String(20))

    data_hora = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    observacao = db.Column(db.Text)

# ROTA HOME
@app.route('/')
def home():

    return jsonify({
        'mensagem': 'Backend funcionando'
    })

# LOGIN ADMIN
@app.route('/login', methods=['POST'])
def login():

    dados = request.get_json()

    usuario = dados.get('username')
    senha = dados.get('senha')

    if usuario == 'admin' and senha == 'admin123':

        return jsonify({
            'status': 'sucesso',
            'mensagem': 'Login realizado com sucesso'
        })

    return jsonify({
        'status': 'erro',
        'mensagem': 'Usuário ou senha inválidos'
    }), 401

# LISTAR COLABORADORES
@app.route('/colaboradores', methods=['GET'])
def listar_colaboradores():

    colaboradores = Colaborador.query.all()

    lista = []

    for c in colaboradores:

        lista.append({
            'id': c.id,
            'nome': c.nome,
            'matricula': c.matricula,
            'rfid_tag': c.rfid_tag,
            'cargo': c.cargo,
            'acesso_permitido': c.acesso_permitido,
            'ativo': c.ativo,
            'criado_em': c.criado_em
        })

    return jsonify(lista)

# CRIAR COLABORADOR
@app.route('/colaboradores', methods=['POST'])
def criar_colaborador():

    dados = request.get_json()

    campos_obrigatorios = [
        'nome',
        'matricula',
        'rfid_tag',
        'cargo'
    ]

    for campo in campos_obrigatorios:

        if not dados.get(campo):

            return jsonify({
                'erro': f'Campo obrigatório: {campo}'
            }), 400

    tag_existente = Colaborador.query.filter_by(
        rfid_tag=dados.get('rfid_tag')
    ).first()

    if tag_existente:

        return jsonify({
            'erro': 'RFID já cadastrada'
        }), 409

    novo = Colaborador(
        nome=dados.get('nome'),
        matricula=dados.get('matricula'),
        rfid_tag=dados.get('rfid_tag'),
        cargo=dados.get('cargo'),
        acesso_permitido=dados.get(
            'acesso_permitido',
            False
        ),
        ativo=dados.get('ativo', True)
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        'mensagem': 'Colaborador criado com sucesso',
        'id': novo.id
    }), 201

# EDITAR COLABORADOR
@app.route('/colaboradores/<int:id>', methods=['PUT'])
def editar_colaborador(id):

    colaborador = Colaborador.query.get(id)

    if not colaborador:

        return jsonify({
            'erro': 'Colaborador não encontrado'
        }), 404

    dados = request.get_json()

    if 'rfid_tag' in dados:

        tag_existente = Colaborador.query.filter_by(
            rfid_tag=dados.get('rfid_tag')
        ).first()

        if tag_existente and tag_existente.id != id:

            return jsonify({
                'erro': 'RFID já cadastrada'
            }), 409

    colaborador.nome = dados.get(
        'nome',
        colaborador.nome
    )

    colaborador.matricula = dados.get(
        'matricula',
        colaborador.matricula
    )

    colaborador.rfid_tag = dados.get(
        'rfid_tag',
        colaborador.rfid_tag
    )

    colaborador.cargo = dados.get(
        'cargo',
        colaborador.cargo
    )

    colaborador.acesso_permitido = dados.get(
        'acesso_permitido',
        colaborador.acesso_permitido
    )

    colaborador.ativo = dados.get(
        'ativo',
        colaborador.ativo
    )

    db.session.commit()

    return jsonify({
        'mensagem': 'Colaborador atualizado com sucesso'
    })

# DELETAR COLABORADOR
@app.route('/colaboradores/<int:id>', methods=['DELETE'])
def deletar_colaborador(id):

    colaborador = Colaborador.query.get(id)

    if not colaborador:

        return jsonify({
            'erro': 'Colaborador não encontrado'
        }), 404

    db.session.delete(colaborador)
    db.session.commit()

    return jsonify({
        'mensagem': 'Colaborador removido com sucesso'
    })

# LISTAR LOGS
@app.route('/logs')
def listar_logs():

    logs = LogAcesso.query.order_by(
        LogAcesso.id.desc()
    ).all()

    lista = []

    for log in logs:

        lista.append({
            'id': log.id,
            'colaborador_id': log.colaborador_id,
            'tag': log.rfid_tag_lida,
            'tipo_evento': log.tipo_evento,
            'observacao': log.observacao,
            'data_hora': log.data_hora
        })

    return jsonify(lista)

# MONITORAMENTO EM TEMPO REAL
@app.route('/monitoramento')
def monitoramento():

    logs = LogAcesso.query.order_by(
        LogAcesso.id.desc()
    ).limit(10).all()

    lista = []

    for log in logs:

        lista.append({
            'tag': log.rfid_tag_lida,
            'evento': log.tipo_evento,
            'data': log.data_hora,
            'observacao': log.observacao
        })

    return jsonify(lista)

# COLABORADORES DENTRO DA SALA
@app.route('/sala')
def colaboradores_na_sala():

    logs = LogAcesso.query.order_by(
        LogAcesso.id.asc()
    ).all()

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

# RECEBER RFID
@app.route('/rfid', methods=['POST'])
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

        # COLABORADOR INATIVO
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
                    mensagem = f'Bem-vindo de volta, {colaborador.nome}'
                else:
                    mensagem = f'Bem-vindo, {colaborador.nome}'

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
                    'tempo_permanencia': str(tempo_permanencia),
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
    
# EXPORTAR CSV
@app.route('/exportar')
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

    df.to_csv('logs.csv', index=False)

    return jsonify({
        'mensagem': 'CSV exportado com sucesso'
    })

# START
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

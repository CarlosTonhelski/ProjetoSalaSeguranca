from flask import Blueprint, request, jsonify

from extensions import db

from models.colaborador import Colaborador

colaborador_bp = Blueprint(
    'colaborador',
    __name__
)

# LISTAR
@colaborador_bp.route('/colaboradores', methods=['GET'])
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

# CRIAR
@colaborador_bp.route('/colaboradores', methods=['POST'])
def criar_colaborador():

    dados = request.get_json()

    novo = Colaborador(
        nome=dados.get('nome'),
        matricula=dados.get('matricula'),
        rfid_tag=dados.get('rfid_tag'),
        cargo=dados.get('cargo'),
        acesso_permitido=dados.get(
            'acesso_permitido',
            False
        ),
        ativo=dados.get(
            'ativo',
            True
        )
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        'mensagem': 'Colaborador criado'
    }), 201

# EDITAR
@colaborador_bp.route('/colaboradores/<int:id>', methods=['PUT'])
def editar_colaborador(id):

    colaborador = Colaborador.query.get(id)

    if not colaborador:

        return jsonify({
            'erro': 'Colaborador não encontrado'
        }), 404

    dados = request.get_json()

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
        'mensagem': 'Colaborador atualizado'
    })

# DELETE
@colaborador_bp.route('/colaboradores/<int:id>', methods=['DELETE'])
def deletar_colaborador(id):

    colaborador = Colaborador.query.get(id)

    if not colaborador:

        return jsonify({
            'erro': 'Colaborador não encontrado'
        }), 404

    db.session.delete(colaborador)

    db.session.commit()

    return jsonify({
        'mensagem': 'Colaborador removido'
    })
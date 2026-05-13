from flask import Blueprint, request, jsonify

auth_bp = Blueprint(
    'auth',
    __name__
)

# LOGIN
@auth_bp.route('/login', methods=['POST'])
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
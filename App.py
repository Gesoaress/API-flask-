from flask import Flask, request, jsonify

app = Flask(__name__)

# Estrutura de dados em memória
usuarios = []
current_id = 1

# CREATE - adicionar usuário
@app.route('/users', methods=['POST'])
def criar_usuario():
    global current_id
    dados = request.json

    if not dados or "nome" not in dados or "email" not in dados:
        return jsonify({"error": "Dados inválidos. Envie 'nome' e 'email'."}), 400

    novo_usuario = {
        "id": current_id,
        "nome": dados["nome"],
        "email": dados["email"]
    }
    usuarios.append(novo_usuario)
    current_id += 1

    return jsonify(novo_usuario), 201


# READ ALL - listar todos os usuários
@app.route('/users', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios), 200


# READ SINGLE - buscar usuário por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def buscar_usuario(user_id):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return jsonify(usuario), 200
    return jsonify({"error": "Usuário não encontrado"}), 404


# UPDATE - atualizar usuário
@app.route('/users/<int:user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    dados = request.json
    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuario["nome"] = dados.get("nome", usuario["nome"])
            usuario["email"] = dados.get("email", usuario["email"])
            return jsonify(usuario), 200
    return jsonify({"error": "Usuário não encontrado"}), 404


# DELETE - remover usuário
@app.route('/users/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuarios.remove(usuario)
            return jsonify({"message": "Usuário excluído com sucesso"}), 200
    return jsonify({"error": "Usuário não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)

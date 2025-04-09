from flask import Flask, request, jsonify
from flask_cors import CORS
#-----import novo -----#
from flask import Flask
import usuarios

import bairros
import cidades
import estados
import usuarios

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Mapeamento de rotas
route_map = {
    'bairros': bairros,
    'cidades': cidades,
    'estados': estados,
    'users': usuarios
}

@app.route('/<resource>/auth', methods=["GET", "POST"])
def auth(resource):
    return usuarios.auth()

@app.route('/<resource>', methods=["GET", "POST"])
@app.route('/<resource>/<int:id>', methods=["GET", "PUT", "DELETE"])
def handle_resource(resource, id=None):
    if resource in route_map:
        if request.method == "GET":
            if id is not None:
                return route_map[resource].getBy(id)    
            return route_map[resource].get()
        
        elif request.method == "POST":
            return route_map[resource].post()
        elif request.method == "PUT":
            return route_map[resource].alterar(request.args.get(id))
        elif request.method == "DELETE":
            return route_map[resource].apagar(request.args.get(id))
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True)

#----------- alterações abaixo --------#

app = Flask(__name__)

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return usuarios.get()

@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    return usuarios.getBy(id)

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    return usuarios.post()

@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    return usuarios.alterar(id)

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    return usuarios.apagar(id)

@app.route('/usuarios/auth', methods=['POST'])
def autenticar_usuario():
    return usuarios.auth()

if __name__ == '__main__':
    app.run(debug=True)
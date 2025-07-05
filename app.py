from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/esquadria'

app.app_context()

# Para criar a tabela no banco de dados via command Line, foi preciso rodar os seguintes comandos:
# from app import app, db
# app.app_context().push()
# db.create_all()
# para isso foi necessario declarar a funcao app_context:
# app.app_context()

db = SQLAlchemy(app)

class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    cliente_nome  = db.Column(db.String(50))
    tipo_material  = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "cliente_nome": self.cliente_nome, "tipo_material": self.tipo_material}


# Fazer relação
# class Cliente(db.Model):
#     id = db.Column(db.Integer, primary_key= True)
#     cliente_nome  = db.Column(db.String(50))
#     telefone = db.Column(db.String(50))




# Selecionar Tudo
@app.route("/orcamentos", methods=["GET"])
def seleciona_orcamentos():
    usuarios_objetos = Orcamento.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

    return gera_response(200, "orcamentos", usuarios_json)

# Selecionar Individual
@app.route("/orcamento/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Orcamento.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "orcamento", usuario_json)

# # Cadastrar
# @app.route("/usuario", methods=["POST"])
# def cria_usuario():
#     body = request.get_json()

#     try:
#         usuario = Usuario(nome=body["nome"], email= body["email"])
#         db.session.add(usuario)
#         db.session.commit()
#         return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
#     except Exception as e:
#         print('Erro', e)
#         return gera_response(400, "usuario", {}, "Erro ao cadastrar")


# # Atualizar
# @app.route("/usuario/<id>", methods=["PUT"])
# def atualiza_usuario(id):
#     usuario_objeto = Usuario.query.filter_by(id=id).first()
#     body = request.get_json()

#     try:
#         if('nome' in body):
#             usuario_objeto.nome = body['nome']
#         if('email' in body):
#             usuario_objeto.email = body['email']
        
#         db.session.add(usuario_objeto)
#         db.session.commit()
#         return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
#     except Exception as e:
#         print('Erro', e)
#         return gera_response(400, "usuario", {}, "Erro ao atualizar")

# # Deletar
# @app.route("/usuario/<id>", methods=["DELETE"])
# def deleta_usuario(id):
#     usuario_objeto = Usuario.query.filter_by(id=id).first()

#     try:
#         db.session.delete(usuario_objeto)
#         db.session.commit()
#         return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
#     except Exception as e:
#         print('Erro', e)
#         return gera_response(400, "usuario", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "chave_super_secreta_grande_123456789"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

jwt = JWTManager(app)
CORS(app)


# CRIAR BANCO AUTOMATICAMENTE
def criar_banco():

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        senha TEXT
    )
    """)

    conn.commit()
    conn.close()


criar_banco()


# TESTE BACKEND
@app.route("/")
def home():
    return "Backend funcionando!"


# CADASTRO
@app.route("/cadastro", methods=["POST"])
def cadastro():

    dados = request.json

    email = dados["email"]
    senha = generate_password_hash(dados["senha"])

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))

    if cursor.fetchone():
        conn.close()
        return jsonify({"mensagem": "Email já cadastrado"}), 400

    cursor.execute(
        "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
        (email, senha)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"})


# LOGIN
@app.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    email = dados["email"]
    senha = dados["senha"]

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, senha FROM usuarios WHERE email=?",
        (email,)
    )

    usuario = cursor.fetchone()

    conn.close()

    if usuario and check_password_hash(usuario[2], senha):

        # TOKEN GUARDA O ID DO USUÁRIO
        token = create_access_token(identity=usuario[1])

        return jsonify({
            "mensagem": "Login OK",
            "token": token,
            "email": usuario[1]
        })

    return jsonify({"erro": "Credenciais inválidas"}), 401


# LISTAR USUÁRIOS
@app.route("/usuarios", methods=["GET"])
@jwt_required()
def listar_usuarios():

    usuario_logado = get_jwt_identity()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, email FROM usuarios")

    usuarios = cursor.fetchall()

    conn.close()

    lista = []

    for u in usuarios:
        lista.append({
            "id": u[0],
            "email": u[1]
        })

    return jsonify(lista)


# DELETAR USUÁRIO
@app.route("/usuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_usuario(id):

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário deletado com sucesso"})


# PERFIL DO USUÁRIO LOGADO
@app.route("/me", methods=["GET"])
@jwt_required()
def usuario_logado():

    user_email = get_jwt_identity()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email FROM usuarios WHERE email=?",
        (user_email,)
    )

    usuario = cursor.fetchone()

    conn.close()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": usuario[0],
        "email": usuario[1]
    })


if __name__ == "__main__":
    app.run(debug=True)
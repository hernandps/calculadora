from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.secret_key = "clave-super-secreta"

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    clave = db.Column(db.String(100), nullable=False)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    if not session.get("usuario"):
        return redirect(url_for("login"))
    return render_template("index.html", usuario=session["usuario"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        user = Usuario.query.filter_by(usuario=usuario, clave=clave).first()
        if user:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/registro", methods=["POST"])
def registro():
    usuario = request.form["usuario"]
    clave = request.form["clave"]
    nuevo = Usuario(usuario=usuario, clave=clave)
    try:
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("login"))
    except IntegrityError:
        db.session.rollback()
        return render_template("login.html", error="Usuario ya existe")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

@app.route("/calcular", methods=["POST"])
def calcular():
    if not session.get("usuario"):
        return jsonify({"error": "No autorizado"}), 401
    data = request.get_json()
    try:
        resultado = eval(data["expresion"])
        return jsonify({"resultado": resultado})
    except Exception:
        return jsonify({"error": "Expresión inválida"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

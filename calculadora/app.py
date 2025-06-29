from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "clave-secreta-muy-larga"  # Puedes cambiarla por algo más aleatorio

# Usuarios válidos (usuario: contraseña)
USUARIOS = {
    "admin": "1234",
    "invitado": "demo"
}

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
        if usuario in USUARIOS and USUARIOS[usuario] == clave:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

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
    app.run(host="0.0.0.0", port=port, debug=False)

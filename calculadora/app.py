from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json()
    try:
        resultado = eval(data["expresion"])
        return jsonify({"resultado": resultado})
    except Exception:
        return jsonify({"error": "Expresión inválida"}), 400

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

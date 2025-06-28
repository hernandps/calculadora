from flask import Flask, render_template, request, jsonify

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
    app.run(debug=True)

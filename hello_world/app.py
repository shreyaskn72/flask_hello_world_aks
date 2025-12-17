from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask on AKS!"


@app.route("/add", methods=["POST"])
def add_numbers():
    data = request.get_json()

    a = data.get("a")
    b = data.get("b")

    if a is None or b is None:
        return jsonify({"error": "Please provide a and b"}), 400

    return jsonify({
        "a": a,
        "b": b,
        "sum": a + b
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, render_template, jsonify
import sys, io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("challenge.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    user_code = data.get("code", "")
    stdout = io.StringIO()

    try:
        sys.stdout = stdout
        exec(user_code, {}, {})
    except Exception as e:
        return jsonify({ "output": f"❌ Fehler: {str(e)}" })

    output = stdout.getvalue()
    return jsonify({ "output": output or "✅ Kein Fehler, aber keine Ausgabe." })

@app.route("/submit", methods=["POST"])
def submit():
    user_code = request.form.get("code")
    return f"<pre>✅ Code wurde empfangen:\n\n{user_code}</pre>"

if __name__ == "__main__":
    app.run(debug=True)

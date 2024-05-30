from flask import Flask, request

auth_data = {"authorization_code": None}

app = Flask(__name__)

@app.route('/exchange_token')
def exchange_token():
    auth_data["authorization_code"] = request.args.get('code')
    return "Authorization code received. You can close this window."

def run_flask_app():
    app.run(port=8000)

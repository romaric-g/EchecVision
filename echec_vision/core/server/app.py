from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/start", methods=['POST'])
def start_game():
    return "<p>Vous venez de lancer la partie</p>"

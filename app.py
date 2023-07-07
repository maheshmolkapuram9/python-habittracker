import os
from flask import Flask,Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv
from routes import pages
load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.habittracket
    app.register_blueprint(pages)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5200)
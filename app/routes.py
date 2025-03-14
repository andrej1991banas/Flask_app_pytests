from flask import jsonify
from .utils import add_numbers, get_home_message

def init_routes(app):
    @app.route('/')
    def home():
        # return jsonify({"message": "Welcome to the Flask App"}), 200
        return jsonify(get_home_message()), 200

    @app.route('/add/<int:a>/<int:b>')
    def add(a, b):
        result = add_numbers(a, b)  # Call helper function
        return jsonify({"result": result}), 200

    @app.route('/about')
    def about():
        return "About Page", 200
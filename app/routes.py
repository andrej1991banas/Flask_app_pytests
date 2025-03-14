from flask import jsonify, request, render_template
from .utils import add_numbers, get_home_message
from .models import Item
from .forms import ItemForm
from . import db

def init_routes(app):
    # Existing Routes
    @app.route('/')
    def home():
        return jsonify(get_home_message()), 200

    @app.route('/add/<int:a>/<int:b>')
    def add(a, b):
        result = add_numbers(a, b)
        return jsonify({"result": result}), 200

    @app.route('/about')
    def about():
        return "About Page", 200

    # New CRUD Routes
    @app.route('/items', methods=['POST'])
    def create_item():
        form = ItemForm()
        if form.validate_on_submit():
            item = Item(name=form.name.data, description=form.description.data)
            db.session.add(item)
            db.session.commit()
            return jsonify({"id": item.id, "name": item.name, "description": item.description}), 201
        return jsonify({"error": "Invalid form data", "errors": form.errors}), 400

    @app.route('/items', methods=['GET'])
    def get_items():
        items = Item.query.all()
        return jsonify([{"id": i.id, "name": i.name, "description": i.description} for i in items]), 200

    @app.route('/items/<int:id>', methods=['GET'])
    def get_item(id):
        item = Item.query.get_or_404(id)
        return jsonify({"id": item.id, "name": item.name, "description": item.description}), 200

    @app.route('/items/<int:id>', methods=['PUT'])
    def update_item(id):
        item = Item.query.get_or_404(id)
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify({"id": item.id, "name": item.name, "description": item.description}), 200

    @app.route('/items/<int:id>', methods=['DELETE'])
    def delete_item(id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200

    # Form Handling Route
    @app.route('/submit', methods=['GET', 'POST'])
    def submit_form():
        form = ItemForm()
        if form.validate_on_submit():
            return jsonify({"message": "Form submitted", "name": form.name.data, "description": form.description.data}), 200
        return render_template('submit.html', form=form)  # We'll need a template for GET
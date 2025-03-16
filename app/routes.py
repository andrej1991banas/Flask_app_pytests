from flask import jsonify, abort, request, render_template
from .utils import add_numbers, get_home_message
from .models import Item
from .forms import ItemForm
from . import db

def init_routes(app):

    # Existing Routes
    @app.route('/')
    def home():
        return jsonify(get_home_message()), 200

    # Enhanced /add Route
    @app.route('/add/<a>/<b>')
    def add(a, b):
        try:
            a, b = int(a), int(b)  # Convert to integers
            result = add_numbers(a, b)
            return jsonify({"result": result}), 200
        except ValueError:
            return jsonify({"error": "Invalid input: parameters must be integers"}), 400

    @app.route('/about')
    def about():
        return "About Page", 200

    # New CRUD Routes with Enhanced Error Handling
    @app.route('/items', methods=['POST'])
    def create_item():
        if not request.form:
            return jsonify({"error": "No form data provided"}), 400
        form = ItemForm()
        if form.validate_on_submit():
            item = Item(name=form.name.data, description=form.description.data)
            db.session.add(item)
            db.session.commit()
            return jsonify({"id": item.id, "name": item.name, "description": item.description}), 201
        return jsonify({"error": "Invalid form data"}), 400

    @app.route('/items', methods=['GET'])
    def get_items():
        items = Item.query.all()
        return jsonify([{"id": i.id, "name": i.name, "description": i.description} for i in items]), 200

    @app.route('/items/<int:id>', methods=['GET'])
    def get_item(id):
        item = Item.query.get(id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        item_data = {"id": item.id, "name": item.name, "description": item.description}
        return jsonify(item_data), 200

    @app.route('/items/<int:id>', methods=['PUT'])
    def update_item(id):
        item = Item.query.get(id)
        if not request.is_json:
            return jsonify({"error": "Request must contain JSON data"}), 400

        if not item:
            return jsonify({"error": "Item not found"}), 404

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if name is not None and not isinstance(name, str):
            return jsonify({"error": "Invalid type for 'name'. Expected a string."}), 400
        if description is not None and not isinstance(description, str):
            return jsonify({"error": "Invalid type for 'description'. Expected a string."}), 400

        item.name = name if name is not None and len(name) >0 else item.name #len(name) >0 preventing from commiting empty strings
        item.description = description if description is not None and len(description) >0 else item.description #len(name) >0 preventing from commiting empty strings
        db.session.commit()
        return jsonify({"id": item.id, "name": item.name, "description": item.description}), 200

    @app.route('/items/<int:id>', methods=['DELETE'])
    def delete_item(id):
        item = Item.query.get(id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200

    # Form Handling Route with Consistent Responses
    @app.route('/submit', methods=['GET', 'POST'])
    def submit_form():
        form = ItemForm()
        if request.method == 'POST':
            if not request.form:
                return jsonify({"error": "No form data provided"}), 400
            if form.validate_on_submit():
                return jsonify({
                    "message": "Form submitted",
                    "name": form.name.data,
                    "description": form.description.data
                }), 200
            else:
                # Use form.errors for consistency with /items POST
                errors = form.errors
                if "name" in errors:
                    if any("required" in msg.lower() for msg in errors["name"]):
                        return jsonify({"error": "Name required"}), 400
                    if any("longer than" in msg.lower() for msg in errors["name"]):
                        return jsonify({"error": "Name is too long"}), 400
                if "description" in errors:
                    if any("longer than" in msg.lower() for msg in errors["description"]):
                        return jsonify({"error": "Description is too long"}), 400
                return jsonify({"error": "Invalid form data", "errors": errors}), 400
        # For GET requests, render the form HTML page with explicit 200
        return render_template('submit.html', form=form), 200
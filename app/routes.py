from flask import jsonify, abort, request, render_template
from .utils import add_numbers, get_home_message
from .models import Item
from .forms import ItemForm
from . import db

def init_routes(app):

    @app.route('/')
    def home():
        return jsonify(get_home_message()), 200

    @app.route('/add/<a>/<b>')
    def add(a, b):
        try:
            a, b = int(a), int(b)
            result = add_numbers(a, b)
            return jsonify({"result": result}), 200
        except ValueError:
            return jsonify({"error": "Invalid input: parameters must be integers"}), 400

    @app.route('/about')
    def about():
        return "About Page", 200

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
        return jsonify({"error": "Invalid form data", "errors": form.errors}), 400

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
        if not item:
            return jsonify({"error": "Item not found"}), 404

        if not request.is_json:  # Add this for robustness
            return jsonify({"error": "Request must contain JSON data"}), 400

        data = request.get_json()
        if data is None:  # Handle case where JSON parsing fails
            return jsonify({"error": "Invalid JSON data"}), 400

        name = data.get('name')
        description = data.get('description')

        if name is not None and not isinstance(name, str):
            return jsonify({"error": "Invalid type for 'name'. Expected a string."}), 400
        if description is not None and not isinstance(description, str):
            return jsonify({"error": "Invalid type for 'description'. Expected a string."}), 400

        item.name = name if name is not None and len(name)>0 else item.name
        item.description = description if description is not None and len(description)>0 else item.description
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

    @app.route('/submit', methods=['GET', 'POST'])
    def submit_form():
        form = ItemForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # Return JSON on successful submission
                return jsonify({
                    "message": "Form submitted",
                    "name": form.name.data,
                    "description": form.description.data
                }), 200
            else:
                if len(form.name.data) > 25:
                    # Return JSON with error details when form is invalid
                    return jsonify({
                        "error": "Name is too long"
                    }), 400
                if len(form.description.data) > 200:
                    # Return JSON with error details when form is invalid
                    return jsonify({
                        "error": "Description is too long"
                    }), 400
                if form.name.data == "":
                    # Return JSON with error details when form is invalid
                    return jsonify({
                        "error": "Name required"
                    }), 400

        # For GET requests, render the form HTML page
        return render_template('submit.html', form=form)

    # New Route for Config Testing
    @app.route('/config-status')
    def config_status():
        debug_mode = app.config['DEBUG_MODE']
        return jsonify({"debug_mode": debug_mode}), 200

    # New Route for 500 Error Testing
    @app.route('/trigger-error')
    def trigger_error():
        # Intentionally raise an exception
        result = 1 / 0  # ZeroDivisionError
        return jsonify({"result": result}), 200  # Unreachable due to error

    @app.errorhandler(ZeroDivisionError) ##error handler for specific error when occur
    def handle_zero_division_error(e):
        response = jsonify({"error": "An internal server error occurred - ZeroDivisionError"})
        response.status_code = 500
        return response

import pytest
from app import create_app, db
from app.models import Item

@pytest.fixture
def app():
    """initialize the instance of the app"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """initialize the client"""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize the database with a sample item."""
    with app.app_context():
        item1 = Item(name="John", description = "bla")
        item2 = Item(name="Jane", description = "bla2")
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()
        yield
        db.session.rollback()
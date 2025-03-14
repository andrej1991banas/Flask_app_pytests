import pytest
import json
from app import create_app
from app.utils import get_home_message, add_numbers ## import the helper function

@pytest.fixture
def app():
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


# TEST CASES
def test_home_route(client):
    """Test the home page for status code and message in json"""
    response = client.get('/')
    assert response.status_code == 200 #check status code
    assert response.is_json #check we receive json data
    assert response.content_type == 'application/json'

    # Parse JSON and check data
    data = json.loads(response.data)
    assert data["message"] == "Welcome to the Flask App"


def test_get_home_message(client):
    message = get_home_message() # use of helper func
    assert message == {"message": "Welcome to the Flask App"}


def test_add(client):

    response = client.get('/add/4/6')
    assert response.status_code == 200  #check status code
    assert response.content_type == 'application/json'#check for JSON data

    data= json.loads(response.data)
    assert data["result"]==10

    response = client.get('/add/-2/3')
    assert response.status_code == 404 #check status code

    response = client.get('/add/abc/7')
    assert response.status_code == 404


def test_about_route(client):
    """Test the about page for status code and message"""
    response = client.get('/about')
    assert response.status_code == 200   #check status code
    assert b"About Page" in response.data #assert the presence of the string


def test_configuration_else(client):
    """Test that the 'else' block sets TESTING to False."""
    config_name = ('Produciton') #Any value other than 'testing'
    app = create_app(config_name)

    # Verify that TESTING is set to False
    assert app.config['TESTING'] is False


def test_add_numbers(client):
    result = add_numbers(5, 7)
    assert result == 12

    result = add_numbers(0,10)
    assert result == 10

    result = add_numbers(1000, 2000)
    assert result == 3000

    result = add_numbers(-3, -4)
    assert result == -7
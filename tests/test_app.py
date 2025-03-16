import json
from app import create_app
from app.utils import get_home_message, add_numbers ## import the helper function



"""Unit Tests
   - Routes/Endpoints (status codes, response content)
   - View Functions (logic in isolation)
   - Helper Functions (utility/business logic)"""

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
    assert app.config['TESTING'] is False # Verify that TESTING is set to False


def test_add_numbers(client):
    result = add_numbers(5, 7)
    assert result == 12

    result = add_numbers(0,10)
    assert result == 10

    result = add_numbers(1000, 2000)
    assert result == 3000

    result = add_numbers(-3, -4)
    assert result == -7



"""Integration Tests
   - Database Interactions (CRUD operations)
   - Form Handling (submissions, validation)
   - API Endpoints (JSON responses, error handling)"""

def test_create_item(client):
    """Test submitting the form with valid data redirects to success."""
    form_data = {
        'name': 'Jane',
        'description': 'hello'
    }
    response = client.post('/items', data=form_data)
    assert response.status_code == 201
    assert response.get_json() == {'id': 1, 'name': 'Jane', 'description': 'hello'} #data for database

    form_data = {'name': '', 'description': 'hello'}
    response = client.post('/items', data=form_data)
    # Parse JSON and check data
    data = json.loads(response.data)
    assert response.status_code == 400 #expecting error page
    assert data["error"] == "Invalid form data" #expecting error message

    response = client.get('/items')
    assert response.status_code == 200 #check status code
    assert b"Jane" in response.data #check insert of the data
    assert b"hello" in response.data


def test_adding_to_database(client, init_database):
    response = client.get('/items')

    data = response.get_json() # Get the JSON response from the test client (query of all items from db)
    assert response.status_code == 200
    assert len(data) == 2 #check if 2 items were added to db from init_database func
    assert data[0] == {"id": 1, "name": "John", "description": "bla"} #returning first item from database
    assert data[1] == {"id": 2, "name": "Jane", "description": "bla2"} #returning second item from database


def test_getting_item_by_id (client, init_database, app):
    """Test the success page with a valid user ID."""
    response = client.get('/items/1') #returning data for id.item from database
    data = response.get_json() #returned data from database from item with id=1
    assert response.status_code == 200
    assert data == {"id": 1, "name": "John", "description": "bla"}

    response = client.get('/items/3') #error when id not found
    data= response.get_json() #retuning data None, as the item with id=3 not exists
    assert response.status_code == 404 #page not found response
    assert data["error"] == "Item not found" #error message from 404 page


def test_putting_new_details_with_item_id(client, init_database, app):
    """Test updating an item's details by ID."""
    # Send a PUT request with updated data
    update_data = {
        "name": "Eric",
        "description": "new description"
    }
    response = client.put('/items/1', json = update_data)
    data = response.get_json() #get updated response data

    assert response.status_code == 200
    assert data == {"id": 1, "name": "Eric", "description": "new description"}

    #validate the case the database was updated properly too
    from app.models import Item
    item = Item.query.get(1) #pick item with id=1 and check for right update
    assert item.name == "Eric"
    assert item.description == "new description"

    #test for good data but not existing item
    response = client.put('/items/3', json = update_data)
    data = response.get_json()
    assert response.status_code == 404
    assert data["error"] == "Item not found"

    #test for TypeError message when wrong type of data is put to update the item
    updated_data = {"name": 1,
                    "description": "new description"
                    }
    response = client.put('/items/1', json = updated_data)
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid type for 'name'. Expected a string."

    updated_data = {"name": "Alice",
                    "description": 2
                    }
    response = client.put('/items/1', json=updated_data)
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid type for 'description'. Expected a string."


def test_delete_item_with_item_id(client, init_database, app):
    """test deleting the item with item id"""
    response = client.delete('/items/1')
    data = response.get_json()
    assert response.status_code == 200
    assert data ["message"] == "Item deleted"

    #test deleting the item with item_id from database
    from app.models import Item
    item = Item.query.get(1)  # pick item with id=1 and check for right update
    assert item is None ##id is already taken, but I have to look for None if the item is deleted from database
    assert response.status_code == 200

    #test deleting the item with item_id (not existing one) with response 404
    response = client.delete('/items/3')
    data = response.get_json()
    assert response.status_code == 404
    assert data["error"] == "Item not found"


"""Form Handling (Submissions, Validation)"""

def test_submit_works(client):
    """verifying rendering HTML page with everything on it"""
    # Test GET request to render the form
    response = client.get('/submit')
    assert response.status_code == 200
    assert b"Submit an Item" in response.data
    assert b"Name" in response.data #data for submit the form
    assert b"Description" in response.data #data for submit the form

    # Test POST request to submit the form
    response = client.post('/submit', data={'name': 'John', 'description': 'bla'})
    assert response.status_code == 200
    assert b"Form submitted" in response.data

    """ test POST request for wrong data """

    response = client.post('/submit', data={'name': '', 'description': 'bla2'}) #passing missing data for name
    data= response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Name required" #not submitting data with missing name

    response = client.post('/submit', data={'name': 'sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss', 'description': 'bla2'})  # passing missing data for name
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Name is too long" #not submitting data with name exceeded 25 char

    #Test that the HTML form is correctly rendered in the response.
    response = client.get('/submit')
    data = response.data.decode('utf-8')
    assert response.status_code == 200 #rendering the template
    assert b"Submit an Item" in response.data #renderinv submit.html
    assert "<form" in data # Checks that a form tag exists in the HTML
    # Check for specific <label> tags by their "for" attribute
    assert '<label for="name">' in data  # Check label for name field
    assert '<label for="description">' in data  # Check label for description field


def test_items_for_no_form_data_with_post(client):
    """ test for invalid data and not validating the form """
    form_data = {"name": "",
                "description": "This is a description"
                 }
    response= client.post('/items', data=form_data)
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Invalid form data"

    #test for no data provided for form
    form_data = {}
    response = client.post('/items', data=form_data)
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "No form data provided"


def test_non_integer_data_input_for_add_number(client):
    """ test for non integer input for add route"""
    response = client.get('/add/12.5/7')
    data= response.get_json()
    assert response.status_code == 400  # check status code
    assert data["error"] == "Invalid input: parameters must be integers"
    assert response.content_type == 'application/json'  # check for JSON data


def test_item_for_put_not_json_data(client):
    """ test for non json data with PUT request and error message"""
    invalid_data = "John bla" # Plain text, not a JSON object
    response = client.put('/items/1', data=invalid_data, content_type='text/plain')
    data= response.get_json()   # Convert the response to JSON for validation
    assert response.status_code == 400
    assert data["error"] == "Request must contain JSON data"


def test_create_item_for_valid_data(client):
    """ test creating new item with valid data """
    #not using ini_database as parameter I will assert id=1
    response = client.post('/items', data={'name': 'Andrej', 'description': 'lorem'})
    data = response.get_json()
    assert response.status_code == 201
    assert data == {'id': 1, 'name': 'Andrej', 'description': 'lorem'} #in case I add "init_database" func as parameter to main func, i have to assert id==3
    assert response.content_type == 'application/json'


def test_item_put_update_only_one_field(client, init_database):
    """Test updating only one field of the item."""
    update_data = {"name": "Andrej", "description": ""} # Update only the "name" field even the description is empty string
    # Convert the update_data dictionary to a JSON string
    response = client.put('/items/1', data=json.dumps(update_data), content_type='application/json')
    data= response.get_json()
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    assert data == {'id': 1, 'name': 'Andrej', 'description': 'bla'}


def test_content_type_across_routes(client, init_database, app):
    response = client.post('/items', data={'name': 'Andrej', 'description': 'lorem'})
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    response = client.get('/items')
    assert response.content_type == 'application/json'

    response = client.get('/items/1')
    assert response.content_type == 'application/json'

    response = client.put('/items/1', data={'name': 'Andrej', 'description': 'lorem'})
    assert response.content_type == 'application/json'

    response = client.delete('/items/1')
    assert response.content_type =='application/json'

    response = client.get('/add/1/2')
    assert response.content_type == 'application/json'

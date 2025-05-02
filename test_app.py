from app import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_and_get_record(client):
    # Add
    response = client.post('/records', json={'content': 'test'})
    assert response.status_code == 201
    record_id = response.get_json()['id']

    # Get
    get_response = client.get(f'/records/{record_id}')
    assert get_response.status_code == 200
    assert get_response.get_json()['content'] == 'test'

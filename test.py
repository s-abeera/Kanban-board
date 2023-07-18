import os
import tempfile
import unittest

import pytest
from app import create_app
from app.db import get_db, init_db


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
    
class TestConfig(unittest.TestCase):
    def test_config(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })
        assert app.config['TESTING'] == True


    def test_db(self):
        db_fd, db_path = tempfile.mkstemp()
        app = create_app({
            'TESTING': True,
            'DATABASE': db_path,
        })
        
        with app.app_context():
            init_db()
            db = get_db()
            assert db is get_db()


    def test_hello(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })

        with app.test_client() as client:
            response = client.get('/hello')
            assert b'Hello, World!' in response.data

    def test_login(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })
        with app.test_client() as client:
            response = client.get('/auth/login')
            assert b'Log In' in response.data

    def test_register(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })
        with app.test_client() as client:
            response = client.get('/auth/register')
            assert b'Register' in response.data

    
    def test_index(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })
        with app.test_client() as client:
            response = client.get('/')
            assert b'Landing page' in response.data

    def test_logout(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })
        with app.test_client() as client:
            response = client.get('/auth/logout')
            assert b'Log In' in response.data

    def test_kanban(self):
        app = create_app({
            'TESTING': True,
            'DATABASE': os.path.join(tempfile.gettempdir(), 'test.db'),
        })
        
        with app.test_client() as client:
             # Create a login session
            response = client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            assert b'Log In' in response.data
            

if __name__ == '__main__':
    unittest.main()
  
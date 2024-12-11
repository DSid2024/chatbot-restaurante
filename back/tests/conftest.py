import pytest
from app.app import create_app



@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

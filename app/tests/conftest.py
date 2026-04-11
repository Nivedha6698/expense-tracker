import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app("test")
    '''
        app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    '''


    with app.app_context():
        db.create_all()   # create tables
        yield app.test_client()
        db.drop_all()     # cleanup after tests
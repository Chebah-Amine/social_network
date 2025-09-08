import pytest
from django.contrib.auth import get_user_model
from network.models import Post

# Needed object during test
# Pytest-django use a test data-base every sql transaction is rollback at the end of the test

User = get_user_model()


@pytest.fixture
def user(db):
    # db indicates to pytest-django this test/fixture needs access to the database
    return User.objects.create_user(
        username="amine", email="am@test.com", password="pass1234"
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="karim", email="karim@test.com", password="pass1234"
    )


@pytest.fixture
def client_logged(client, user):
    client.login(username="amine", password="pass1234")
    return client


@pytest.fixture
def post(user):
    return Post.objects.create(user=user, content="Hello world")

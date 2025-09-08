import pytest
from django.urls import reverse

# TEST REGISTER


@pytest.mark.django_db
def test_register_get(client):
    response = client.get(reverse("register"))

    assert b"Already have an account?" in response.content


@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "new@test.com",
            "password": "pass1234",
            "confirmation": "pass1234",
        },
    )

    assert response.status_code == 302  # redirect
    assert "/" in response.url


@pytest.mark.django_db
def test_register_password_mismatch(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "new@test.com",
            "password": "pass1234",
            "confirmation": "wrongpass",
        },
    )

    # check the error message in the response / b --> for byte
    assert b"Passwords must match." in response.content


@pytest.mark.django_db
def test_register_existing_username(client, user):
    response = client.post(
        reverse("register"),
        {
            "username": "amine",
            "email": "amine@test.com",
            "password": "pass1234",
            "confirmation": "pass1234",
        },
    )

    assert b"Username already taken." in response.content


# TEST LOGIN


@pytest.mark.django_db
def test_login_get(client):
    response = client.get(reverse("login"))

    assert b"Don't have an account?" in response.content


@pytest.mark.django_db
def test_login_successfull(client, user):
    response = client.post(
        reverse("login"), {"username": "amine", "password": "pass1234"}
    )

    assert response.status_code == 302  # redirect
    assert "/" in response.url


@pytest.mark.django_db
def test_login_unsuccessfull(client):
    response = client.post(
        reverse("login"), {"username": "amine", "password": "pass1234"}
    )

    assert b"Invalid username and/or password." in response.content


# TEST LOGOUT


@pytest.mark.django_db
def test_logout(
    client_logged,
    user,
):
    response = client_logged.get(reverse("logout"))

    assert response.status_code == 302

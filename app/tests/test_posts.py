import pytest
from django.urls import reverse
from network.views import NewPostForm

MAX_POST_LENGTH = 500


@pytest.mark.django_db
def test_new_post_success(client_logged):
    response = client_logged.post(reverse("new_post"), {"content": "Mon premier post"})
    assert response.status_code == 302


@pytest.mark.django_db
def test_new_post_too_long(client_logged):
    long_content = "a" * (MAX_POST_LENGTH + 1)
    _ = client_logged.post(reverse("new_post"), {"content": long_content})
    form = NewPostForm(data={"content": long_content})
    assert not form.is_valid()


@pytest.mark.django_db
def test_edit_post_by_owner(client_logged, post):
    url = reverse("edit_post", args=[post.id])
    response = client_logged.put(
        url, data={"content": "Updated!"}, content_type="application/json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_post_by_other_user(client, another_user, post):
    client.login(username="karim", password="pass1234")
    url = reverse("edit_post", args=[post.id])
    response = client.put(
        url, data={"content": "Hacked"}, content_type="application/json"
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_authentification_required(client, post):
    url = reverse("edit_post", args=[post.id])
    response = client.put(
        url, data={"content": "Updated!"}, content_type="application/json"
    )
    assert response.status_code == 401

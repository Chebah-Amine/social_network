import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_like_unlike_post(client_logged, post):
    url = reverse("toggle_like", args=[post.id])
    r1 = client_logged.post(url)
    assert r1.status_code == 200
    r2 = client_logged.post(url)
    assert r2.status_code == 200


@pytest.mark.django_db
def test_authentification_required(client, post):
    url = reverse("toggle_like", args=[post.id])
    response = client.post(url)
    assert response.status_code == 401

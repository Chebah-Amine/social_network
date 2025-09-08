import pytest
from django.urls import reverse
from network.models import Follow


@pytest.mark.django_db
def test_follow_unfollow(client_logged, another_user):
    url = reverse("toggle_follow", args=[another_user.username])
    # follow
    r1 = client_logged.post(url)
    assert r1.status_code == 200
    assert Follow.objects.filter(
        follower__username="amine", following=another_user
    ).exists()
    # unfollow
    r2 = client_logged.post(url)
    assert r2.status_code == 200
    assert not Follow.objects.filter(
        follower__username="amine", following=another_user
    ).exists()


@pytest.mark.django_db
def test_follow_self(client_logged, user):
    url = reverse("toggle_follow", args=[user.username])
    response = client_logged.post(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_authentification_required(client, user):
    url = reverse("toggle_follow", args=[user.username])
    response = client.post(url)
    assert response.status_code == 401

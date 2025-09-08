import pytest
from django.urls import reverse
from network.models import Post


@pytest.mark.django_db
def test_profile_view(client_logged, user):
    Post.objects.create(user=user, content="Post 1")
    Post.objects.create(user=user, content="Post 2")

    response = client_logged.get(reverse("profile", args=[user.username]))

    assert response.status_code == 200
    assert "Post 1" in response.content.decode()
    assert "Post 2" in response.content.decode()
    assert "Followers" in response.content.decode()
    assert "Following" in response.content.decode()
    assert "Posts" in response.content.decode()


@pytest.mark.django_db
def test_profile_nonexistent_user(client_logged):
    response = client_logged.get(reverse("profile", args=["not_a_user"]))

    assert response.status_code == 200
    assert "User not_a_user does not exist" in response.content.decode()

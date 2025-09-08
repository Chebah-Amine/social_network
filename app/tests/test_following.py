import pytest
from django.urls import reverse
from network.models import Post, Follow


@pytest.mark.django_db
def test_following_posts(client_logged, user, django_user_model):
    other_user = django_user_model.objects.create_user(
        username="other", password="pass1234"
    )
    third_user = django_user_model.objects.create_user(
        username="third", password="pass1234"
    )

    post1 = Post.objects.create(user=other_user, content="Hello from other")
    post2 = Post.objects.create(user=third_user, content="Hello from third")

    Follow.objects.create(follower=user, following=other_user)

    response = client_logged.get(reverse("following_posts"))

    assert response.status_code == 200
    content = response.content.decode()
    assert post1.content in content
    assert post2.content not in content

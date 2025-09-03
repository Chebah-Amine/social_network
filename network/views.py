from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django import forms

from .models import User, Post, Follow


class NewPostForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-2",
                "rows": 4,
                "placeholder": "What's on your mind?",
            }
        ),
        label="New Post",
        max_length=500,
    )

@login_required
def index(request):
    try:
        posts = Post.objects.all().order_by("-created_at")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")

        if not page_number or not page_number.isdecimal():
            page_number = 1
        else:
            page_number = int(page_number)

        page_obj = paginator.get_page(page_number)
    except Exception as e:
        return render(
            request,
            "network/error.html",
            {"code": 400, "message": "Error loading all posts, {e}"},
        )

    return render(
        request, "network/index.html", {"form": NewPostForm(), "page": page_obj}
    )


@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            Post.objects.create(user=request.user, content=content)
            return redirect("index")
        else:
            posts = Post.objects.all().order_by("-created_at")
            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number or 1)
            return render(
                request,
                "network/index.html",
                {"form": form, "page": page_obj},
            )
    return redirect("index")


@login_required
def profile(request, username):
    try:
        profile_user = get_object_or_404(User, username=username)
        posts = profile_user.posts.all().order_by("-created_at")
        followers = profile_user.followers.count()
        following = profile_user.following.count()
        is_following = Follow.objects.filter(
            follower=request.user, following=profile_user
        ).exists()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number or 1)
    except Exception as e:
        return render(
            request,
            "network/error.html",
            {"code": 400, "message": f"User {username} does not exist, {e}"},
        )
    return render(
        request,
        "network/profile.html",
        {
            "profile_user": profile_user,
            "page": page_obj,
            "followers": followers,
            "following": following,
            "is_following": is_following,
            "nb_posts": len(posts),
        },
    )


@login_required
def following_posts(request):
    try:
        followed_users = Follow.objects.filter(follower=request.user).values_list(
            "following", flat=True
        )
        posts = Post.objects.filter(user__in=followed_users).order_by("-created_at")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number or 1)
    except Exception as e:
        return render(
            request,
            "network/error.html",
            {"code": 400, "message": "Error loading following posts, {e}"},
        )
    return render(request, "network/following.html", {"page": page_obj})


@csrf_exempt
def edit_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            post = get_object_or_404(Post, id=post_id, user=request.user)
            if request.user == post.user:
                data = json.loads(request.body)
                # get the content value if it exists or give the actual content value (post.content)
                post.content = data.get("content", post.content)
                post.save()
                return JsonResponse(
                    {
                        "message": "Post updated successfully.",
                        "post": post.serialize(),
                        "is_liked": post.is_liked(request.user),
                    },
                    status=200,
                )
            return JsonResponse(
                {
                    "error": "WRONG USER ! You are no authorized to update this post",
                    "redirect": reverse("index"),
                },
                status=401,
            )
    else:
        return JsonResponse(
            {"error": "Authentication required", "redirect": reverse("login")},
            status=401,
        )


@csrf_exempt
def toggle_like(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = get_object_or_404(Post, id=post_id)
            liked = post.is_liked(request.user)
            if liked:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return JsonResponse(
                {"likes": post.like_count(), "is_liked": liked}, status=200
            )
    else:
        return JsonResponse(
            {"error": "Authentication required", "redirect": reverse("login")},
            status=401,
        )


@csrf_exempt
def toggle_follow(request, username):
    if request.user.is_authenticated:
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow == request.user:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)
        follow_relationship, created = Follow.objects.get_or_create(
            follower=request.user, following=user_to_follow
        )
        if not created:
            follow_relationship.delete()
        return JsonResponse(
            {"followers": user_to_follow.followers.count(), "is_following": created},
            status=200,
        )
    else:
        return JsonResponse(
            {"error": "Authentication required", "redirect": reverse("login")},
            status=401,
        )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

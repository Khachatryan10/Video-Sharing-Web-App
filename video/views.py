from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import User, Comments, Video, Likes
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import requests

import json

from datetime import datetime

# Create your views here.


def index(request):
    return render(request, "video/index.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if len(username) < 1 or len(email) < 1 or len(password) < 1 or len(confirmation) < 1:
            return render(request, "video/register_user.html", {
                "error": "Please fill all fields"
            })

        if len(password) < 8 or len(confirmation) < 8:
            return render(request, "video/register_user.html", {
                "error": "Password must have at least 8 characters"
            })

        if password == confirmation:
            try:
                userData = User.objects.create_user(username, email, password)
                userData.save()
                return HttpResponseRedirect("login_user")

            except IntegrityError:
                return render(request, "video/register_user.html", {
                    "error": "Username already exist, please try other username "
                })

        else:
            return render(request, "video/register_user.html", {
                "error": "Password and confirmation doesn't match"
            })
    else:
        return render(request, "video/register_user.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        is_authenticated = authenticate(
            request, username=username, password=password)

        if is_authenticated is not None:
            login(request, is_authenticated)
            return HttpResponseRedirect("all_videos/1")
        else:
            return render(request, "video/login_user.html", {
                "error": "Username or/and password are invalid"
            })

    else:
        return render(request, "video/login_user.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login_user")


def add_video(request):
    if request.method == "POST":
        title = request.POST.get("title")
        mood = request.POST.get("mood")
        url = request.POST.get("video_url")

        date = datetime.now()

        if len(str(date.day)) == 1:
            day = f"0{date.day}"
        else:
            day = date.day

        if len(str(date.month)) == 1:
            month = f"0{date.month}"
        else:
            month = date.month

        if len(str(date.hour)) == 1:
            hour = f"0{date.hour}"
        else:
            hour = date.hour

        if len(str(date.minute)) == 1:
            minute = f"0{date.minute}"
        else:
            minute = date.minute

        if len(str(date.second)) == 1:
            second = f"0{date.second}"
        else:
            second = date.second

        date_now = f"{date.year}-{month}-{day} {hour}:{minute}:{second}"
        predefined_link = "https://drive.google.com/uc?export=download&id="
        requests_url = requests.get(url)
        content_type = requests_url.headers.get('Content-Type')
        is_video = content_type.startswith("video")

        if url.startswith(predefined_link) and len(url) > len(predefined_link) and is_video:
            if requests.get(url).status_code == 200:
                m = Video(title=title, posted_by=request.user.username,
                        mood=mood, video_link=url, date_and_time=date_now)
                m.save()
                return HttpResponseRedirect("all_videos/1")
            else:
                return render(request, "video/add_video.html", {
                    "error": "Url doesn't exist"
                })

        else:
            return render(request, "video/add_video.html", {
                "error": "Please provide a valid url"
            })

    else:
        return render(request, "video/add_video.html")


def all_videos(request, page):
    if request.method == "POST":
        search_title = request.POST.get("title")
        videos = Video.objects.all().filter(
            title__contains=search_title).order_by("date_and_time").reverse()
        page_videos = Paginator(videos, 8)
        each_page_video = page_videos.get_page(page)
        return render(request, "video/all_videos.html", {
            "videos": each_page_video
        })
    else:
        videos = Video.objects.all().order_by("date_and_time").reverse()
        page_videos = Paginator(videos, 8)
        each_page_video = page_videos.page(page)
        return render(request, "video/all_videos.html", {
            "videos": each_page_video
        })


@csrf_exempt
def add_comment(request, id):
    if request.method == "POST":
        content = json.loads(request.body)
        date = datetime.now()

        if len(str(date.day)) == 1:
            day = f"0{date.day}"
        else:
            day = date.day

        if len(str(date.month)) == 1:
            month = f"0{date.month}"
        else:
            month = date.month

        if len(str(date.hour)) == 1:
            hour = f"0{date.hour}"
        else:
            hour = date.hour

        if len(str(date.minute)) == 1:
            minute = f"0{date.minute}"
        else:
            minute = date.minute

        if len(str(date.second)) == 1:
            second = f"0{date.second}"
        else:
            second = date.second

        date_now = f"{date.year}-{month}-{day} {hour}:{minute}:{second}"
        comment = Comments(commenter=request.user.username, comment=content.get(
            "comment"), commented_video_id=id, date_and_time=date_now)
        comment.save()
        return HttpResponse("Sent")
    else:
        comments = Comments.objects.all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)


def getComments(request, id):
    comments = Comments.objects.filter(
        commented_video_id=id).order_by("date_and_time").reverse()
    return JsonResponse([comment.serialize() for comment in comments], safe=False)


def video(request, id):
    videoObj = Video.objects.filter(id=id)
    username = request.user.username
    return render(request, "video/video.html", {
        "videoObj": videoObj,
        "username": username
    })


@csrf_exempt
def getVideoLike(request, id):
    if request.method == "POST":

        body = json.loads(request.body)
        video_id = body.get("liked_video_id")

        l = Likes(liker=request.user.username, liked_video_id=video_id)
        l.save()
        return HttpResponse("Liked")

    elif request.method == "DELETE":

        body = json.loads(request.body)
        v_id = body.get("liked_video_id")
        l_del = Likes.objects.filter(
            liker=request.user.username, liked_video_id=v_id)
        l_del.delete()
        return HttpResponse("Deleted")

    else:
        likes = Likes.objects.filter(liked_video_id=id)
        return JsonResponse([like.serialize() for like in likes], safe=False)


def liked(request, page):
    videos = Video.objects.all()
    likes = Likes.objects.all()

    ids = []
    for like in likes:
        for video in videos:
            if like.liked_video_id == video.id and like.liker == request.user.username:
                ids.append(like.liked_video_id)

    liked_videos = Video.objects.filter(
        id__in=ids).order_by("date_and_time").reverse()

    page_videos = Paginator(liked_videos, 8)
    each_page_video = page_videos.page(page)

    return render(request, "video/liked.html", {
        "videos": each_page_video,
    })


def profile(request, page):
    likes = Likes.objects.filter(liker=request.user.username)
    videos = Video.objects.filter(
        posted_by=request.user.username).order_by("date_and_time").reverse()

    page_videos = Paginator(videos, 8)
    each_page_video = page_videos.page(page)

    return render(request, "video/profile.html", {
        "videos": each_page_video,
        "likes": likes
    })


def recommended(request):
    likes = Likes.objects.filter(liker=request.user.username)
    videos = Video.objects.all().order_by("date_and_time").reverse()

    favorites_title = []
    favorites_mood = []
    current_liked = []

    for like in likes:
        for video in videos:
            if like.liked_video_id == video.id:
                favorites_title.append(video.title)
                favorites_mood.append(video.mood)
                current_liked.append(video.id)

    fav_videos = Video.objects.filter(Q(title__in=favorites_title) | Q(mood__in=favorites_mood)).exclude(
        id__in=current_liked).exclude(posted_by=request.user.username).order_by("date_and_time").reverse()[0:8]
    return render(request, "video/recommended.html", {
        "fav_videos": fav_videos
    })


@csrf_exempt
def delete_video(request, id):
    video = Video.objects.get(id=id)
    if request.method == "DELETE":
        if video.posted_by == request.user.username:
            video_to_delete = Video.objects.filter(id=id)
            video_to_delete.delete()
            return HttpResponse("done")
        else:
            return HttpResponse("You are not allowed to delete the video, because you don't own the video")
    else:
        HttpResponse("The url is only for Delete request")

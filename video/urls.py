from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_user", views.register_user, name="register_user"),
    path("login_user", views.login_user, name="login_user"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("add_video", views.add_video, name="add_video"),
    path("all_videos/<int:page>", views.all_videos, name="all_videos"),
    path("video/<int:id>", views.video, name="video"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("getComments/<int:id>", views.getComments, name="getComments"),
    path("getVideoLike/<int:id>", views.getVideoLike, name="getVideoLike"),
    path("liked/<int:page>", views.liked, name="liked"),
    path("profile/<int:page>", views.profile, name="profile"),
    path("recommended", views.recommended, name="recommended"),
    path("delete_video/<int:id>", views.delete_video, name="delete_video")
]

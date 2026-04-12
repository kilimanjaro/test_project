from django.contrib import admin
from django.urls import path, include
from board import views as board_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", board_views.index, name="index"),
    path("board/", include("board.urls", namespace="board")),
]

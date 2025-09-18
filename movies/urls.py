from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="movies.index"),
    path("liked/", views.liked_movies, name="movies.liked"),
    path("<int:id>/", views.show, name="movies.show"),
    path("<int:id>/review/create/", views.create_review, name="movies.create_review"),
    path(
        "<int:id>/review/<int:review_id>/edit/",
        views.edit_review,
        name="movies.edit_review",
    ),
    path(
        "<int:id>/review/<int:review_id>/delete/",
        views.delete_review,
        name="movies.delete_review",
    ),
    path("<int:id>/like/", views.toggle_like, name="toggle_like"),
]


from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="movies.index"),
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
    path(
        "<int:id>/review/<int:review_id>/toggle_like/",
        views.toggle_like,
        name="movies.toggle_like",
    ),
    path("wishlist/", views.wishlist, name="movies.wishlist"),
    path(
        "<int:id>/add_to_wishlist/",
        views.add_to_wishlist,
        name="movies.add_to_wishlist",
    ),
    path(
        "<int:id>/remove_from_wishlist/",
        views.remove_from_wishlist,
        name="movies.remove_from_wishlist",
    ),
    path(
        "<int:id>/review/<int:review_id>/add_reply/",
        views.add_reply,
        name="movies.add_reply",
    ),
    path('liked/', views.liked_movies, name='movies.liked_movies'),
    path('<int:id>/like/', views.like_movie, name='movies.like_movie'),
    path('<int:id>/unlike/', views.unlike_movie, name='movies.unlike_movie'),
]

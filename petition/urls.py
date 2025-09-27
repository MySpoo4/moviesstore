from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="petition.index"),
    path("<int:id>/", views.show, name="petition.show"),
    path("create/", views.create, name="petition.create"),
    path("<int:id>/delete", views.delete, name="petition.delete"),
    path("<int:id>/vote", views.vote, name="petition.vote"),
]


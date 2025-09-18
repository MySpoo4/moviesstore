from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="accounts.signup"),
    path("login/", views.login, name="accounts.login"),
    path("logout/", views.logout, name="accounts.logout"),
    path("orders/", views.orders, name="accounts.orders"),
    path(
        "reset-password-security/",
        views.reset_password_security,
        name="accounts.reset_password_security",
    ),
    path("settings/", views.user_settings, name="accounts.user_settings"),
]

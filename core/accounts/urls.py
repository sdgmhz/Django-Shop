from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # Route to login view
    path("login/", views.LoginView.as_view(), name="login"),
    # Route to registration view
    path("register/", views.RegisterView.as_view(), name="register"),
    # Route to logout view
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # Route to password reset request view
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    # Route to password reset done confirmation view
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    # Route to password reset confirmation view using uid and token
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # Route to password reset complete view
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

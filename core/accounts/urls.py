from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
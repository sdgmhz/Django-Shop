from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    # Route to homepage
    path("", views.IndexView.as_view(), name="index"),
    # Route to contact page
    path("contact/", views.ContactView.as_view(), name="contact"),
    # Route to about page
    path("about/", views.AboutView.as_view(), name="about"),
]

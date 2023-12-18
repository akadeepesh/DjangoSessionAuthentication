from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chatBackend.urls")),
    path("tokenize/", views.tokenize, name="tokenize"),
    path("remove_stopwords/", views.remove_stopwords, name="remove_stopwords"),
    path("lemmatize/", views.lemmatize, name="lemmatize"),
]

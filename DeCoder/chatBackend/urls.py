from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login, tokenize, remove_stopwords, lemmatize

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", login, name="login"),
    path("tokenize/", tokenize, name="tokenize"),
    path("remove_stopwords/", remove_stopwords, name="remove_stopwords"),
    path("lemmatize/", lemmatize, name="lemmatize"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("user/", views.UserView.as_view(), name="user"),
    path("tokenize/", views.tokenize, name="tokenize"),
    path("remove_stopwords/", views.remove_stopwords, name="remove_stopwords"),
    path("lemmatize/", views.lemmatize, name="lemmatize"),
]

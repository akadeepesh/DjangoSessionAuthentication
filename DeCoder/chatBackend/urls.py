from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("user/", views.UserView.as_view(), name="user"),
    # path('register', views.UserRegister.as_view(), name='register'),
	# path('login', views.UserLogin.as_view(), name='login'),
	# path('logout', views.UserLogout.as_view(), name='logout'),
	# path('user', views.UserView.as_view(), name='user'),
    path("tokenize/", views.TokenizeSentence.as_view(), name="TokenizeSentence"),
    path("RemoveStopwords/", views.RemoveStopwords.as_view(), name="RemoveStopwords"),
    path('lemmatize/', views.LemmatizeWords.as_view(), name='Lemmatization'),
]

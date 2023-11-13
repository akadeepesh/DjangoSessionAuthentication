from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            "Invalid email or password", status=status.HTTP_401_UNAUTHORIZED
        )

    if user.password == password:
        return Response("Login successful", status=status.HTTP_200_OK)
    else:
        return Response(
            "Invalid email or password", status=status.HTTP_401_UNAUTHORIZED
        )


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def StopWords(request):
    nltk.download("stopwords")
    nltk.download("punkt")
    input_text = request.data.get("input_text")
    language = request.data.get("language")
    words = word_tokenize(input_text)
    stop_words = set(stopwords.words(language))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_text = " ".join(filtered_words)
    print(filtered_text)

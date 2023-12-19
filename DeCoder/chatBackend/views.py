from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


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


@csrf_exempt
def tokenize(request):
    if request.method == "POST":
        text = request.POST.get("text")
        tokenization_type = request.POST.get("type")
        if tokenization_type == "word":
            tokens = word_tokenize(text)
        elif tokenization_type == "sentence":
            tokens = sent_tokenize(text)
        else:
            tokens = []
        return JsonResponse({"tokens": tokens})
    else:
        return JsonResponse("tokens")


@csrf_exempt
def remove_stopwords(request):
    if request.method == "POST":
        text = request.POST.get("text")
        stop_words = set(stopwords.words("english"))
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in stop_words]
        return JsonResponse({"tokens": tokens})


@csrf_exempt
def lemmatize(request):
    if request.method == "POST":
        text = request.POST.get("text")
        tokens = word_tokenize(text)
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return JsonResponse({"tokens": tokens})

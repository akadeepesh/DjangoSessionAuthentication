from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"msg": "Registration Successful"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


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

from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
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


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")  # type: ignore
            password = serializer.data.get("password")  # type: ignore
            user = authenticate(email=email, password=password)
            if user is not None:
                return Response(
                    {"msg": "Login Successful"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or Password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )


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

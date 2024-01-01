from rest_framework.response import Response
from django.contrib.auth import authenticate,login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


#---------------------------------------------------------User Authentication-------------------------------------------------------#
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
                login(request, user)
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
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


#-----------------------------------------Tokenization - RemovingStopWords - Lemmenization ------------------------------------------#
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TokenizeSentence(APIView):
    def post(self, request):
        sentence = request.data.get('sentence')
        tokenized_sentence = word_tokenize(sentence)
        return Response({"tokenized_sentence": tokenized_sentence})

class RemoveStopwords(APIView):
    def post(self, request):
        sentence = request.data.get('sentence')
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return Response({"filtered_sentence": filtered_sentence})

class LemmatizeWords(APIView):
    def post(self, request):
        sentence = request.data.get('sentence')
        lemmatizer = WordNetLemmatizer()
        word_tokens = word_tokenize(sentence)
        lemmatized_words = [lemmatizer.lemmatize(w) for w in word_tokens]
        return Response({"lemmatized_words": lemmatized_words})
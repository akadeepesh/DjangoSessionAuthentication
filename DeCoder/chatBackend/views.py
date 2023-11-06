from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    # Perform authentication logic here, such as:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            "Invalid email or password", status=status.HTTP_401_UNAUTHORIZED
        )

    if user.password == password:
        # User authenticated successfully
        return Response("Login successful", status=status.HTTP_200_OK)
    else:
        return Response(
            "Invalid email or password", status=status.HTTP_401_UNAUTHORIZED
        )


def StopWords(request):
    input_text = request.data.get("input_text")
    language = request.data.get("language")
    # example_sent = """This is a sample sentence,
    #                 showing off the stop words filtration."""

    # stop_words = set(stopwords.words("english"))

    # word_tokens = word_tokenize(example_sent)
    # # converts the words in word_tokens to lower case and then checks whether
    # # they are present in stop_words or not
    # filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # # with no lower case conversion
    # filtered_sentence = []

    # for w in word_tokens:
    #     if w not in stop_words:
    #         filtered_sentence.append(w)

    # print(word_tokens)
    # print(filtered_sentence)

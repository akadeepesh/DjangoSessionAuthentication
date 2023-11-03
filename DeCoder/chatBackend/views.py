from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    print(email, password)
    user = authenticate(request, username=email, password=password)

    if user is None:
        print("User not found")
        return Response({"error": "Invalid login credentials"})

    return Response({"message": "Logged in successfully"})

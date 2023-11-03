from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from django.contrib.auth import authenticate
# from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @api_view(["POST"])
# def login(request):
#     email = request.data.get("email")
#     password = request.data.get("password")
#     print(email, password)
#     user = authenticate(request, username=email, password=password)

#     if user is None:
#         print("User not found")
#         return Response({"error": "Invalid login credentials"})

#     return Response({"message": "Logged in successfully"})


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

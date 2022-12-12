from datetime import datetime
import json
from rest_framework.viewsets import ModelViewSet

from timi.custom_methods import generate_username, IsAuthenticatedCustom
from .serializers import (
    CustomUser,
    LoginSerializer,
    RegisterSerializer,
    UpdateUserSerializer,
    UserSerializer,
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from timi.utils import encode_jwt
from rest_framework.response import Response

# Create your views here.


class LoginView(ModelViewSet):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ("post",)

    def create(self, request):
        request_data = self.serializer_class(data=request.data)
        request_data.is_valid(raise_exception=True)
        get_user = self.queryset.filter(email=request_data.validated_data.get("email"))
        user = None
        if len(get_user) > 0:
            user = authenticate(
                username=request_data.validated_data.get("email"),
                password=request_data.validated_data.get("password"),
            )

            if not user:
                return Response({"error": "Invalid credentials"})
            token = encode_jwt({"user_id": str(user.id)}, 1)
            user.last_login = datetime.now()
            user.save()

        return Response({"access": token})


class RegisterView(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = LoginView.queryset
    http_method_names = ("post",)

    def create(self, request, *args, **kwargs):

        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        check_user = self.queryset.filter(email=data.validated_data.get("email"))
        if len(check_user) > 0:
            raise Exception("user with email exists")
        username = generate_username(
            data.validated_data.get("first_name"), data.validated_data.get("last_name")
        )
        data.validated_data.update({"username": username})
        user = CustomUser.objects.create_user(**data.validated_data)
        if user:
            return Response({"success": "user created"})
        return Response({"errors": data.error_messages})


class UpdateUserView(ModelViewSet):
    queryset = LoginView.queryset
    http_method_names = ("post",)
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticatedCustom,)


class UserProfile(ModelViewSet):
    queryset = LoginView.queryset
    http_method_names = ("get",)
    permission_classes = (IsAuthenticatedCustom,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        result = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(result)
        return Response(serializer.data)

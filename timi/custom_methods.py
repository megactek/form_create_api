from rest_framework.permissions import BasePermission
from .utils import decode_jwt
from timi_app.models import CustomUser
import random


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, _):
        token = request.META.get("HTTP_AUTHORIZATION", None)

        if not token:
            return False

        user = decode_jwt(token)
        if not user:
            return False

        request.user = user
        return True


def generate_username(first_name, last_name):
    # Generate a username based on the user's name
    username = first_name[0] + last_name

    # Check if the username is already taken
    existing_usernames = CustomUser.objects.values_list("username", flat=True)
    if username in existing_usernames:
        # If the username is taken, add a random number to the end of it
        username = username + str(random.randint(1, 100))

    return username

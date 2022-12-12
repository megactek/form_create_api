import jwt
from datetime import datetime, timedelta
from django.conf import settings

from timi_app.models import CustomUser


def encode_jwt(payload, expiry):
    token = jwt.encode(
        {"exp": datetime.now() + timedelta(days=expiry), **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return token


def decode_jwt(request):
    if not request:
        return None
    token = request[7:]
    try:
        decode = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except:
        return None

    if decode:
        try:
            return CustomUser.objects.get(id=decode.get("user_id", None))
        except:
            return None

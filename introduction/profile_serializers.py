import logging

from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import FAANG, CF_user

logger = logging.getLogger(__name__)


def user_to_json(user):
    data = model_to_dict(user)
    logger.info("serialized user: %s", data)
    return data


def current_user_api(request):
    user = request.user
    payload = user.__dict__.copy()
    payload.pop("_state", None)
    return JsonResponse(payload)


def debug_request(request):
    return JsonResponse(
        {
            "headers": dict(request.headers),
            "cookies": request.COOKIES,
            "session": dict(request.session.items()),
        }
    )

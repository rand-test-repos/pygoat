import logging

from django.contrib.auth.decorators import login_required, staff_member_required
from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import CF_user

logger = logging.getLogger(__name__)


# Keep profile serialization separate from the model's internal fields.  In
# particular, password fields must never be included in this response.
PROFILE_FIELDS = {
    CF_user: ("username",),
}
DEFAULT_PROFILE_FIELDS = ("username", "first_name", "last_name", "email")


def user_to_json(user):
    fields = PROFILE_FIELDS.get(type(user), DEFAULT_PROFILE_FIELDS)
    data = model_to_dict(user, fields=fields)
    logger.info("serialized user profile")
    return data


@login_required
def current_user_api(request):
    return JsonResponse(user_to_json(request.user))


@staff_member_required
def debug_request(request):
    return JsonResponse(
        {
            "method": request.method,
            "path": request.path,
            "is_secure": request.is_secure(),
            "authenticated": request.user.is_authenticated,
        }
    )

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .models import UserStatus
from .settings import graphql_auth_settings as app_settings


UserModel = get_user_model()


def get_user_by_email(email):
    """
    Get user by email or by secondary email (case-insensitive).
    Raise ObjectDoesNotExist if not found.
    """
    try:
        lookup = f"{UserModel.EMAIL_FIELD}__iexact"
        user = UserModel._default_manager.get(**{lookup: email})
        return user
    except ObjectDoesNotExist:
        status = UserStatus._default_manager.get(secondary_email__iexact=email)
        return status.user


def get_user_to_login(**kwargs):
    """
    Get user by kwargs or secondary email (case-insensitive) to perform login.
    Raise ObjectDoesNotExist if not found.
    """
    email_field = UserModel.EMAIL_FIELD
    email = kwargs.get(email_field)

    try:
        if email:
            return UserModel._default_manager.get(**{f"{email_field}__iexact": email})
        return UserModel._default_manager.get(**kwargs)
    except ObjectDoesNotExist:
        if app_settings.ALLOW_LOGIN_WITH_SECONDARY_EMAIL and email:
            status = UserStatus._default_manager.get(secondary_email__iexact=email)
            return status.user
        raise

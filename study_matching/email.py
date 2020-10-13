from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings
from django.conf import settings as django_settings


class ActivationEmail(BaseEmailMessage):
    template_name = "custom_email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["scheme"] = django_settings.URL_PROTOCOL
        print(context["scheme"])
        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = "custom_email/confirmation.html"


class PasswordResetEmail(BaseEmailMessage):
    template_name = "custom_email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["protocol"] = django_settings.URL_PROTOCOL
        return context


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "custom_email/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(BaseEmailMessage):
    template_name = "custom_email/username_changed_confirmation.html"


class UsernameResetEmail(BaseEmailMessage):
    template_name = "custom_email/username_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
        return context
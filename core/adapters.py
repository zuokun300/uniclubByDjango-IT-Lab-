from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


class DomainRestrictedSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)

        allowed_domains = getattr(settings, "SOCIAL_ALLOWED_EMAIL_DOMAINS", [])
        if not allowed_domains:
            return

        email = (sociallogin.user.email or "").strip().lower()
        domain = email.split("@")[-1] if "@" in email else ""

        if domain not in allowed_domains:
            messages.error(request, "Your email domain is not allowed for social sign in.")
            raise ImmediateHttpResponse(redirect("login"))

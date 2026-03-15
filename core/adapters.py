from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


class DomainRestrictedSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)

        allowed_domains = getattr(settings, "SOCIAL_ALLOWED_EMAIL_DOMAINS", [])
        restricted_providers = {
            provider.lower()
            for provider in getattr(settings, "SOCIAL_DOMAIN_RESTRICTED_PROVIDERS", [])
        }
        provider = getattr(getattr(sociallogin, "account", None), "provider", "").lower()

        if not allowed_domains or provider not in restricted_providers:
            return

        email = (sociallogin.user.email or "").strip().lower()
        domain = email.split("@")[-1] if "@" in email else ""

        if domain not in allowed_domains:
            messages.error(request, "Please use your University of Glasgow email account.")
            raise ImmediateHttpResponse(redirect("login"))

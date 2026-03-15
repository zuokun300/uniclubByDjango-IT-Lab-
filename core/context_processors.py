from django.conf import settings


def social_auth_context(request):
    return {
        "google_login_enabled": getattr(settings, "GOOGLE_OAUTH_ENABLED", False),
        "social_allowed_email_domains": getattr(settings, "SOCIAL_ALLOWED_EMAIL_DOMAINS", []),
    }

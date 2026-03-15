from datetime import timedelta
from types import SimpleNamespace

from allauth.exceptions import ImmediateHttpResponse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from .adapters import DomainRestrictedSocialAccountAdapter
from .models import Club, Comment, Event, Membership, Registration


class ClubModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tester", password="pass12345")

    def test_get_absolute_url_points_to_detail_page(self):
        club = Club.objects.create(
            club_name="Chess Society",
            description="Board games and tournaments",
            founded_by=self.user,
        )
        self.assertEqual(club.get_absolute_url(), reverse("club_detail", args=[club.pk]))


class MembershipViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="member", password="pass12345")
        self.club = Club.objects.create(
            club_name="Robotics Club",
            description="Robotics workshops",
            founded_by=self.user,
        )

    def test_join_club_requires_authentication(self):
        response = self.client.post(reverse("join_club", args=[self.club.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_join_club_creates_membership(self):
        self.client.login(username="member", password="pass12345")
        self.client.post(reverse("join_club", args=[self.club.pk]))
        self.assertTrue(Membership.objects.filter(club=self.club, user=self.user).exists())

    def test_club_list_shows_join_button_for_non_members(self):
        outsider = get_user_model().objects.create_user(username="outsider", password="pass12345")
        self.client.login(username="outsider", password="pass12345")
        response = self.client.get(reverse("club_list"))
        self.assertContains(response, reverse("join_club", args=[self.club.pk]))


class AuthenticationTests(TestCase):
    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newmember",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(username="newmember").exists())
        self.assertTrue(response.context["user"].is_authenticated)

    def test_register_accepts_simple_eight_character_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "simpledemo",
                "password1": "12345678",
                "password2": "12345678",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(username="simpledemo").exists())

    def test_home_shows_register_link_for_guests(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("register"))

    @override_settings(GOOGLE_OAUTH_ENABLED=True, MICROSOFT_OAUTH_ENABLED=True)
    def test_login_page_shows_google_and_uofg_sign_in_when_configured(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "Continue with Google")
        self.assertContains(response, "Continue with University of Glasgow email")

    @override_settings(GOOGLE_OAUTH_ENABLED=False, MICROSOFT_OAUTH_ENABLED=False)
    def test_login_page_shows_setup_message_when_social_sign_in_is_not_configured(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "Social sign-in will appear here after OAuth credentials are configured.")


class SocialAccountAdapterTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def build_request(self):
        request = self.factory.get(reverse("login"))
        SessionMiddleware(lambda req: None).process_request(request)
        request.session.save()
        setattr(request, "_messages", FallbackStorage(request))
        return request

    @override_settings(
        SOCIAL_ALLOWED_EMAIL_DOMAINS=["glasgow.ac.uk", "student.gla.ac.uk"],
        SOCIAL_DOMAIN_RESTRICTED_PROVIDERS=["microsoft"],
    )
    def test_adapter_allows_university_of_glasgow_domain_for_microsoft_login(self):
        request = self.build_request()
        sociallogin = SimpleNamespace(
            user=SimpleNamespace(email="student@student.gla.ac.uk"),
            account=SimpleNamespace(provider="microsoft"),
        )

        DomainRestrictedSocialAccountAdapter(request).pre_social_login(request, sociallogin)

    @override_settings(
        SOCIAL_ALLOWED_EMAIL_DOMAINS=["glasgow.ac.uk", "student.gla.ac.uk"],
        SOCIAL_DOMAIN_RESTRICTED_PROVIDERS=["microsoft"],
    )
    def test_adapter_rejects_non_uofg_domain_for_microsoft_login(self):
        request = self.build_request()
        sociallogin = SimpleNamespace(
            user=SimpleNamespace(email="user@example.com"),
            account=SimpleNamespace(provider="microsoft"),
        )

        with self.assertRaises(ImmediateHttpResponse):
            DomainRestrictedSocialAccountAdapter(request).pre_social_login(request, sociallogin)

    @override_settings(
        SOCIAL_ALLOWED_EMAIL_DOMAINS=["glasgow.ac.uk", "student.gla.ac.uk"],
        SOCIAL_DOMAIN_RESTRICTED_PROVIDERS=["microsoft"],
    )
    def test_adapter_does_not_restrict_google_login(self):
        request = self.build_request()
        sociallogin = SimpleNamespace(
            user=SimpleNamespace(email="person@gmail.com"),
            account=SimpleNamespace(provider="google"),
        )

        DomainRestrictedSocialAccountAdapter(request).pre_social_login(request, sociallogin)


class EventInteractionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="participant", password="pass12345")
        self.other_user = get_user_model().objects.create_user(
            username="visitor", password="pass12345"
        )
        self.club = Club.objects.create(
            club_name="Film Club",
            description="Weekly screenings",
            founded_by=self.user,
        )
        self.event = Event.objects.create(
            event_name="Screening Night",
            description="Independent film showcase",
            event_date=timezone.now() + timedelta(days=3),
            location="Room A",
            club=self.club,
            created_by=self.user,
        )

    def test_register_event_ajax_returns_json(self):
        self.client.login(username="participant", password="pass12345")
        response = self.client.post(
            reverse("register_event", args=[self.event.pk]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Registration.objects.filter(event=self.event, user=self.user).exists())
        self.assertEqual(response.json()["event"], "Screening Night")

    def test_club_detail_hides_register_button_for_confirmed_registration(self):
        Registration.objects.create(
            event=self.event,
            user=self.user,
            status=Registration.STATUS_CONFIRMED,
        )
        self.client.login(username="participant", password="pass12345")
        response = self.client.get(reverse("club_detail", args=[self.club.pk]))
        self.assertContains(response, "Registered for Screening Night.")
        self.assertNotContains(response, "Register instantly")

    def test_club_detail_shows_register_again_for_cancelled_registration(self):
        Registration.objects.create(
            event=self.event,
            user=self.user,
            status=Registration.STATUS_CANCELLED,
        )
        self.client.login(username="participant", password="pass12345")
        response = self.client.get(reverse("club_detail", args=[self.club.pk]))
        self.assertContains(response, "Register again")
        self.assertContains(response, "Registration cancelled. You can register again.")

    def test_club_detail_confirmed_count_excludes_cancelled_registrations(self):
        Registration.objects.create(
            event=self.event,
            user=self.user,
            status=Registration.STATUS_CONFIRMED,
        )
        Registration.objects.create(
            event=self.event,
            user=self.other_user,
            status=Registration.STATUS_CANCELLED,
        )
        response = self.client.get(reverse("club_detail", args=[self.club.pk]))
        self.assertContains(response, "<span data-registration-count>1</span>", html=True)

    def test_add_comment_ajax_creates_comment(self):
        self.client.login(username="participant", password="pass12345")
        response = self.client.post(
            reverse("add_comment", args=[self.event.pk]),
            {"content": "Looking forward to it"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(event=self.event, user=self.user).exists())
        self.assertEqual(response.json()["author"], "participant")

    def test_anonymous_user_is_redirected_from_event_create_page(self):
        response = self.client.get(reverse("event_create", args=[self.club.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_anonymous_user_is_redirected_from_event_update_page(self):
        response = self.client.get(reverse("event_update", args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_anonymous_user_is_redirected_from_event_delete_page(self):
        response = self.client.get(reverse("event_delete", args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_only_club_founder_can_access_event_create_page(self):
        self.client.login(username="visitor", password="pass12345")
        response = self.client.get(reverse("event_create", args=[self.club.pk]))
        self.assertEqual(response.status_code, 403)

    def test_only_club_founder_can_access_event_update_page(self):
        self.client.login(username="visitor", password="pass12345")
        response = self.client.get(reverse("event_update", args=[self.event.pk]))
        self.assertEqual(response.status_code, 403)

    def test_club_founder_can_update_event(self):
        self.client.login(username="participant", password="pass12345")
        response = self.client.post(
            reverse("event_update", args=[self.event.pk]),
            {
                "event_name": "Updated Screening Night",
                "description": self.event.description,
                "event_date": self.event.event_date.strftime("%Y-%m-%dT%H:%M"),
                "location": self.event.location,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(self.event.event_name, "Updated Screening Night")

    def test_club_founder_can_delete_event(self):
        self.client.login(username="participant", password="pass12345")
        response = self.client.post(reverse("event_delete", args=[self.event.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())


class RegistrationManagementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="member2", password="pass12345")
        self.other_user = get_user_model().objects.create_user(username="other2", password="pass12345")
        self.club = Club.objects.create(
            club_name="Debate Club",
            description="Weekly debates",
            founded_by=self.user,
        )
        self.event = Event.objects.create(
            event_name="Debate Session",
            description="Open discussion",
            event_date=timezone.now() + timedelta(days=5),
            location="Hall B",
            club=self.club,
            created_by=self.user,
        )
        self.registration = Registration.objects.create(
            event=self.event,
            user=self.user,
            status=Registration.STATUS_CONFIRMED,
        )

    def test_my_registrations_requires_login(self):
        response = self.client.get(reverse("my_registrations"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_my_registrations_lists_current_user_records(self):
        Registration.objects.create(
            event=self.event,
            user=self.other_user,
            status=Registration.STATUS_CONFIRMED,
        )
        self.client.login(username="member2", password="pass12345")
        response = self.client.get(reverse("my_registrations"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Debate Session")

    def test_cancel_registration_updates_status(self):
        self.client.login(username="member2", password="pass12345")
        response = self.client.post(reverse("cancel_registration", args=[self.registration.pk]))
        self.assertEqual(response.status_code, 302)
        self.registration.refresh_from_db()
        self.assertEqual(self.registration.status, Registration.STATUS_CANCELLED)

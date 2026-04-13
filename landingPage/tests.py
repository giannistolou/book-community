from unittest.mock import MagicMock, patch

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from .forms import SubscribeForm
from .views import bio, index, newsletter, subscribe, thank_you_subscribe


def _attach_messages(request):
    """Attach a FallbackStorage to a request so views can use messages."""
    setattr(request, "session", {})
    setattr(request, "_messages", FallbackStorage(request))


# ---------------------------------------------------------------------------
# Form Tests
# ---------------------------------------------------------------------------


class SubscribeFormTests(TestCase):
    def test_valid_email(self):
        form = SubscribeForm(data={"email": "user@example.com", "honeypot": ""})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = SubscribeForm(data={"email": "not-an-email", "honeypot": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_email(self):
        form = SubscribeForm(data={"honeypot": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_honeypot_not_required(self):
        form = SubscribeForm(data={"email": "user@example.com"})
        self.assertTrue(form.is_valid())

    def test_cleaned_data_email(self):
        form = SubscribeForm(data={"email": "user@example.com", "honeypot": ""})
        form.is_valid()
        self.assertEqual(form.cleaned_data["email"], "user@example.com")


# ---------------------------------------------------------------------------
# Simple View Tests
# ---------------------------------------------------------------------------


class LandingPageViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_returns_200(self):
        request = self.factory.get("/")
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_bio_returns_200(self):
        request = self.factory.get("/bio/")
        response = bio(request)
        self.assertEqual(response.status_code, 200)

    def test_thank_you_subscribe_returns_200(self):
        request = self.factory.get("/thank-you-subscribe/")
        response = thank_you_subscribe(request)
        self.assertEqual(response.status_code, 200)

    def test_newsletter_returns_200(self):
        request = self.factory.get("/newsletter/")
        response = newsletter(request)
        self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# Subscribe View Tests
# ---------------------------------------------------------------------------


class SubscribeViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_request_renders_form(self):
        request = self.factory.get("/newsletter-subscribe/")
        _attach_messages(request)
        response = subscribe(request)
        self.assertEqual(response.status_code, 200)

    def test_post_with_invalid_email_returns_form_with_errors(self):
        request = self.factory.post(
            "/newsletter-subscribe/",
            {"email": "bad-email", "honeypot": ""},
        )
        _attach_messages(request)
        response = subscribe(request)
        self.assertEqual(response.status_code, 200)

    @patch("requests.post")
    def test_post_captcha_failure_returns_form(self, mock_post):
        mock_post.return_value.json.return_value = {"success": False}
        request = self.factory.post(
            "/newsletter-subscribe/",
            {
                "email": "user@example.com",
                "honeypot": "",
                "cf-turnstile-response": "bad-token",
            },
        )
        _attach_messages(request)
        response = subscribe(request)
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once()

    @patch("landingPage.views.resend.Contacts.create")
    @patch("requests.post")
    def test_post_valid_redirects_to_thank_you(self, mock_post, mock_resend):
        mock_post.return_value.json.return_value = {"success": True}
        mock_resend.return_value = MagicMock()
        request = self.factory.post(
            "/newsletter-subscribe/",
            {
                "email": "user@example.com",
                "honeypot": "",
                "cf-turnstile-response": "valid-token",
            },
        )
        _attach_messages(request)
        response = subscribe(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn("thank-you-subscribe", response["Location"])

    @patch("landingPage.views.resend.Contacts.create")
    @patch("requests.post")
    def test_post_resend_exception_returns_form_with_error(
        self, mock_post, mock_resend
    ):
        mock_post.return_value.json.return_value = {"success": True}
        mock_resend.side_effect = Exception("API error")
        request = self.factory.post(
            "/newsletter-subscribe/",
            {
                "email": "user@example.com",
                "honeypot": "",
                "cf-turnstile-response": "valid-token",
            },
        )
        _attach_messages(request)
        response = subscribe(request)
        self.assertEqual(response.status_code, 200)

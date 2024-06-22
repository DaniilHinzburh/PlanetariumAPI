from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow as Show, ShowTheme
from planetarium.serializers import AstronomyShowListSerializer, AstronomyShowRetrieveSerializer

SHOW_URL = reverse("planetarium:astronomyshow-list")


def sample_show(**params):
    defaults = {
        "title": "test_show",
        "description": "test_show",
    }
    defaults.update(params)
    return Show.objects.create(**defaults)


def default_url(show_id):
    return reverse("planetarium:astronomyshow-detail", args=[show_id])


class UnauthenticatedShowTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(SHOW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com", password="test"
        )
        self.client.force_authenticate(self.user)

    def test_show_list(self):
        sample_show()
        response = self.client.get(SHOW_URL)
        shows = Show.objects.all()
        serializer = AstronomyShowListSerializer(shows, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_shows_by_theme(self):
        show_without_theme = sample_show(title="title_0")
        show_with_theme_1 = sample_show(title="title_1")
        show_with_theme_2 = sample_show(title="title_2")

        theme_1 = ShowTheme.objects.create(name="theme_1")
        theme_2 = ShowTheme.objects.create(name="theme_2")

        show_with_theme_1.show_themes.add(theme_1)
        show_with_theme_2.show_themes.add(theme_2)

        response = self.client.get(SHOW_URL, {"show_themes": f"{theme_1.id},{theme_2.id}"})

        serializer_without_themes = AstronomyShowListSerializer(show_without_theme)
        serializer_with_theme1 = AstronomyShowListSerializer(show_with_theme_1)
        serializer_with_theme2 = AstronomyShowListSerializer(show_with_theme_2)

        self.assertIn(serializer_with_theme1.data, response.data)
        self.assertIn(serializer_with_theme2.data, response.data)
        self.assertNotIn(serializer_without_themes, response.data)

    def test_retrieve_show_detail(self):
        show = sample_show()
        show.show_themes.add(ShowTheme.objects.create(name="theme_1"))

        url = default_url(show.id)
        response = self.client.get(url)
        serializer = AstronomyShowRetrieveSerializer(show)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_show_forbidden(self):
        payload = {
            "title": "test title",
            "description": "test description"
        }
        response = self.client.post(SHOW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com", password="admin", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_show_with_theme_admin(self):
        theme_1 = ShowTheme.objects.create(name="theme_1")
        theme_2 = ShowTheme.objects.create(name="theme_2")

        payload = {
            "title": "test title",
            "description": "test description",
            "show_themes": [theme_1.id, theme_2.id]
        }
        response = self.client.post(SHOW_URL, payload)

        show = Show.objects.get(id=response.data["id"])
        themes = show.show_themes.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(theme_1, themes)
        self.assertIn(theme_2, themes)
        self.assertEqual(themes.count(), 2)

    def test_create_show_admin(self):
        payload = {
            "title": "test title",
            "description": "test description",
        }
        response = self.client.post(SHOW_URL, payload)
        print(response)
        show = Show.objects.get(id=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(show, key))

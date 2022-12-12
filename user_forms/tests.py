import json
from timi_app.models import CustomUser
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status


class FormTestCase(APITestCase):
    def setUp(self):
        self.email = "test@user.com"
        self.password = "123"
        # create user
        test_user = CustomUser.objects.create_user(
            email="test@user.com", password="123"
        )
        #
        self.test_user = test_user
        self.client = APIClient()
        login = reverse("user:login-list")

        # login user
        resp = self.client.post(
            login, {"email": self.email, "password": self.password}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        self.token = resp.data["access"]
        self.auth = "Bearer {0}".format(self.token)

    def test_userForms(self):
        #  Forms url
        url = reverse("app:forms-list")

        # Test for user forms is a list of forms
        request = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        forms = request.data.get("forms")
        self.assertIsInstance(forms, list)
        self.assertEqual(request.status_code, 200)

        # Test form create confirm form name is correct
        request = self.client.post(
            url,
            data={
                "name": "New form",
            },
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )
        new_form_name = request.data.get("name")
        self.assertEqual(request.status_code, 201)
        self.assertEqual(new_form_name, "New form")

        # Check added form has correct name
        request = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        forms = request.data.get("forms")
        self.assertIsInstance(forms, list)
        first_form = forms[0].get("name")
        self.assertEqual(first_form, "New form")
        self.assertEqual(request.status_code, 200)

        # test add input success
        input_data = {"label": "First Name", "input_type": "input"}
        form_id = forms[0].get("id")
        request = self.client.post(
            f"/api/app/forms/{form_id}/add_input/",
            data=input_data,
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )
        # validate added input
        self.assertIn("input added", json.dumps(request.data))

        # test user response to form
        response_data = {
            "response": {
                "First Name": "Engineering English two",
            }
        }
        request = self.client.post(
            f"/api/app/forms/{form_id}/submit_response/",
            data=response_data,
            HTTP_AUTHORIZATION=self.auth,
            format="json",
        )
        # Validate user response to form
        resp_test = request.data.get("response")
        self.assertEqual(resp_test["First Name"], "Engineering English two")
        self.assertEqual(request.status_code, 200)

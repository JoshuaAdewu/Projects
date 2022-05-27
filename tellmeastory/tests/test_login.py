from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User

COOKIE_NAME: str = "StoryUserLoggedIn"

hash_pw = lambda pw: sha512(pw.encode("utf-8")).hexdigest()
def insert_registered_user(username: str, password: str) -> User:
    return User.objects.create(
        username=username,
        password=hash_pw(password),
        display_name=username
    )

class UserLoginViewTests(TestCase):
    def test_blank_login_page(self) -> None:
        """
        Base login page should have no error messages present.
        The user should not have a cookie here.
        """
        res: HttpResponse = self.client.get("/story/login/")
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "No account with that username.")
        self.assertNotContains(res, "Incorrect password.")
        self.assertEqual(res.wsgi_request.COOKIES.get(COOKIE_NAME), None)

        return

    def test_login_all_fields(self) -> None:
        """
        Successful login should give the user some kind of session token.
        The user should be redirected to /story/account/<their_username>/.
        """
        # insert an existing user into the db to retrieve
        inp_name: str = "BenJohnson"
        inp_pass: str = "#1Aaaaa"
        johnson: User = insert_registered_user(inp_name, inp_pass)

        # refer to views.login @ line 35 for why this is terrible :(
        res: HttpResponse = self.client.post("/story/login/", data={
            "username": inp_name,
            "password": inp_pass
        })

        # HTTP 302 -> Redirect (Found)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get("location"), f"/story/account/{inp_name}")

        # check to make sure we now have a cookie
        idx_res: HttpResponse = self.client.get("/story/")
        self.assertEqual(idx_res.wsgi_request.COOKIES.get(COOKIE_NAME), inp_name)

        return

    def test_login_bad_username(self) -> None:
        """
        Failure to login based on username should keep the user at /story/login/.
        An error message should be present, "No account with that username."
        The user should have no session token.
        """
        # we can just not make a user account for this :)
        inp_name: str = "Berczynski"
        inp_pass: str = "AHHHHHH"

        # refer to views.login @ line 35 for why this is terrible :(
        res: HttpResponse = self.client.post("/story/login/", data={
            "username": inp_name,
            "password": inp_pass
        })

        # HTTP 200 indicates no redirect
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "No account with that username.")

        # check to make sure we do not have a cookie
        idx_res: HttpResponse = self.client.get("/story/")
        self.assertEqual(idx_res.wsgi_request.COOKIES.get(COOKIE_NAME), None)

        return

    def test_login_bad_password(self) -> None:
        """
        Failure to login based on password should keep the user at /story/login/.
        An error message should be present, "Incorrect password."
        The user should have no session token.
        """
        inp_name: str = "Berczynski"
        inp_pass: str = "AHHHHHH"
        bad_pass: str = "sjlhf"
        mark: User = insert_registered_user(inp_name, inp_pass)

        # refer to views.login @ line 35 for why this is terrible :(
        res: HttpResponse = self.client.post("/story/login/", data={
            "username": inp_name,
            "password": bad_pass
        })

        # HTTP 200 indicates no redirect
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Incorrect password.")

        # check to make sure we do not have a cookie
        idx_res: HttpResponse = self.client.get("/story/")
        self.assertEqual(idx_res.wsgi_request.COOKIES.get(COOKIE_NAME), None)

        return

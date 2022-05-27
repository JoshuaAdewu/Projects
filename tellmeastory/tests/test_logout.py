from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User, Node
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def insertUser(usern: str , pw: str , dname: str) -> User:
    return User.objects.create(
        username=usern ,
        password=sha512(pw.encode("utf-8")).hexdigest() ,
        display_name=dname ,
    )

URL_PROFILE = "/profile/"
TEST_ACCOUNT = "tellme1"


class UserLogoutViewTests(TestCase):

    def test_profile_page_logout(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        userDB = User.objects.get(username=uName)
        userID = userDB.id

        self.client.cookies['StoryUserLoggedIn'] = uName
        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks that it loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks that the user cookie exists for logged in
        self.assertEqual(res.wsgi_request.COOKIES.get("StoryUserLoggedIn"), uName)

        # Checks to make sure that the user is logged in properly and has the option to logout
        self.assertContains(res , "Log Out")

        # Checks to make sure that the login and register options are now available after redirecting to profile page
        res2: HttpResponse = self.client.get("/story/logout/")
        res2: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")

        # Checks that we removed association of the user cookie
        self.assertEqual(res2.wsgi_request.COOKIES.get("StoryUserLoggedIn"), '')

        # Checks that login and register are still showing
        self.assertContains(res2, "Login")
        self.assertContains(res2, "Register")

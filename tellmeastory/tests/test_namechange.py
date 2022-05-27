from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User

USERNAME: str = "hrrrrrngh"
DISPLAY_NAME: str = "olddname"
ACC_URL: str = f"/story/account/{USERNAME}/"
COOKIE_NAME: str = "StoryUserLoggedIn"

hash_pw = lambda pw: sha512(pw.encode("utf-8")).hexdigest()
def insert_registered_user(username: str, password: str, dname: str) -> User:
    return User.objects.create(
        username=username,
        password=hash_pw(password),
        display_name=dname
    )

class UserNameChangeViewTests(TestCase):
    def setUp(self):
        insert_registered_user(USERNAME, "cringe", DISPLAY_NAME)
        return

    def test_blank_account_page_with_cookie(self) -> None:
        """
        The base account page for these tests should include
        the user's username, and their current display name.
        With a cookie, a form should be present that allows the user
        to change their display name.
        """

        self.client.cookies[COOKIE_NAME] = USERNAME
        res: HttpResponse = self.client.get(ACC_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, DISPLAY_NAME)
        self.assertNotContains(res, "Successfully changed")
        self.assertNotContains(res, "Failed to change")
        self.assertContains(res, "New display name")

        return

    def test_blank_account_page_no_cookie(self) -> None:
        """
        The base account page for these tests should include
        the user's username, and their current display name.
        Without a cookie, no form prompting the user to change
        their display name should be present.
        """
        self.client.cookies[COOKIE_NAME] = USERNAME
        res: HttpResponse = self.client.get(ACC_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, DISPLAY_NAME)
        self.assertNotContains(res, "Successfully changed")
        self.assertNotContains(res, "Failed to change")
        self.assertNotContains(res, "Change your display name")

        return

    def test_valid_new_display_name(self) -> None:
        """
        Changing the user's display name to a valid name
        should keep them on their account page, and update their User
        Model in the database.
        The page should also display their new display name.
        Lastly, "Successfully changed display name." should be present.
        """
        self.client.cookies[COOKIE_NAME] = USERNAME

        new_dname: str = "new d name"
        res: HttpResponse = self.client.post(ACC_URL, data={
            "new_display_name": new_dname
        })

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Successfully changed display name.")
        self.assertNotContains(res, "Failed to change display name.")

        # user should be updated
        user: User = None
        try: user = User.objects.get(username=USERNAME)
        except: pass

        self.assertNotEqual(user, None)
        self.assertEqual(user.display_name, new_dname)

        return

    def test_invalid_new_display_name(self) -> None:
        """
        Changing the user's display name to an invalid name
        should keep them on their account page and NOT update their User
        Model in the database.
        The page should display their old display name.
        The page should also display "Failed to change display name."
        """
        self.client.cookies[COOKIE_NAME] = USERNAME

        new_dname: str = "this is wayyy too long hahahahahaha"
        res: HttpResponse = self.client.post(ACC_URL, data={
            "new_display_name": new_dname
        })

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Successfully changed display name.")
        self.assertContains(res, "Failed to change display name.")
        self.assertContains(res, DISPLAY_NAME)

        # user should not be updated
        user: User = None
        try: user = User.objects.get(username=USERNAME)
        except: pass

        self.assertNotEqual(user, None)
        self.assertEqual(user.display_name, DISPLAY_NAME)

        return

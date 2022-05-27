from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User

URL_ACCOUNT = "/account/"
TEST_ACCOUNT = "tellme18"
COOKIE_NAME: str = "StoryUserLoggedIn"

def insertUser(usern: str , pw: str , dname: str) -> User:
    return User.objects.create(
        username=usern ,
        password=sha512(pw.encode("utf-8")).hexdigest() ,
        display_name=dname ,
    )


class userBlurbTests(TestCase):

    # Tests to make sure Login and Register are displayed on the navbar.
    def test_login_account(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testaccount"
        dName = "Bob Tester"

        insertUser(uName , pw , dName)

    # Tests to make sure that no message is displayed if no changes are made
    def test_no_changes(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testaccount"
        dName = "Bob Tester"
        testUserBlurb = ""

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })

        res: HttpResponse = self.client.get("/story/account/" + TEST_ACCOUNT + "/")

        # Checks to make sure a success message is not displayed
        self.assertNotContains(res , "alert alert-success")

        # Checks to make sure an error message is not displayed
        self.assertNotContains(res , "alert alert-danger")

    # Tests to make sure that an error message is displayed for an invalid display name
    # and that there is no message related to a user blurb change.

    def test_only_change_displayname_inval(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testaccount"
        dName = "Bob Tester"
        testUserBlurb = ""

        insertUser(uName , pw , dName)


        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })


        # Checks to make sure we logged in correctly and were redirected
        self.assertEqual(resLogin.status_code , 302)

        res: HttpResponse = self.client.post("/story/account/" + TEST_ACCOUNT + "/" , data={
            "new_display_name": "Inv",
            "edit_blurb": testUserBlurb
        })

        # Checks to make sure an error message is displayed
        self.assertContains(res , "alert alert-danger")

        # Checks to make sure a message about invalid display name is displayed
        self.assertContains(res , "Failed to change display name.")

        # Checks to make sure a message about changing blurb is not displayed
        self.assertNotContains(res , "Successfully changed user blurb.")

    # Tests to make sure that an error message is displayed for an invalid display name
    # with a valid blurb change
    def test_invaldisplay_validblurb(self)->None:
        uName = TEST_ACCOUNT
        pw = "testaccount"
        dName = "Bob Tester"
        testUserBlurb = "This is my new blurb."

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })


        # Checks to make sure we logged in correctly and were redirected
        self.assertEqual(resLogin.status_code , 302)

        res: HttpResponse = self.client.post("/story/account/" + TEST_ACCOUNT + "/" , data={
            "new_display_name": "Inv" ,
            "edit_blurb": testUserBlurb
        })

        # Checks to make sure an error message is displayed
        self.assertContains(res , "alert alert-danger")

        # Checks to make sure a message about invalid display name is displayed
        self.assertContains(res , "Failed to change display name.")

        # Checks to make sure a message about changing blurb is displayed
        self.assertContains(res , "Successfully changed user blurb.")

    # Tests to make sure that a success message is displayed for a valid display name change
    # with a valid blurb change
    def test_valdisplay_validblurb(self)->None:
        uName = TEST_ACCOUNT
        pw = "testaccount"
        dName = "Bob Tester"
        testUserBlurb = "This is my new blurb."

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })


        # Checks to make sure we logged in correctly and were redirected
        self.assertEqual(resLogin.status_code , 302)

        res: HttpResponse = self.client.post("/story/account/" + TEST_ACCOUNT + "/" , data={
            "new_display_name": "Bill Tester" ,
            "edit_blurb": testUserBlurb
        })

        # Checks to make sure an error message is displayed
        self.assertContains(res , "alert alert-success")

        # Checks to make sure a message about invalid display name is displayed
        self.assertContains(res , "Successfully changed display name.")

        # Checks to make sure a message about changing blurb is displayed
        self.assertContains(res , "Successfully changed user blurb.")

    # Tests to make sure that a success message is displayed for a valid display name change
    # with no blurb change
    def test_valdisplay_noblurbchange(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testaccount"
        dName = "Bob Tester"
        testUserBlurb = ""

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })

        self.client.cookies[COOKIE_NAME] = uName

        # Checks to make sure we logged in correctly and were redirected
        self.assertEqual(resLogin.status_code , 302)

        res: HttpResponse = self.client.post("/story/account/" + TEST_ACCOUNT + "/" , data={
            "new_display_name": "Bill Tester" ,
            "edit_blurb": testUserBlurb
        })


        # Checks to make sure an error message is displayed
        self.assertContains(res , "alert alert-success")

        # Checks to make sure a message about invalid display name is displayed
        self.assertContains(res , "Successfully changed display name.")

        # Checks to make sure a message about changing blurb is displayed
        self.assertNotContains(res , "Successfully changed user blurb.")



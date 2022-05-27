from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import User, Node

COOKIE_NAME: str = "StoryUserLoggedIn"
USERNAME: str = "SomeUser"

def insert_registered_user(username: str, password: str, dname: str) -> User:
    return User.objects.create(
        username=username,
        password=password,
        display_name=dname
    )

class NodeCreationViewTests(TestCase):
    def setUp(self) -> None:
        insert_registered_user(USERNAME, "Cringe", "SomeUserDisp")
        return

    def test_node_creation_page_not_logged_in(self) -> None:
        """
        The base creation page should not have a form present.
        Furthermore, it should have a redirect to the login page.
        """
        res: HttpResponse = self.client.get("/story/create-story/")
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Invalid title.")
        self.assertNotContains(res,
            "The content must be less than 10,000 characters!",
        html=True)
        self.assertNotContains(res, "Submit Story", html=True)
        self.assertContains(res, "Log in here.", html=True)
        self.assertNotContains(res, "could not find your", html=True)

        return

    def test_node_creation_page_logged_in(self) -> None:
        """
        If the user is logged in, the node creation page should give them
        a prompt to enter some title and some content for a Node.
        """
        self.client.cookies[COOKIE_NAME] = USERNAME

        res: HttpResponse = self.client.get("/story/create-story/")
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Invalid title.", html=True)
        self.assertNotContains(res,
            "The content must be less than 10,000 characters!",
        html=True)
        self.assertNotContains(res, "Submit Story", html=True)
        self.assertNotContains(res, "Log in here.", html=True)
        self.assertNotContains(res, "We could not find your account...", html=True)

        return

    def test_node_creation_false_cookie(self) -> None:
        """
        If the user has a cookie but the username is invalid, the response
        should contain a login redirect.
        """
        self.client.cookies[COOKIE_NAME] = "wawawawawaw"

        res: HttpResponse = self.client.get("/story/create-story/")
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Invalid title.", html=True)
        self.assertNotContains(res,
            "The content must be less than 10,000 characters!",
        html=True)
        self.assertContains(res, "Log in here.", html=True)

        return

    def test_node_creation_bad_title(self) -> None:
        """
        An extension of the is_valid_title() Node model test.
        If the title entered is invalid, then the response should contain "Invalid title."
        """
        self.client.cookies[COOKIE_NAME] = USERNAME

        self.client.get("/story/create-story/")
        res: HttpResponse = self.client.post("/story/create-story/", data={
            "node_title": "yoo",
            "node_content": "hi"
        })

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Invalid title.", html=True)
        self.assertNotContains(res,
            "The content must be less than 10,000 characters!",
        html=True)

        return

    def test_node_creation_bad_content(self) -> None:
        """
        An extension of the is_valid_content() Node model test.
        If the content entered is invalid, the response should not redirect.
        """
        self.client.cookies[COOKIE_NAME] = USERNAME
        long_content: str = "y" * 100000

        self.client.get("/story/create-story/")
        res: HttpResponse = self.client.post("/story/create-story/", data={
            "node_title": "Hello there bucko",
            "node_content": long_content
        })

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Invalid title.", html=True)
        self.assertIn("it has 100000", str(res.content))

        return

    def test_node_creation_all_valid(self) -> None:
        """
        No error message should be present if the user successfully creates a node.
        TEMPORARILY, THE USER SHOULD BE REDIRECTED TO THE INDEX PAGE. THIS WILL CHANGE.
        """
        self.client.cookies[COOKIE_NAME] = USERNAME

        res: HttpResponse = self.client.post("/story/create-story/", data={
            "node_title": "hows it going",
            "node_content": "klsjhgkjdshgkjhshk"
        })

        # redirect
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get("location"), "/story/")

        return

from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import Node, User, Report, Ban


def insert_story_node(post_id: str, node_title: str, node_content: str, node_author: User) -> Node:
    return Node.objects.create(
        post_id=post_id,
        node_title=node_title,
        node_content=node_content,
        node_author=node_author

    )

class UserRegistrationViewTests(TestCase):
    def test_blank_registration_page(self) -> None:
        """
        Base registration page should have no error messages present.
        """
        res: HttpResponse = self.client.get("/story/register/")
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Invalid ")
        self.assertNotContains(res, "already taken.")

        return

    def test_registration_all_fields(self) -> None:
        """
        Enter a valid username, password, and display name into each field.
        Should redirect to /story/login/ and the User should be in the db.
        The input password should be hashed, so it will not be equal to what is in the db.
        In this case, User.username can, but should not, == User.display_name.
        """
        inp_name: str = "Spongebob"
        inp_pass: str = "!1Aaaaa"
        inp_email: str = "ojjosh55@gmail.com"
        inp_dname: str = "Spongey Boy"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass,
            "email": inp_email,
            "display_name": inp_dname,
            "maturity": 18
        })

        # HTTP 302 -> Redirect (Found)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get("location"), "/story/login/")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertNotEqual(new_user, None)
        self.assertEqual(new_user.username, inp_name)
        self.assertEqual(new_user.display_name, inp_dname)
        self.assertNotEqual(new_user.password, inp_pass)
        self.assertEqual(new_user.email, inp_email)
        self.assertEqual(new_user.password, sha512(inp_pass.encode("utf-8")).hexdigest())

        return

    def test_registration_no_display_name(self) -> None:
        """
        Enter a valid username and password into their fields.
        Should redirect to /story/login/ and the User should be in the db.
        The input password should be hashed, so it will not be equal to what is in the db.
        In this case, User.username == User.display_name.
        """
        inp_name: str = "Spongebob"
        inp_pass: str = "!1Aaaaa"
        inp_email: str = "ojjosh55@gmail.com"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass,
            "email": inp_email,
            "maturity": 18
        })

        # HTTP 302 -> Redirect (Found)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get("location"), "/story/login/")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertNotEqual(new_user, None)
        self.assertEqual(new_user.username, inp_name)
        self.assertEqual(new_user.display_name, inp_name)
        self.assertNotEqual(new_user.password, inp_pass)
        self.assertEqual(new_user.email, inp_email)
        self.assertEqual(new_user.password, sha512(inp_pass.encode("utf-8")).hexdigest())

        return

    def test_bad_username(self) -> None:
        """
        Enter an invalid username (too short, too long, or bad chars) into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indicating "Invalid username."
        User should not in the db.
        """
        inp_name: str = "Yo"
        inp_pass: str = "!1Aaaaa"
        inp_email: str = "ojjosh55@gmail.com"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass,
            "email": inp_email,
            "maturity": 18
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Invalid username.")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertEqual(new_user, None)

        return

    def test_dup_username(self) -> None:
        """
        Enter a username that is already reserved into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indicating "Username is already taken."
        User should not be in the db.
        """
        orig_name: str = "Squidward"
        password: str = "!1Aaaaa"
        email: str = "ojjosh55@gmail.com"
        orig_dname: str = "uhhhhhhhh"

        # create an existing user in the database
        existing_user: User = User.objects.create(
            username=orig_name,
            password=password,
            email=email,
            display_name=orig_dname
        )

        new_dname: str = "different"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": orig_name,
            "password": password,
            "email": email,
            "display_name": new_dname,
            "maturity": 18
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Username is already taken.")

        old_user: User = User.objects.get(username=orig_name)
        new_user: User = None
        try: new_user = User.objects.get(display_name=new_dname)
        except: pass

        self.assertEqual(old_user.display_name, orig_dname)
        self.assertEqual(new_user, None)

        return

    def test_bad_display_name(self) -> None:
        """
        Enter an invalid display name (too short, too long) into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indiciating "Invalid display name."
        User should not be in the db.
        """
        inp_name: str = "Patrick"
        inp_pass: str = "!1Aaaaa"
        inp_email: str = "ojjosh55@gmail.com"
        inp_dname: str = "jj"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass,
            "email": inp_email,
            "display_name": inp_dname,
            "maturity": 18
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Invalid display name.")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertEqual(new_user, None)

        return

    def test_dup_email(self) -> None:
        """
        Enter an email that is already reserved into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indicating "Username is already taken."
        User should not be in the db.
        """
        orig_name: str = "Squidward"
        password: str = "!1Aaaaa"
        orig_dname: str = "uhhhhhhhh"
        orig_email: str = "ojjosh55@gmail.com"

        # create an existing user in the database
        existing_user: User = User.objects.create(
            username=orig_name,
            password=password,
            display_name=orig_dname,
            email=orig_email
        )

        new_email: str = "onepiece@gmail.com"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": orig_name,
            "password": password,
            "display_name": orig_dname,
            "email": orig_email,
            "maturity": 18
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertNotContains(res, "Email is already taken.")

        old_user: User = User.objects.get(email=orig_email)
        new_user: User = None
        try: new_user = User.objects.get(email=new_email)
        except: pass

        self.assertEqual(old_user.email, orig_email)
        self.assertEqual(new_user, None)

        return

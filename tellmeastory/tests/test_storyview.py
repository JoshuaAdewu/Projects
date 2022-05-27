from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import User , Node

COOKIE_NAME: str = "StoryUserLoggedIn"
USERNAME: str = "SomeUser"


def insert_registered_user(username: str , password: str , dname: str) -> User:
    return User.objects.create(
        username=username ,
        password=password ,
        display_name=dname
    )


def insert_story_node(post_id: str , node_title: str , node_content: str , node_author: User) -> Node:
    return Node.objects.create(
        post_id=post_id ,
        node_title=node_title ,
        node_content=node_content ,
        node_author=node_author

    )


class CrateAndViewStories(TestCase):

    def test_story_page_view_invalid_information(self) -> None:
        user_obj = insert_registered_user("user1" , "pwisthepw" , "My Display Name")
        insert_story_node("skjfiw-fjwood-wkkdld" , "My Story Title" , "This is the content of my story" , user_obj)

        res: HttpResponse = self.client.get("/post/INVALIDPOST/")

        # Make sure that the page loaded
        self.assertEqual(res.status_code , 200)
        # Make sure that an invalid post message is received
        self.assertContains(res , "You have tried to access a story page that does not exist.")

        return

    def test_story_page_view_valid_information(self) -> None:
        post_id = "skjfiw-fjwood-wkkdld"
        user_obj = insert_registered_user("user1" , "pwisthepw" , "My Display Name")
        story_node = insert_story_node(post_id , "My Story Title" , "This is the content of my story" , user_obj)

        res: HttpResponse = self.client.get("/post/" + post_id + "/")

        # Make sure that the page loaded
        self.assertEqual(res.status_code , 200)

        # Make sure that the post title is displayed
        self.assertContains(res , "My Story Title")

        # Make sure that the post content is displayed
        self.assertContains(res , "This is the content of my story")

        # Make Sure Reactions are Shown
        self.assertContains(res , "<b>0</b>")

        UserGet = User.objects.get(id=user_obj.id)
        # Add thumbs down Reaction
        story_node.add_reaction("thumbsdown" , UserGet)

        res: HttpResponse = self.client.get("/post/" + post_id + "/")

        # Check to make sure the thumbs down has displayed 1 node
        self.assertContains(res , "<b>1</b>")

        # Check to make sure the actual count is 1
        self.assertEqual(story_node.num_reactions_of_emoji("thumbsdown") , 1)

        return

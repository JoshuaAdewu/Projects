from django.test import TestCase
from tellmeastory.models import User, Node
from django.http import HttpResponse

COOKIE_NAME: str = "StoryUserLoggedIn"

def insert_registered_user(username: str, password: str, dname: str) -> User:
    return User.objects.create(
        username=username,
        password=password,
        display_name=dname
    )

def insert_story_node(post_id: str, node_title: str, node_content: str, node_author: User) -> Node:
    return Node.objects.create(
        post_id=post_id,
        node_title=node_title,
        node_content=node_content,
        node_author=node_author

    )

class NodeEditViewTests(TestCase):
    def test_edit_node(self):
        userObj = insert_registered_user("Zebra123", "oatw9ktoda", "BigZebra")
        insert_story_node("252052-06262060a-26a62", "My first story!", "Blah blah blah", userObj)

        self.client.cookies[COOKIE_NAME] = "Zebra123"

        # should equal 200
        response = self.client.get('/modify/252052-06262060a-26a62')
        self.assertEqual(response.status_code, 200)

        #simulate an edited node
        nodeObj = Node.objects.get(post_id="252052-06262060a-26a62")
        nodeObj.node_content = "Changed text"
        nodeObj.save()

        res: HttpResponse = self.client.get("/profile/" + "Zebra123" + "/")

        # Checks that our story has successfully been edited
        self.assertContains(res, "Changed text")
        return

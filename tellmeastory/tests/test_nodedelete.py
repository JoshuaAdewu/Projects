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

def insert_story_node(post_id: str, node_title: str, node_content: str, node_author: User) -> Node:
    return Node.objects.create(
        post_id=post_id,
        node_title=node_title,
        node_content=node_content,
        node_author=node_author

    )


class NodeDeletionViewTests(TestCase):
    """
    Basic test inserting a node then deleting it
    """





    def test_node_deletion(self)-> None:
        userObj = User(1,"Zebra123", "oatw9ktoda", "BigZebra")
        nodeObj = insert_story_node("252052-06262060a-26a62", "My first story!", "Blah blah blah", userObj)

        userObj.save()
        nodeObj.delete()
        deleteCheck = Node.objects.filter(post_id="252052-06262060a-26a62")
        deleteCheckCount = deleteCheck.count()
        self.assertEqual(deleteCheckCount, 0)
        return


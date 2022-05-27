from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import Node
from django.db.models import ImageField
from tellmeastory.forms import AddImageForm
from django.core.files.uploadedfile import SimpleUploadedFile

class NodeImageTests(TestCase):
    def test_add_image_to_node(self):
        """
        Creates a node and adds an image to it, then test
        updates the image stored to a new image.
        """
        # Check form comes back
        self.assertIsNotNone(AddImageForm(data={"image_file": "storyimages/test_image.jpeg", "id": 1}))
        self.assertIsNotNone(AddImageForm(data={"image_url": "www.google.com", "id": 1}))
        # Add an image from a valid file
        test_image_path = "media/storyimages/test_image.jpeg"
        test_image_file = SimpleUploadedFile(name='test_image.jpeg',
                                             content=open(test_image_path, 'rb').read(),
                                             content_type='image/jpeg')
        node: Node = Node(node_title="Test1")
        node.save()
        self.assertIs(Node.objects.get(id=node.id).add_image(newFile=test_image_file), True)
        self.assertIs(Node.objects.get(id=node.id).has_image_file, True)
        self.assertNotEqual(Node.objects.get(id=node.id).image.url, None)
        return

    def test_add_url_image_to_node(self):
        """
        Add image sourced from another website to be attached to a
        node. The image must be stored in the node after adding the
        url.
        """
        # Add an image from a valid URL
        test_image_url = "https://www.google.com/"
        node: Node = Node(node_title="Test2")
        node.save()
        self.assertIs(Node.objects.get(id=node.id).add_image(newURL=test_image_url), True)
        self.assertIs(Node.objects.get(id=node.id).has_image_file, False)
        # Add an image from an invalid URL
        test_image_url = "invalidlink_testing"
        node: Node = Node(node_title="Test3")
        node.save()
        self.assertIs(Node.objects.get(id=node.id).add_image(newURL=test_image_url), False)
        return

    def test_change_image(self):
        """
        Swap between URL and file images. Should not cause
        errors and properties must be updated.
        """
        # Test image file
        test_image_path = "media/storyimages/test_image.jpeg"
        test_image_file = SimpleUploadedFile(name='test_image.jpeg',
                                             content=open(test_image_path, 'rb').read(),
                                             content_type='image/jpeg')
        # Test image url
        test_image_url = "https://www.google.com/"

        # Create test node
        node: Node = Node(node_title="Test4")
        node.save()

        # Swap to image from no image (initialize
        self.assertIs(Node.objects.get(id=node.id).add_image(newFile=test_image_file), True)
        # Swap to URL from file
        self.assertIs(Node.objects.get(id=node.id).add_image(newURL=test_image_url), True)
        # Swap to file from URL
        self.assertIs(Node.objects.get(id=node.id).add_image(newFile=test_image_file), True)
        return

    def test_add_image_view(self):
        '''
        Test for proper responses from submitting multiple possible forms
        to the add image to a node view.
        '''
        # Test image file
        test_image_path = "media/storyimages/test_image.jpeg"
        test_image_file = SimpleUploadedFile(name='test_image.jpeg',
                                             content=open(test_image_path, 'rb').read(),
                                             content_type='image/jpeg')
        # Test image url
        test_image_url = "https://www.google.com/"
        all_nodes = Node.objects.filter()
        err_msg = "N/A"
        # Create test node
        node: Node = Node(node_title="Test5")
        node.save()
        # Process basic request for url
        self.client.get("/story/addnodeimage/")  # Process basic request for prompts
        res: HttpResponse = self.client.post("/story/addnodeimage/", data={
            "form": AddImageForm,
            "err_msg": err_msg,
            "image_url": test_image_url,
            "id": node.id,
            "nodes": all_nodes
        })
        self.assertEqual(res.status_code, 200)
        # Process basic request for image
        self.client.get("/story/addnodeimage/")  # Process basic request for prompts
        res: HttpResponse = self.client.post("/story/addnodeimage/", data={
            "form": AddImageForm,
            "err_msg": err_msg,
            "image_file": test_image_file,
            "image_url": "",
            "id": node.id,
            "nodes": all_nodes
        })
        self.assertEqual(res.status_code, 200)
        # Process basic request with invalid node
        self.client.get("/story/addnodeimage/")  # Process basic request for prompts
        res: HttpResponse = self.client.post("/story/addnodeimage/", data={
            "form": AddImageForm,
            "err_msg": err_msg,
            "image_file": test_image_file,
            "image_url": "",
            "id": 0,
            "nodes": all_nodes
        })
        self.assertEqual(res.status_code, 200)
        return

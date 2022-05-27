from django.test import TestCase
from tellmeastory.models import Node, User
from managetags.models import Tag
from selenium import webdriver
from django.test import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from hashlib import sha512
from django.core.files.uploadedfile import SimpleUploadedFile

class AddNodeFromUserTests(LiveServerTestCase):

    def test_enter_node_information(self):
        """
        Function contains Sections 1 and 2.
        Section 1 is Setup and Input
        Section 2 is Submission and Check

        Section 1 of Function
        Test a user entering information about a node.
        The fields should all be present for title, text
        content, image, and tags.
        """
        # Create a test user for login
        username = "namename"
        password = "password1"
        email = "ojjosh55@gmail.com"
        display_name = "display"
        # Register above credentials
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        password_input = selenium_browser.find_element(By.NAME, value="email")
        password_input.send_keys(email)  # Enter email
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        maturity_input = selenium_browser.find_element(By.NAME, value="maturity")
        maturity_input.send_keys(16)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()
        # Navigate to Story Posting for given user
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/'+username))
        # Enter Title, Content, One Image, and a Main Tag ID (after first creating a Tag)
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag() # Create Main Tag to Add
        title_input = selenium_browser.find_element(By.NAME, value="node_title")
        title_input.send_keys("title")  # Enter story title
        content_input = selenium_browser.find_element(By.NAME, value="node_content")
        content_input.send_keys("content")  # Enter story content
        image_input = selenium_browser.find_element(By.NAME, value="image_url")
        image_input.send_keys("www.google.com")  # Enter valid URL
        main_tag_input = selenium_browser.find_element(By.NAME, value="main_tag_id")
        main_tag_input.send_keys(TagToInsert.id)  # Enter valid tag id
        # Enter longitude and latitude
        title_input = selenium_browser.find_element(By.NAME, value="latitude")
        title_input.send_keys(0)  # Enter latitude
        title_input = selenium_browser.find_element(By.NAME, value="longitude")
        title_input.send_keys(0)  # Enter longitude
        """
        Section 2 of Function
        Tests submitting a node with various data
        needed for a node and check if node was 
        correctly saved.
        """
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()
        # Check that node success message was printed
        success_message = "Successfully Added your Story!"
        self.assertTrue(selenium_browser.page_source.find(success_message) != -1)
        # Check that node exists and the author is the user that registered
        self.assertTrue(Tag.objects.count())  # Check if tags exist
        self.assertTrue(Node.objects.count())  # Check if nodes exist
        self.assertTrue(Node.objects.filter(node_author__username=username).first().node_title == "title")  # Check title
        self.assertTrue(Node.objects.filter(node_author__username=username).first().node_content == "content")  # Check content
        self.assertFalse(Node.objects.filter(node_author__username=username).first().has_image_file)  # Check image (should only have url, not file)
        return

    def test_add_invalid_and_valid_story_fields(self):
        """
        Tests invalid input for all story fields. The correct error
        message should appear and no additional nodes should exist.
        """
        # Create a temporary Test user for calling post function
        username = "namename"
        password = "password1"
        display_name = "display"
        user = User.objects.create(username=username, password=sha512(password.encode("utf-8")).hexdigest(), display_name=display_name)
        # Test invalid main tag response (when there are no tags at all)
        invalid_main_tag_err = "Main Tag not found. Please select a valid main tag."
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": 1,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 90
                }
        self.assertTrue(invalid_main_tag_err, user.post_node(invalid_node_dict))
        # Create test tag
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag() # Create Main Tag to Add
        # Test invalid title response
        invalid_title_err = "Invalid title"
        invalid_node_dict = {
                    "node_title": "t",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 90
                }
        self.assertTrue(invalid_title_err, user.post_node(invalid_node_dict))
        # Test invalid content response
        invalid_content_err = "Content is limited to 10,000 characters"
        long_content: str = "l" * 100000
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": long_content,
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 90
                }
        self.assertTrue(invalid_content_err, user.post_node(invalid_node_dict))
        # Test invalid image response
        invalid_image_err = "Invalid Image. You may add one image to each story."
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": "www.google.com",
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 90
                }
        self.assertTrue(invalid_image_err, user.post_node(invalid_node_dict))
        # Test invalid main tag response
        invalid_main_tag_err = "Main Tag not found. Please select a valid main tag."
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": -1,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 90
                }
        self.assertTrue(invalid_main_tag_err, user.post_node(invalid_node_dict))
        # Test valid image response
        test_image_path = "media/storyimages/test_image.jpeg"
        test_image_file = SimpleUploadedFile(name='test_image.jpeg',
                                             content=open(test_image_path, 'rb').read(),
                                             content_type='image/jpeg')
        valid_response = "Successfully Added your Story! Please refresh page to see changes."
        invalid_node_dict = {
                    "node_title": "titletitle",
                    "node_content": "content",
                    "image_file": test_image_file,
                    "image_url": None,
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 90
                }
        self.assertTrue(valid_response, user.post_node(invalid_node_dict))
        return

    def test_existing_stories_and_tags_present(self):
        """
        Tests if the existing stories of a user are present
        on the node creation page and tags too.
        """
        # Create a test user for login
        username = "namename"
        password = "password1"
        email = "ojjosh55@gmail.com"
        display_name = "display"
        # Register above credentials
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        password_input = selenium_browser.find_element(By.NAME, value="email")
        password_input.send_keys(email)  # Enter email
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        maturity_input = selenium_browser.find_element(By.NAME, value="maturity")
        maturity_input.send_keys(16)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()
        # Check for stories posted by other users (should be none)
        # Create a temporary Test user for calling post function
        newusername = "namename1"
        newpassword = "password2"
        newdisplay_name = "display1"
        newuser = User.objects.create(username=newusername, password=sha512(newpassword.encode("utf-8")).hexdigest(), display_name=newdisplay_name)
        # Create test tag
        NewTagToInsert = Tag(name_text="differentTag", language="en_US")
        NewTagToInsert.add_new_tag() # Create Main Tag to Add
        valid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": NewTagToInsert.id,
                    "mature_node": False,
                    "latitude": 0,
                    "longitude": 0
                }
        newuser.post_node(valid_node_dict)
        present_story = "ID: " + str(Node.objects.filter(node_author__username=newusername).first().id)\
                      + " Title: " + Node.objects.filter(node_author__username=newusername).first().node_title
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/'+username))  # Navigate to Story Posting for a different user
        self.assertTrue(selenium_browser.page_source.find(present_story) == -1)  # It should not find another user's story on creation page
        # Enter Title, Content, One Image, and a Main Tag ID (after first creating a Tag)
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag() # Create Main Tag to Add
        title_input = selenium_browser.find_element(By.NAME, value="node_title")
        title_input.send_keys("title")  # Enter story title
        content_input = selenium_browser.find_element(By.NAME, value="node_content")
        content_input.send_keys("content")  # Enter story content
        image_input = selenium_browser.find_element(By.NAME, value="image_url")
        image_input.send_keys("www.google.com")  # Enter valid URL
        main_tag_input = selenium_browser.find_element(By.NAME, value="main_tag_id")
        main_tag_input.send_keys(TagToInsert.id)  # Enter valid tag id
        # Enter longitude and latitude
        title_input = selenium_browser.find_element(By.NAME, value="latitude")
        title_input.send_keys(0)  # Enter latitude
        title_input = selenium_browser.find_element(By.NAME, value="longitude")
        title_input.send_keys(0)  # Enter longitude
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()
        """ Now the stories should be present as well as the tags on the posting page. """
        # Navigate to Story Posting for given user
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/'+username))
        # Check if the added tag is present on the page with its ID
        tag_with_ID = "ID: " + str(TagToInsert.id) + " Name: " + TagToInsert.name_text
        self.assertTrue(selenium_browser.page_source.find(tag_with_ID) != -1)
        # Check if the added story is present on the page with its ID
        story_with_ID = "ID: " + str(Node.objects.filter(node_author__username=username).first().id)\
                      + " Title: " + Node.objects.filter(node_author__username=username).first().node_title
        self.assertTrue(selenium_browser.page_source.find(story_with_ID) != -1)
        return

    def test_long_lat_input(self):
        """
        Tests will run to check for invalid long
        and lat values given to posting function.
        """
        # Create a temporary Test user for calling post function
        username = "namename"
        password = "password1"
        display_name = "display"
        user = User.objects.create(username=username, password=sha512(password.encode("utf-8")).hexdigest(), display_name=display_name)
        # Create test tag
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag() # Create Main Tag to Add
        # Test invalid responses
        invalid_lat_err = "Invalid latitude"
        invalid_long_err = "Invalid longitude"
        # Test overly large latitude
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 91,
                    "longitude": 90
                }
        self.assertTrue(invalid_lat_err, user.post_node(invalid_node_dict))
        # Test overly small latitude
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": -91,
                    "longitude": 90
                }
        self.assertTrue(invalid_lat_err, user.post_node(invalid_node_dict))
        # Test overly large longitude
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": 181
                }
        self.assertTrue(invalid_long_err, user.post_node(invalid_node_dict))
        # Test overly small longitude
        invalid_node_dict = {
                    "node_title": "title",
                    "node_content": "content",
                    "image_file": None,
                    "image_url": "www.google.com",
                    "main_tag_id": TagToInsert.id,
                    "mature_node": False,
                    "latitude": 90,
                    "longitude": -181
                }
        self.assertTrue(invalid_long_err, user.post_node(invalid_node_dict))
        return


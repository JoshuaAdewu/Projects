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
        Tests that navbar search redirects to correct
        search results page on all modified pages.
        """
        # Create a test user for login
        username = "namename"
        password = "password1"
        email = "ojjosh55@gmail.com"
        display_name = "display"
        # Start selenium
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        # Navigate to no profile page
        selenium_browser.get('%s%s' % (self.live_server_url, '/profile/' + username))
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertNotEqual("Search Results", selenium_browser.title)
        # Register given credentials
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        email_input = selenium_browser.find_element(By.NAME, value="email")
        email_input.send_keys(email)  # Enter email
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        maturity_input = selenium_browser.find_element(By.NAME, value="maturity")
        maturity_input.send_keys(18)  # Enter display name
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
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertEqual("Search Results", selenium_browser.title)
        # Navigate to account page
        selenium_browser.get('%s%s' % (self.live_server_url, '/account/' + username))
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertEqual("Search Results", selenium_browser.title)
        # Navigate to login page
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertNotEqual("Search Results", selenium_browser.title)
        # Navigate to map page
        selenium_browser.get('%s%s' % (self.live_server_url, '/map/'))
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertEqual("Search Results", selenium_browser.title)
        # Navigate to profile page
        selenium_browser.get('%s%s' % (self.live_server_url, '/profile/' + username))
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertEqual("Search Results", selenium_browser.title)
        # Navigate to register page
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        # Test search redirect here
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        self.assertNotEqual("Search Results", selenium_browser.title)
        return

    def test_content_present_in_search_results(self):
        """
        Test checks for the presence of all required parts
        of a story presentation. This includes the title,
        author, maturity, and location.
        """
        # Test search redirect here
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
        email_input = selenium_browser.find_element(By.NAME, value="email")
        email_input.send_keys(email)  # Enter email
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        maturity_input = selenium_browser.find_element(By.NAME, value="maturity")
        maturity_input.send_keys(18)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()
        # Navigate to Story Posting for given user
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/' + username))
        # Enter Title, Content, One Image, and a Main Tag ID (after first creating a Tag)
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag()  # Create Main Tag to Add
        title_input = selenium_browser.find_element(By.NAME, value="node_title")
        title_input.send_keys("title")  # Enter story title
        content_input = selenium_browser.find_element(By.NAME, value="node_content")
        content_input.send_keys("content")  # Enter story content
        image_input = selenium_browser.find_element(By.NAME, value="image_url")
        image_input.send_keys("www.google.com")  # Enter valid URL
        main_tag_input = selenium_browser.find_element(By.NAME, value="main_tag_id")
        main_tag_input.send_keys(TagToInsert.id)  # Enter valid tag id
        # Enter longitude and latitude
        loc_input = selenium_browser.find_element(By.NAME, value="latitude")
        loc_input.send_keys(0)  # Enter latitude
        loc_input = selenium_browser.find_element(By.NAME, value="longitude")
        loc_input.send_keys(0)  # Enter longitude
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()

        # Check if all needed components are on the screen
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()  # Empty search matches everything
        self.assertTrue(selenium_browser.page_source.find("title") != -1)
        self.assertTrue(selenium_browser.page_source.find("www.google.com") != -1)
        self.assertTrue(selenium_browser.page_source.find("name123") != -1)
        self.assertTrue(selenium_browser.page_source.find("Longitude: 0.0") != -1)
        self.assertTrue(selenium_browser.page_source.find("Latitude: 0.0") != -1)
        return

    def test_many_stories_present_in_results(self):
        # Start selenium
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())

        # Create a temporary Test user
        username = "namename"
        password = "password1"
        display_name = "display"

        user = User.objects.create(username=username, password=sha512(password.encode("utf-8")).hexdigest(),
                                   display_name=display_name)
        self.client.cookies["StoryUserLoggedIn"] = username

        # Navigate to map page
        selenium_browser.get('%s%s' % (self.live_server_url, '/map/'))


        # Insert 100 test nodes (of many different titles)
        arbitrary_num_nodes = 100
        for i in range(arbitrary_num_nodes):
            # Create test tag
            TagToInsert = Tag(name_text="name123"+str(i), language="en_US")
            TagToInsert.add_new_tag()  # Create Main Tag to Add
            valid_node_dict = {
                        "node_title": "title"+str(i),
                        "node_content": "content",
                        "image_file": None,
                        "image_url": "www.google.com",
                        "main_tag_id": TagToInsert.id,
                        "mature_node": False,
                        "latitude": 90,
                        "longitude": 90
                    }
            user.post_node(valid_node_dict)


        # Check that search results contain all test nodes
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()  # Empty search matches everything

        # All added titles must be present
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find("title"+str(i)) != -1)
        return

    def test_immature_user_cannot_search_mature_content(self):
        """
        Test checks that an immature user cannot find
        mature story content. User registration defaults
        to immature.
        """
        # Test search redirect here
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
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        email_input = selenium_browser.find_element(By.NAME, value="email")
        email_input.send_keys(email)  # Enter email
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
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/' + username))
        # Enter Title, Content, One Image, and a Main Tag ID (after first creating a Mature Tag)
        TagToInsert = Tag(name_text="Mature", language="en_US")
        TagToInsert.add_new_tag()  # Create Mature tag to Add
        title_input = selenium_browser.find_element(By.NAME, value="node_title")
        title_input.send_keys("maturenodestory")  # Enter story title
        content_input = selenium_browser.find_element(By.NAME, value="node_content")
        content_input.send_keys("content")  # Enter story content
        image_input = selenium_browser.find_element(By.NAME, value="image_url")
        image_input.send_keys("www.google.com")  # Enter valid URL
        main_tag_input = selenium_browser.find_element(By.NAME, value="main_tag_id")
        main_tag_input.send_keys(TagToInsert.id)  # Enter valid tag id
        # Enter longitude and latitude
        loc_input = selenium_browser.find_element(By.NAME, value="latitude")
        loc_input.send_keys(0)  # Enter latitude
        loc_input = selenium_browser.find_element(By.NAME, value="longitude")
        loc_input.send_keys(0)  # Enter longitude
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()

        # Check that no mature nodes are present
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()  # Empty search matches everything
        self.assertTrue(selenium_browser.page_source.find("maturenodestory") == -1)
        self.assertTrue(selenium_browser.page_source.find("www.google.com") == -1)
        self.assertTrue(selenium_browser.page_source.find("name123") == -1)
        self.assertTrue(selenium_browser.page_source.find("Longitude: 0.0") == -1)
        self.assertTrue(selenium_browser.page_source.find("Latitude: 0.0") == -1)
        return

    def test_search_results(self):
        # Test search redirect here
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
        email_input = selenium_browser.find_element(By.NAME, value="email")
        email_input.send_keys(email)  # Enter email
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        maturity_input = selenium_browser.find_element(By.NAME, value="maturity")
        maturity_input.send_keys(18)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()
        # Get to search page
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()  # Empty search matches everything

        # Insert 9 test nodes (of many different titles)
        arbitrary_num_nodes = 10
        user = User.objects.get(username=username)
        for i in range(arbitrary_num_nodes):
            # Create test tag
            TagToInsert = Tag(name_text="name123"+str(i), language="en_US")
            TagToInsert.add_new_tag()  # Create Main Tag to Add
            valid_node_dict = {
                        "node_title": "uniquetitle"+str(i),
                        "node_content": "content",
                        "image_file": None,
                        "image_url": "www.google.com",
                        "main_tag_id": TagToInsert.id,
                        "mature_node": False,
                        "latitude": 90,
                        "longitude": 90
                    }
            user.post_node(valid_node_dict)
        # UNIQUE SEARCH -- All unique searches must be unique and result in a singular node
        for i in range(arbitrary_num_nodes):
            # Check that search results contain all searched nodes
            search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
            search_input.send_keys("uniquetitle"+str(i))  # Enter search query based on unique identifiers
            selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
            # Searched for node should be present
            self.assertTrue(selenium_browser.page_source.find("uniquetitle"+str(i)) != -1)
            # No other nodes should be present
            for j in range(arbitrary_num_nodes):
                if j != i:
                    self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(j))) == -1)
        # CASE INSENSITIVE -- Case should not matter
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys("Uniquetitle" + str(0))  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for node should be present
        self.assertTrue(selenium_browser.page_source.find("uniquetitle" + str(0)) != -1)
        # TAG SEARCH -- Can find stories by their tags
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys("name123" + str(0))  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for node should be present
        self.assertTrue(selenium_browser.page_source.find("name123" + str(0)) != -1)
        # AUTHOR SEARCH - Can search by author
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys(username)  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for nodes should be present
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) != -1)
        # URL SEARCH -- Can search by story url
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys("www.google.com")  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for nodes should be present
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) != -1)
        # CONTENT SEARCH -- Searching by content should return all matching stories with matching content
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys("content")  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for nodes should be present
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) != -1)
        # PARTIAL VALUE -- Query making partial matches to stories should come up
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys("uniquetitle")  # Enter search query with partial matches to all stories
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for nodes should be present (all)
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) != -1)
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        # PARTIAL VALUE -- Tag partial value matches should not return anything
        search_input.send_keys("name123")  # Enter search query with partial matches to all stories
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # Searched for nodes should be present (all)
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) == -1)
        # NO RESULT SEARCH -- No nodes should come up with an invalid match
        invalid_query = "Armando1"
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys(invalid_query)  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # No nodes should be present
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) == -1)
        invalid_query = "HElO41230"
        search_input = selenium_browser.find_element(By.XPATH, value='//input[@type="search"]')
        search_input.send_keys(invalid_query)  # Enter search query based on unique identifiers
        selenium_browser.find_element(By.XPATH, value='//button[@value="Search"]').click()
        # No nodes should be present
        for i in range(arbitrary_num_nodes):
            self.assertTrue(selenium_browser.page_source.find(("uniquetitle" + str(i))) == -1)
        return

from decimal import Decimal
from django.http import HttpResponse
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tellmeastory.models import Node, User


USERNAME: str = "namename"
PASSWORD: str = "password"
EMAIL: str = "ojjosh55@gmail.com"
DIS_NAME: str = "display"

URL_MAPS = "/story/map/"
class MapPageViewTests(TestCase):

    # We can use this to check if the webpage loaded. Since the
    # Map is loaded client sided. Client can view map as long as the API key is correct
    def test_map_page_loading(self) -> None:
        self.client.cookies["StoryUserLoggedIn"] = USERNAME
        User.objects.create(username=USERNAME,password=PASSWORD, display_name=DIS_NAME)

        res: HttpResponse = self.client.get(URL_MAPS)





        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code, 200)
        # Checks to make sure the map frame loaded within the HTTPResponse
        self.assertContains(res, "<div id='map' width='100%' style='margin-top:100px; height:800px'></div>")

class CreateStoryFromMap(LiveServerTestCase):
    def test_double_click_redirects(self) -> None:
        """
        Double clicking a location on the map should redirect the user
        to the author-story page with the location as args in the URL.
        """
        # Register credentials
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(USERNAME)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(PASSWORD)  # Enter password
        email_input = selenium_browser.find_element(By.NAME, value="email")
        email_input.send_keys(EMAIL)  # Enter username
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(DIS_NAME)  # Enter display name
        maturity_input = selenium_browser.find_element(By.NAME, value="maturity")
        maturity_input.send_keys(16)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()

        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(USERNAME)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(PASSWORD)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()

        # redirect to map page and click in the middle of the screen
        selenium_browser.get(f"{self.live_server_url}{URL_MAPS}")
        map = selenium_browser.find_element(By.XPATH, value='//div[@id="map"]')
        ActionChains(selenium_browser).double_click(map).perform()

        # verify that we were redirected to the story creation page
        self.assertIn(
            f"{self.live_server_url}/story/author-story/{USERNAME}/",
            selenium_browser.current_url
        )

        return

    def test_map_renders_nodes(self) -> None:
        """
        The map should have markers for nodes that have been created.
        Note: The magic coordinates for long/lat are the starting point of the map on load.
        """
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        node: Node = Node.objects.create(
            node_title="Test Node",
            longitude=Decimal(-76.611),
            latitude=Decimal(39.301)
        )

        # redirect to map page and verify that "mapboxgl-marker mapboxgl-marker-anchor-center" is present
        selenium_browser.get(f"{self.live_server_url}{URL_MAPS}")
        self.assertIn(
            "mapboxgl-marker mapboxgl-marker-anchor-center",
            selenium_browser.page_source
        )

        return

    def test_regression_double_click_no_login(self) -> None:
        """
        Regression test.
        Changed a Javascript conditional that was always true when double clicking the map.
        If the user was not logged in, they would get a 404.
        Double clicking when not logged in should do nothing.
        """

        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())

        # redirect to map page and click in the middle of the screen
        selenium_browser.get(f"{self.live_server_url}{URL_MAPS}")

        map = selenium_browser.find_element(By.XPATH, value='//div[@id="map"]')
        ActionChains(selenium_browser).double_click(map).perform()

        # verify that we were not redirected
        self.assertEqual(
            f"{self.live_server_url}{URL_MAPS}",
            selenium_browser.current_url
        )
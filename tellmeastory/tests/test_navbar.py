from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


URL_PROFILE = "/profile/"
TEST_ACCOUNT = "tellme1"
COOKIE_NAME: str = "StoryUserLoggedIn"

def insertUser(usern: str , pw: str , dname: str) -> User:
    return User.objects.create(
        username=usern ,
        password=sha512(pw.encode("utf-8")).hexdigest() ,
        display_name=dname ,
    )


class navBarTests(TestCase):


    # Tests to make sure Login and Register are displayed on the navbar.
    def test_login_register(self)->None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")


        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks to ensure that Login and Register are displayed
        self.assertContains(res, "Login")
        self.assertContains(res, "Register")

    def test_myaccount_myprofile(self)-> None:

        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName,
            "password": pw
        })

        self.client.cookies[COOKIE_NAME] = uName
        res: HttpResponse = self.client.get("/story/account/" + TEST_ACCOUNT + "/")

        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        #Checks to make sure that the profile page is addressed
        self.assertContains(res, "My Profile")

        # Checks to ensure that a welcome message is given
        self.assertContains(res , "Welcome")

    def test_myaccount_manage(self)-> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })

        self.client.cookies[COOKIE_NAME] = uName
        res: HttpResponse = self.client.get("/story/account/" + TEST_ACCOUNT + "/")


        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks to make sure that a manage page is properly displayed
        self.assertContains(res , "Manage")

    def test_myaccount_attempt_other_account(self)-> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        extraAccount = "thetest1"

        insertUser(uName , pw , dName)
        insertUser(extraAccount, pw, dName + " Second")

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })


        res: HttpResponse = self.client.get("/story/account/" + extraAccount + "/")



        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks to make sure an Oh No! message is displayed to the user
        self.assertContains(res, "Oh no!")


class SeleniumTests(LiveServerTestCase):

    def testLogin(self):
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"
        insertUser(uName , pw , dName)

        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = selenium.find_element(By.NAME, value="username")
        username_input.send_keys(uName)

        pw_input = selenium.find_element(By.NAME, value="password")
        pw_input.send_keys(pw)

        selenium.find_element(By.XPATH, value = '//input[@value="Login"]').click()
        # Check to make sure that welcome user is displayed
        checkmsg = "Welcome, " + uName
        assert checkmsg in selenium.page_source

    def testRegister(self):
        uName2 = "TheTester123"
        pw = "testing123"
        dName = "John Doe"
        insertUser(uName2 , pw , dName)

        selenium = webdriver.Chrome(ChromeDriverManager().install())


        # Register the account
        selenium.get('%s%s' % (self.live_server_url , '/register/'))

        username_input = selenium.find_element(By.NAME , value="username")
        username_input.send_keys(uName2)

        pw_input = selenium.find_element(By.NAME , value="password")
        pw_input.send_keys(pw)

        display_name_input = selenium.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(dName)

        selenium.find_element(By.XPATH , value='//input[@value="Register"]').click()

        # Log in the account
        selenium.get('%s%s' % (self.live_server_url , '/login/'))

        username_input = selenium.find_element(By.NAME, value="username")
        username_input.send_keys(uName2)

        pw_input = selenium.find_element(By.NAME, value="password")
        pw_input.send_keys(pw)

        selenium.find_element(By.XPATH, value = '//input[@value="Login"]').click()

        # Check to make sure we are in the account page
        checkmsg = "Manage " + dName + "'s Account"
        assert checkmsg in selenium.page_source

    def testCorrectInformationDisplay(self):
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"
        insertUser(uName , pw , dName)

        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('%s%s' % (self.live_server_url, '/profile/' + uName))

        # Check to make sure that Register and Login Buttons are Displayed

        assert "Register" in selenium.page_source
        assert "Login" in selenium.page_source
        assert "Tell Me A Story" in selenium.page_source



## HOW TO INSTALL SELENIUM

# python -m pip install selenium
# python -m pip install webdriver-manager

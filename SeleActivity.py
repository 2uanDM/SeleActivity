from random import *
import time
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import random


class UserActivity():
    def __init__(self, **kwargs):
        """
        Constructor ~
        - If you don't mention the user profile, this will open a browser with an new user profile
        - Remember that, if you want to open a browser with an existing profile, then you must to CLOSE all Chrome windows first
        Kwargs:
            profile_dir (string): The link to the profile folder  
            profile_name (string): The name of the profile (If not mentioned, the default value is "Default")
            proxy (string): Proxy you want to connect (IP:port)
        """

        # Add options to the Chrome driver
        options = uc.ChromeOptions()

        if "profile_dir" in kwargs:
            profile_dir = kwargs.get("profile_dir")
            profile_name = kwargs.get("profile_name", "Default")

            # Add profile arguments
            options.add_argument(f"--user-data-dir={profile_dir}")
            options.add_argument(f"--profile-directory={profile_name}")

        if "proxy" in kwargs:
            proxy = kwargs.get("proxy")
            options.add_argument(f"--proxy-server={proxy}")

        # Get the Chrome driver
        self.driver = uc.Chrome(options=options)

    def resizeWindow(self, x, y):
        """
        Resize your browser window
        Args:
            x (int): width size
            y (int): height size
        """
        self.driver.set_window_size(x, y)

    def clearBrowserData(self):
        """
        Clear all your browser's data (No parameters needed)
        """
        self.driver.get('chrome://settings/clearBrowserData')
        time.sleep(2)
        self.driver.find_element(
            By.XPATH, '//settings-ui').send_keys(Keys.ENTER)

    def openWebPage(self, url):
        """
        This method is used for open a specified web page
        The maximum wait time for this activity is 10 seconds
        After this time, if the "Time out Exception" occurs, then refresh the web page

        Args:
            url (string): Url of the web page 
        """
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except TimeoutException:
            self.driver.refresh()

    def clickButton(self, XPATH):
        """
        Click a button or any clickable object 
        Args:
            XPATH (string): XPATH of the object
        """
        button = self.driver.find_element(By.XPATH, XPATH)
        button.click()
        self.driver.implicitly_wait(1)

    def scrollToElement(self, XPATH):
        """
        Scroll to the element immediately
        Args:
            XPATH (string): XPATH of the object
        """
        target = self.driver.find_element(By.XPATH, XPATH)
        self.driver.execute_script('arguments[0].scrollIntoView(true)', target)
        self.driver.implicitly_wait(1)

    def scrollUp(self, height):
        """
        Scroll up by a specific height
        Args:
            height (int): Vertical distance
        """
        self.driver.execute_script(f'scrollBy(0,-{height})')
        self.driver.implicitly_wait(1)

    def scrollDown(self, height):
        """
        Scroll down by a specific height
        Args:
            height (int): Vertical distance
        """
        self.execute_script(f'scrollBy(0,{height})')
        self.driver.implicitly_wait(1)

    def scrollDownSlowly(self, totalHeight, smooth):
        """
        Scroll down slowly by a specific height
        Args:
            totalHeight (int): Vertical distance
            smooth (int): Smoothy of your scrool
        """
        # The higher the smooth parameter, the smoothier the activity is
        step = totalHeight / smooth
        for x in range(smooth):
            self.driver.execute_script(f'scrollBy(0,{step})')
            # time.sleep(0.001)

    def scrollUpSlowly(self, totalHeight, smooth):
        """
        Scroll up slowly by a specific height
        Args:
            totalHeight (int): Vertical distance
            smooth (int): Smoothy of your scrool
        """
        # The higher the smooth parameter, the smoothier the activity is
        step = totalHeight / smooth
        for x in range(smooth):
            self.driver.execute_script(f'scrollBy(0,-{step})')
            time.sleep(uniform(0, 0.05))

    def enterText(self, XPATH, text):
        """
        Enter text in a box object (clearBox is recommended to do first)
        Args:
            XPATH (string): XPATH of the box object
            text (string): content
        """
        enterBox = self.driver.find_element(By.XPATH, XPATH)
        enterBox.clear()
        enterBox.send_keys(text)
        time.sleep(1)

    def clearBox(self, XPATH):
        """
        Clear text in a box object
        Args:
            XPATH (string): XPATH of the box object
        """
        enterBox = self.driver.find_element(By.XPATH, XPATH)
        enterBox.clear()

    def maximizeWindow(self):
        self.driver.maximize_window()

    def newTab(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(
            Keys.CONTROL + 't')  # If using MacOS, Keys.COMMAND + 't'

    def clickOnPosition(self, x, y):
        """
        Click on a specific position
        Args:
            x (int): x_cordinate
            y (int): y_cordinate
        """
        action = ActionChains(self.driver)
        action.move_by_offset(x, y)
        action.perform()

    def dropDownByValue(self, XPATH, value):
        """
        Choose on option from a drop down object
        Args:
            XPATH (string): XPATH of the drop down object
            value (string): the value of that option (Check in DevTool)
        """
        box = self.driver.find_element(By.XPATH, XPATH)
        action = Select(box)
        action.select_by_value(value)
        time.sleep(1)

    def waitForPageLoaded(self, duration=10):
        try:
            WebDriverWait(self.driver, duration).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except TimeoutException:
            pass

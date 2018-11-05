import os
import unittest
from pyunitreport import HTMLTestRunner
from appium import webdriver
import Functions.Todoist_Functions as Todoist
from time import sleep
from todoist.api import TodoistAPI
from configparser import ConfigParser

# instantiate
config = ConfigParser()

# parse ini file
config.read('../test_info.ini')

def setUp(self):
    # read device values
    platformName = config.get('device','platformName')
    deviceName = config.get('device', 'deviceName')
    app = config.get('device', 'app')
    appPackage = config.get('device', 'appPackage')
    appActivity = config.get('device', 'appActivity')
    serverUrl = config.get('device', 'serverUrl')

    # connect to mobile device apps
    desired_caps = {}
    desired_caps['platformName'] = platformName
    desired_caps['deviceName'] = deviceName
    desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), app))
    desired_caps['appPackage'] = appPackage
    desired_caps['appActivity'] = appActivity
    self.driver = webdriver.Remote(serverUrl, desired_caps)

def tearDown(self):
    self.driver.quit()


def Login(self):
    # read users values
    email = config.get('users','email')
    password = config.get('users', 'password')

    Email_button = self.driver.find_element_by_id("com.todoist:id/btn_welcome_continue_with_email")
    Email_button.click()

    Email_tb = self.driver.find_element_by_id("com.todoist:id/email_exists_input")
    Email_tb.send_keys(email)

    ContinueWEmail_button = self.driver.find_element_by_id("com.todoist:id/btn_continue_with_email")
    ContinueWEmail_button.click()

    Password_tb = self.driver.find_element_by_id("com.todoist:id/log_in_password")
    Password_tb.send_keys(password)

    Login_button = self.driver.find_element_by_id("com.todoist:id/btn_log_in")
    Login_button.click()

    self.driver.implicitly_wait(5)

    # Verify if login successfully
    if self.driver.find_element_by_id("com.todoist:id/empty_text") == 0:
        return False

def Verify_CreatedProject(self, projectname):
    current_view = self.driver.find_element_by_accessibility_id("Change the current view")
    current_view.click()

    expand = self.driver.find_element_by_accessibility_id("Expand/collapse")
    expand.click()

    self.driver.implicitly_wait(5)

    # Verify if project created successfully
    if self.driver.find_elements_by_xpath("//*[contains(text(), projectname)]") == 0:
        return False
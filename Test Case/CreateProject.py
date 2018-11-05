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

class Todoist_CreateProject(unittest.TestCase):
    def setUp(self):
        Todoist.setUp(self)

    def tearDown(self):
        Todoist.tearDown(self)

    def test_CreateProject(self):
        #read api token values
        apitoken = config.get('todoistinfo', 'apitoken')

        # read project name
        projectname = config.get('todoistinfo', 'projectname')

        '''
        Create project by using API commands
        '''
        api = TodoistAPI(apitoken)
        api.sync()

        create_project = api.projects.add(projectname)
        response = api.commit()

        # Verify if the project has been created successfully
        assert response['projects'][0]['name'] == projectname
        assert projectname in [p['name'] for p in api.state['projects']]
        assert api.projects.get_by_id(create_project['id']) == create_project

        # update the created project ID to ini file
        config.set("todoistinfo", "projectid", str(create_project['id']))
        config.write(open('../test_info.ini', 'w'))

        #Login to mobile apps and verify the project has been created successfully
        Todoist.Login(self)
        sleep(6)
        Todoist.Verify_CreatedProject(self, projectname)


# ---START OF SCRIPT
if __name__ == '__main__':
    # Report will be generate after done the execution
    suite = unittest.TestLoader().loadTestsFromTestCase(Todoist_CreateProject)
    kwargs = {
        "output": 'TestReport',
        "report_name": 'CreateProjectReport',
        "failfast": True
    }
    runner = HTMLTestRunner(**kwargs)
    runner.run(suite)
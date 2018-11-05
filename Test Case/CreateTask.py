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

class Todoist_CreateTask(unittest.TestCase):
    def setUp(self):
        Todoist.setUp(self)

    def tearDown(self):
        Todoist.tearDown(self)

    def test_CreateTask(self):
        # read api token values
        apitoken = config.get('todoistinfo', 'apitoken')

        # read task name
        taskname = config.get('todoistinfo', 'taskname')

        # read created project ID
        projectid = config.get('todoistinfo', 'projectid')

        '''
        Create task by using API commands
        '''
        api = TodoistAPI(apitoken)
        api.sync()

        create_task = api.items.add(taskname, projectid)
        response = api.commit()

        # Verify if the task has been created successfully
        assert create_task['content'] == taskname, "Task created unsuccessfully."
        assert taskname in [i['content'] for i in api.state['items']]
        assert api.items.get_by_id(create_task['id']) == create_task

        # update the created task ID to ini file
        config.set("todoistinfo", "taskid", str(create_task['id']))
        config.write(open('../test_info.ini', 'w'))
        

# ---START OF SCRIPT
if __name__ == '__main__':
    # Report will be generate after done the execution
    suite = unittest.TestLoader().loadTestsFromTestCase(Todoist_CreateTask)
    kwargs = {
        "output": 'TestReport',
        "report_name": 'CreateTaskReport',
        "failfast": True
    }
    runner = HTMLTestRunner(**kwargs)
    runner.run(suite)

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

class Todoist_ReopenTask(unittest.TestCase):
    def setUp(self):
        Todoist.setUp(self)

    def tearDown(self):
        Todoist.tearDown(self)

    def test_CreateTask(self):
        # read api token values
        apitoken = config.get('todoistinfo', 'apitoken')

        # read created task name
        taskname = config.get('todoistinfo', 'taskname')

        # read created task ID
        taskid = config.get('todoistinfo', 'taskid')

        # Complete Task
        api = TodoistAPI(apitoken)
        api.sync()
        created_task = api.items.get_by_id(int(taskid))
        created_task.complete()
        response = api.commit()

        # Verify if the task has been completed successfully
        assert response['items'][0]['content'] == taskname
        assert response['items'][0]['checked'] == 1
        assert 1 in [i['checked'] for i in api.state['items'] if i['id'] == int(taskid)]

        # Reopen Task
        created_task.uncomplete()
        response = api.commit()

        # Verify if the task has been reopened successfully
        assert response['items'][0]['content'] == taskname
        assert response['items'][0]['checked'] == 0
        assert 0 in [i['checked'] for i in api.state['items'] if i['id'] == int(taskid)]


# ---START OF SCRIPT
if __name__ == '__main__':
    # Report will be generate after done the execution
    suite = unittest.TestLoader().loadTestsFromTestCase(Todoist_ReopenTask)
    kwargs = {
        "output": 'TestReport',
        "report_name": 'ReopenTaskReport',
        "failfast": True
    }
    runner = HTMLTestRunner(**kwargs)
    runner.run(suite)

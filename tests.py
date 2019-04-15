import unittest
import unittest.mock as mock
from unittest.mock import patch
from playhouse.test_utils import test_database
from menus import Menu
from peewee import *
from work_log_entry import WorkLogEntry
from work_log import *

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([WorkLogEntry],safe=True)

DATA = {
    "employee_name": "Nicolas Dhaene",
    "time_spent": 120,
    "task_name": "Birthday",
    "notes": "no notes",
    "date": "11/26/2019"
}

class WorkLogTests(unittest.TestCase):
    @staticmethod
    def create_entries():
    	WorkLogEntry.create(employee=DATA["employee_name"],
						date=datetime.datetime.strptime(DATA["date"], "%m/%d/%Y"),
						task_name=DATA["task_name"],
						time_spent=DATA["time_spent"],
						notes=DATA["notes"])

    def test_is_valid_date(self):
    	self.assertFalse(is_valid_date("cheese"))

    def test_is_valid_integer(self):
    	self.assertFalse(is_valid_integer("26/11/2019"))

    def test_get_employee_name(self):
    	input_args = ["Nicolas Dhaene"]
    	with patch('builtins.input', side_effect=input_args) as mock:
    		result = get_employee_name()
    		self.assertEqual(result, input_args[0])

    def test_get_date(self):
    	input_args = ["11/26/2019"]
    	with patch('builtins.input', side_effect=input_args) as mock:
    		result = get_task_date()
    		self.assertEqual(result, datetime.datetime.strptime(input_args[0], "%m/%d/%Y"))

    def test_get_task_name(self):
    	input_args = ["Birthday"]
    	with patch('builtins.input', side_effect=input_args) as mock:
    		result = get_task_name()
    		self.assertEqual(result, input_args[0])

    def test_get_time_spent(self):
    	input_args = ["120"]
    	with patch('builtins.input', side_effect=input_args) as mock:
    		result = get_time_spent()
    		self.assertEqual(result, int(input_args[0]))

    def test_get_notes(self):
    	input_args = ["notes"]
    	with patch('builtins.input', side_effect=input_args) as mock:
    		result = get_notes()
    		self.assertEqual(result, input_args[0])

    def test_employee(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
    		self.create_entries()
    		with mock.patch('builtins.input',side_effect=["Nicolas Dhaene"]):
    			assert employee().count() == 1
    
    def test_exact_date(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
    		self.create_entries()
    		with mock.patch('builtins.input',side_effect=["11/26/2019"]):
    			assert exact_date().count() == 1

    def test_range_of_dates(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
    		self.create_entries()
    		with mock.patch('builtins.input',side_effect=["12/26/2019","12/28/2019"]):
    			assert range_of_dates().count() == 0
    		with mock.patch('builtins.input',side_effect=["10/26/2019","12/28/2019"]):
    			assert range_of_dates().count() == 1

    def test_task_or_notes(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
    		self.create_entries()
    		with mock.patch('builtins.input',side_effect=["cheese"]):
    			assert task_or_notes().count() == 0
    		with mock.patch('builtins.input',side_effect=["Birthday"]):
    			assert task_or_notes().count() == 1
    		with mock.patch('builtins.input',side_effect=["notes"]):
    			assert task_or_notes().count() == 1

    def test_time_spent(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
    		self.create_entries()
    		with mock.patch('builtins.input',side_effect=["12"]):
    			assert time_spent().count() == 0
    		with mock.patch('builtins.input',side_effect=["120"]):
    			assert time_spent().count() == 1

    def test_check_if_no_result(self):
    	assert check_if_no_result([]) == True

    def test_define_navigation_option(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
            self.create_entries()
            entries = WorkLogEntry.select()
            assert "Previous" not in define_navigation_options(entries,0) 
            assert "Next" not in define_navigation_options(entries,1)

    def test_delete_entry(self):
        with test_database(TEST_DB, (WorkLogEntry,)):
            self.create_entries()
            entry = WorkLogEntry.select().first()
            with mock.patch('builtins.input', side_effect=["y", ""]):
                delete_entry(entry)
                self.assertEqual(WorkLogEntry.select().count(), 0)

    def test_edit_entry(self):
    	with test_database(TEST_DB, (WorkLogEntry,)):
            self.create_entries()
            entry = WorkLogEntry.select().first()
            with mock.patch('builtins.input', side_effect=["n", "n", "n", "n", "y", "new_notes", ""]):
                edit_entry(entry)
                self.assertEqual(entry.notes, "new_notes")

if __name__ == '__main__':
	unittest.main()
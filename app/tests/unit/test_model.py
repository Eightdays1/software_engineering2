import unittest
from tests.base_test import BaseTestCase

from datetime import datetime

from werkzeug.security import check_password_hash


class TestUserModel(BaseTestCase):
    def test_email(self):
        self.assertEqual(self.test_user.email, 'test@test.com')

    def test_password(self):
        self.assertNotEqual(self.test_user.password, 'testpassword')

    def test_first_name(self):
        self.assertEqual(self.test_user.first_name, 'Testname')

    def test_check_password(self):
        self.assertEqual(self.test_user.check_password('falsetestpassword'), False)
        self.assertEqual(self.test_user.check_password('testpassword'), True)

    def test_change_name(self):
        self.test_user.change_name('Newname')
        self.assertNotEqual(self.test_user.first_name, 'Testname')
        self.assertEqual(self.test_user.first_name, 'Newname')

    def test_change_email(self):
        self.assertEqual(self.test_user.change_email('test2@test.com'), True)

    def test_change_password(self):
        self.test_user.change_password('NewTestPassword')
        self.assertEqual(check_password_hash(self.test_user.password, 'NewTestPassword'), True)


class TestGroupModel(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.test_group.name, 'TestGroup')

    def test_change_group_name(self):
        self.test_group.name = 'NewTestGroupName'
        self.assertEqual(self.test_group.name, 'NewTestGroupName')


class TestTaskModel(BaseTestCase):
    def test_title(self):
        self.assertEqual(self.new_task1.title, 'TestTask1')
        self.assertEqual(self.new_task2.title, 'TestTask2')

    def test_data(self):
        self.assertEqual(self.new_task1.data, 'TestData1')
        self.assertEqual(self.new_task2.data, 'TestData2')

    def test_date(self):
        self.assertEqual(self.new_task1.date, None)
        self.assertEqual(self.new_task2.date, self.date)

    def test_state(self):
        self.assertEqual(self.new_task1.state, True)
        self.assertEqual(self.new_task2.state, False)

    def test_group_id(self):
        self.assertEqual(self.new_task1.group_id, self.test_group.id)
        self.assertEqual(self.new_task2.group_id, self.test_group.id)

    def test_user_id(self):
        self.assertEqual(self.new_task1.user_id, None)
        self.assertEqual(self.new_task2.user_id, self.test_user.id)


class TestNoteModel(BaseTestCase):
    def test_data(self):
        self.assertEqual(self.new_note1.data, 'TestData1')

    def test_group_id(self):
        self.assertEqual(self.new_note1.group_id, self.test_group.id)


class TestItemModel(BaseTestCase):
    def test_title(self):
        self.assertEqual(self.new_item1.title, 'TestItem')
        self.assertEqual(self.new_item2.title, 'TestItem2')

    def test_group_id(self):
        self.assertEqual(self.new_item1.group_id, self.test_group.id)
        self.assertEqual(self.new_item2.group_id, self.test_group.id)

    def test_state(self):
        self.assertEqual(self.new_item1.state, False)
        self.assertEqual(self.new_item2.state, True)


class TestEventModel(BaseTestCase):
    def test_title(self):
        self.assertEqual(self.new_event.title, 'TestEvent')
        self.assertEqual(self.new_event1.title, 'TestEvent1')

    def test_group_id(self):
        self.assertEqual(self.new_event.group_id, self.test_group.id)
        self.assertEqual(self.new_event1.group_id, self.test_group.id)

    def test_user_id(self):
        self.assertEqual(self.new_event.user_id, self.test_user.id)
        self.assertEqual(self.new_event1.user_id, None)

    def test_start(self):
        self.assertEqual(self.new_event.start, self.date)
        self.assertEqual(self.new_event1.start, self.date)

    def test_end(self):
        self.assertEqual(self.new_event.end, self.date)
        self.assertEqual(self.new_event1.end, self.date)

    def test_repeat(self):
        self.assertEqual(self.new_event.repeat, 2)
        self.assertEqual(self.new_event1.repeat, 1)

    def test_repeat_till(self):
        self.assertEqual(self.new_event.repeat_till, datetime(2022, 7, 26, 0, 0))
        self.assertEqual(self.new_event1.repeat_till, datetime(2022, 7, 26, 0, 0))

    def test_color(self):
        self.assertEqual(self.new_event.color, '#401902')
        self.assertEqual(self.new_event1.color, 'green')


if __name__ == '__main__':
    unittest.main()

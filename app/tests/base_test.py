import unittest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from website.config import TestConfig
from flask_login import LoginManager, login_user, current_user

from website import db, create_app
from website.models import User, Group, Note, Item, Event, Task
from datetime import datetime


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        self.date = datetime.now()
        db.create_all()
        self.test_user = User(email='test@test.com', password=generate_password_hash('testpassword', method='sha256'),
                              first_name='Testname')
        db.session.add(self.test_user)
        self.test_group = Group(name='TestGroup')
        db.session.add(self.test_group)
        self.test_user.group_id = self.test_group.id
        db.session.commit()
        self.new_item1 = Item(title='TestItem', group_id=self.test_group.id, state=False)
        self.new_item2 = Item(title='TestItem', group_id=self.test_group.id, state=True)
        db.session.add_all([self.new_item1, self.new_item2])
        db.session.commit()
        self.new_event = Event(title='TestEvent1', group_id=self.test_group.id, user_id=self.test_user.id, repeat=2,
                               repeat_till=datetime(2022, 7, 26, 0, 0), start=self.date, end=self.date, color='#401902')
        self.new_event1 = Event(title='TestEvent2', group_id=self.test_group.id, repeat=1,
                                repeat_till=datetime(2022, 7, 26, 0, 0), start=self.date, end=self.date, color='green')
        db.session.add_all([self.new_event, self.new_event1])
        db.session.commit()

        self.new_task1 = Task(title='TestTask1', group_id=self.test_group.id,
                              data='TestData1', state=True)
        self.new_task2 = Task(title='TestTask2', group_id=self.test_group.id,
                              data='TestData2', user_id=self.test_user.id, date=self.date)
        db.session.add_all([self.new_task1, self.new_task2])
        db.session.commit()

        self.new_note1 = Note(data="TestData1", group_id=self.test_group.id)
        db.session.add(self.new_note1)
        db.session.commit()

        login_user(self.test_user, remember=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

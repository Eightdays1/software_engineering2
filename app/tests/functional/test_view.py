import unittest
import flask_unittest
import flask.globals
from datetime import datetime
from datetime import timedelta
from website.views import views

from website.models import Note, Item, Group, User, Event, Task
from website import db


class test_view(unittest.TestCase):
    def test_days_till(self):
        now = datetime.now()
        date_in_8_days = now + timedelta(days=8)
        result = views.days_till(date_in_8_days)
        self.assertEqual(result, 8)


if __name__ == '__main__':
    unittest.main()

import unittest
from main import app
from tests.base_test import BaseTestCase


class TestAuth(BaseTestCase):
    def test_sign_up(self):
        response = self.tester.get('/sign-up')
        self.assertEqual(response.status_code, 200)
        form = {'email': 'test2@test.com', 'firstName': 'Test_User',
                'password1': 'Password_1', 'password2': 'Password_1',}
        response = self.tester.post('/sign-up', data=form)
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.tester.get('/login')
        self.assertEqual(response.status_code, 200)
        form = {'email': 'test1@test.com', 'password': 'testpassword1'}
        response = self.tester.post('/login', data=form)
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.tester.get('/logout')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()

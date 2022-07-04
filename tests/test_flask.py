import unittest
from main import app


class FlaskTestCase(unittest.TestCase):
    # Testing if apps builds
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_auth_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Testing login cases
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email="test@gmail.com", password="Test123!@#"),
                               follow_redirects=True)
        self.assertIn(b'Logged in', response.data)

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email="wrong@gmail.com", password="Wrong123!@#"),
                               follow_redirects=True)
        self.assertIn(b'Email does not exist.', response.data)

    def test_incorrect_passwd(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email="test@gmail.com", password="Wrong123!@#000"),
                               follow_redirects=True)
        self.assertIn(b'Incorrect password, try again.', response.data)

    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email="test@gmail.com", password="Test123!@#"),
                               follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_logout_needs_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    # Testing protected routes
    def test_assets_page_needs_login(self):
        tester = app.test_client(self)
        response = tester.get('/assets', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    def test_configuration_page_needs_login(self):
        tester = app.test_client(self)
        response = tester.get('/configuration', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    def test_reports_page_needs_login(self):
        tester = app.test_client(self)
        response = tester.get('/reports', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    # Test config forms
    def test_configuration_form_one(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email="test@gmail.com", password="Test123!@#"),
                               follow_redirects=True)
        response = tester.post('/configuration',
                               data=dict(ip_address='192.168.0.1', admin_login='admin', admin_password='admin'),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configuration updated!', response.data)

    def test_configuration_form_two(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(email="test@gmail.com", password="Test123!@#"),
                               follow_redirects=True)
        response = tester.post('/configuration',
                               data=dict(email_account='test@gmail.com', email_account_password='Test123!@#',
                                         smtp_email_account='smtp.gmail.com', email_account_port='587',
                                         monitoring_server_ip='192.168.0.59'),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configuration updated', response.data)


if __name__ == '__main__':
    unittest.main()

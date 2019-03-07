from django.test import TestCase
from django.contrib.auth.models import User


class AuthTestCase(TestCase):
    def test_signup(self):
        post_body_u1 = {
            "username": "test",
            "email": "test@gmail.com",
            "password": "123456",
        }
        response = self.client.post(
            '/auth/signup', post_body_u1, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        # print(response.data)
        test_user = User.objects.get(username="test")
        self.assertTrue(test_user.check_password("123456"))
        self.assertFalse(test_user.is_active)
        self.assertEqual(test_user.username, "test")
        self.assertEqual(test_user.email, "test@gmail.com")

        # log in with right password, but not be verified by admin
        login = self.client.login(username='test', password='123456')
        self.assertFalse(login)

        # activate author
        test_user.is_active = True
        test_user.save()

        # log in with right password
        login = self.client.login(username='test', password='123456')
        self.assertTrue(login)

        #  log in with wrong password
        login = self.client.login(username='test', password='12356')
        self.assertFalse(login)

        # sign up with wrong format
        post_body_u2 = {
            "username": "test2",
            "email": "sfds",
            "password": "123456",
        }
        response = self.client.post(
            '/auth/signup', post_body_u2, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # print(response.data)

from django.test import TestCase, Client
from django.urls import reverse
from .models import User


def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    activate_user(user)
    return user


def comfirm_site_rules(user):
    user.is_rules_confirmed = True
    user.save()
    return user


def activate_user(user):
    user.is_active = True
    user.save()
    return user


def create_activated_test_user():
    user = create_user(username='test', email='test@eis.hokudai.ac.jp', password='test1234')
    activate_user(user)
    return user


class JWTCreateViewTest(TestCase):
    def test_login_using_email(self):
        user = create_user(username='test', email='test@hokudai.ac.jp', password='password')
        data = {"email": user.email, "password": 'password'}
        response = self.client.post(reverse('jwt-create'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['access'],'')
        self.assertNotEqual(response.data['refresh'],'')

    def test_login_using_username(self):
        user = create_user(username='test', email='test@hokudai.ac.jp', password='password')
        data = {"username": user.username, "password": 'password'}
        response = self.client.post(reverse('jwt-create'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['access'],'')
        self.assertNotEqual(response.data['refresh'],'')


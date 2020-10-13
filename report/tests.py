from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Report
from account.tests import *


class ReportTests(APITestCase):
    def test_create_report(self):
        account_data = [
                {
                    'username': 'test1',
                    'email': 'test1@eis.hokudai.ac.jp',
                    'password': 'hokuma1'
                },
                {
                    'username': 'test2',
                    'email': 'test2@eis.hokudai.ac.jp',
                    'password': 'hokuma2'

                }
            ]

        reporting_user = create_user(account_data[0]['username'], account_data[0]['email'], account_data[0]['password'])
        reporting_user = activate_user(reporting_user)
        reporting_user = comfirm_site_rules(reporting_user)

        reported_user = create_user(account_data[1]['username'], account_data[1]['email'], account_data[1]['password'])
        reported_user = activate_user(reported_user)
        reported_user = comfirm_site_rules(reported_user)

        url = reverse('report-list')
        data = {'reporting_user_id': reporting_user.id,
                'reported_user_id': reported_user.id,
                'content': 'test'
                }

        self.client.login(username=account_data[0]['username'], password=account_data[0]['password'])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': '通報が完了しました。'})



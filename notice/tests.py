from rest_framework.test import APITestCase
from .models import Notice, UnreadNoticeCount
from .utils import create_notice
from account.tests import create_activated_test_user
from django.urls import reverse
from rest_framework import status


class NoticeTests(APITestCase):
    def test_create_notice(self):
        user = create_activated_test_user()
        data1 = {
                'recieved_user': user,
                'body':'テスト用のお知らせです。',
                'image_url':'http://design-ec.com/d/e_others_50/m_e_others_501.jpg',
                'link':'https://twitter.com/matchingstudy'}
        data2 = {
            'recieved_user': user,
            'body':'二つ目のテストお知らせです。',
            'image_url':'http://design-ec.com/d/e_others_50/m_e_others_501.jpg',
            'link':'https://twitter.com/matchingstudy'}
        _, _ = create_notice(recieved_user=data1['recieved_user'], body=data1['body'],
                                                        image_url=data1['image_url'],
                                                        link=data1['link'])
        _, my_unread_notice_count_model = create_notice(recieved_user=data2['recieved_user'], body=data2['body'],
                                                             image_url=data2['image_url'],
                                                             link=data2['link'])
        self.assertEqual(my_unread_notice_count_model.count, 2)

        self.client.force_login(user=user)

        response = self.client.get(reverse('notice:fetch_my_notice_list'), format='json')

        # 最新の日付から順になっているか？
        self.assertEqual(response.data[0]['recieved_user'], data2['recieved_user'].id)
        self.assertEqual(response.data[0]['body'], data2['body'])
        self.assertEqual(response.data[0]['image_url'], data2['image_url'])
        self.assertEqual(response.data[0]['link'], data2['link'])
        self.assertEqual(response.data[1]['recieved_user'], data1['recieved_user'].id)
        self.assertEqual(response.data[1]['body'], data1['body'])
        self.assertEqual(response.data[1]['image_url'], data1['image_url'])
        self.assertEqual(response.data[1]['link'], data1['link'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_my_unread_notice_count(self):
        user = create_activated_test_user()
        _, my_unread_notice_count_model = create_notice(recieved_user=user, body='テスト用のお知らせです。',
                      image_url='http://design-ec.com/d/e_others_50/m_e_others_501.jpg',
                      link='https://twitter.com/matchingstudy')
        self.assertEqual(my_unread_notice_count_model.count, 1)

        self.client.force_login(user=user)

        response = self.client.post(reverse('notice:reset_my_unread_notice_count'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        my_unread_notice_count = UnreadNoticeCount.objects.filter(user=user).first().count
        self.assertEqual(my_unread_notice_count, 0)

    def test_fetch_my_unread_notice_count(self):
        user = create_activated_test_user()
        _, my_unread_notice_count_model = create_notice(recieved_user=user, body='テスト用のお知らせです。',
                                                        image_url='http://design-ec.com/d/e_others_50/m_e_others_501.jpg',
                                                        link='https://twitter.com/matchingstudy')
        self.client.force_login(user=user)

        response = self.client.get(reverse('notice:fetch_my_unread_notice_count'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['unread_notice_count'], 1)

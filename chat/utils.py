from firebase_messaging.utils import send_fcm
from notice.utils import create_notice
from account.models import User


def notify_talk_recieve(sender:User, reciever:User):
    message = sender.username+'さんからメッセージが届いています。'
    sender_image_url = sender.icon.thumbnail['300x300'] if sender.icon is not None else 'http://design-ec.com/d/e_others_50/m_e_others_501.jpg'
    create_notice(recieved_user=reciever, body=message, image_url=sender_image_url, link='')
    send_fcm(title='お知らせ', body=message, reciever=reciever)

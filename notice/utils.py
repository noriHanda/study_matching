from account.models import User
from .models import UnreadNoticeCount, Notice


def create_notice(recieved_user: User, body: str, image_url: str, link: str):
    notice = Notice.objects.create(recieved_user=recieved_user, body=body, image_url=image_url, link=link)
    unread_notice_count_model = increment_unread_notice_count(user=recieved_user)
    return notice, unread_notice_count_model


def increment_unread_notice_count(user: User):
    unread_notice_count_model = UnreadNoticeCount.objects.filter(user=user).first()
    if unread_notice_count_model is None:
        unread_notice_count_model = UnreadNoticeCount.objects.create(user=user)
    unread_notice_count_model.increment()
    return unread_notice_count_model

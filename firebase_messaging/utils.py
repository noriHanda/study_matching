import firebase_admin
from firebase_admin import messaging, credentials
from django.conf import settings
from .models import FCMDeviceToken

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def initialize_firebase_admin_sdk():
    cred = credentials.Certificate(settings.FIREBASE_CERTIFICATE)
    if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
        firebase_admin.initialize_app(cred)


# TODO: エラーハンドリング
def send_fcm(title, body, reciever):
    initialize_firebase_admin_sdk()
    firebase_admin.get_app()
    notification = messaging.Notification(title=title, body=body)
    print(reciever)
    tokens = FCMDeviceToken.objects.filter(user=reciever)
    # token = settings.FIREBASE_TEST_TOKEN  # local_settings.py
    if tokens is not None:
        for token in tokens:
            apns = messaging.APNSConfig(payload=messaging.APNSPayload(aps=messaging.Aps(badge=1)))
            message = messaging.Message(
                notification=notification,
                apns=apns,
                token=token.device_token,
            )
            try:
                messaging.send(message)
                logger.info('fcm ok')
                print('fcm ok')
            except:
                print('error')
                logger.error('fcm sending error')
                pass

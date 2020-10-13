from rest_framework_simplejwt import views
from rest_framework_simplejwt import serializers
from rest_framework import serializers as drf_serializers
from rest_framework import exceptions
from collections import OrderedDict
from .models import User


def get_username_from_email(email):
    return User.objects.get(email=email).username


class CustomJWTTokenSerializer(serializers.TokenObtainPairSerializer):
    """
    Djoser（が使っているsimplejwtモジュール）ではusername, passwordのみでの認証にしか対応していない
    そのため、カスタムシリアライザを以下のように作成しemailとusernameのどちらでもログインできるように変更した
    EmailとUsernameのどちらかさえリクエストから受け取れればエラーは返さないが、
    どちらも受け取れなかった場合は{"username": ["この項目は空にできません。"]を返すようになっている点に注意
    """
    def __init__(self, *args, **kwargs):
        self.fields['email'] = drf_serializers.EmailField(required=False, allow_blank=True)
        new_kwargs = kwargs.copy()
        if 'data' in kwargs.keys():
            if 'email' not in kwargs['data'].keys():
                super().__init__(*args, **kwargs)
            else:
                if 'username' in kwargs['data'].keys() and kwargs['data']['username'] == '' \
                or 'username' not in kwargs['data'].keys():
                    data = kwargs['data'].copy()
                    data['username'] = kwargs['data']['email']
                    new_kwargs.update({'data': data})
                    super().__init__(*args, **new_kwargs)
        super().__init__(*args, **new_kwargs)

    def validate(self, attrs):
        if 'email' in attrs.keys() and attrs['email']:
            try:
                username = get_username_from_email(attrs['email'])
            except:
                raise exceptions.AuthenticationFailed(
                    {'email_do_not_match_user': '入力されたメールアドレスに一致するユーザが見つかりませんでした'},
                    'email_do_not_match_user'
                )
        else:
            username = attrs['username']
        username_password_attrs = OrderedDict({'username': username, 'password': attrs['password']})
        data = super().validate(username_password_attrs)
        print(data)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CustomJWTTokenView(views.TokenObtainPairView):
    serializer_class = CustomJWTTokenSerializer

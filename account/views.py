from rest_framework import viewsets
from rest_framework.views import APIView

from .models import User
from .serializers import RestrictedUserSerializer, MyUserSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import requests

from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from .forms import PasswordResetForm


class UserViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser)

    queryset = User.objects.all()
    serializer_class = RestrictedUserSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None, *args, **kwargs):
        if request.user.id == int(pk):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを変更することはできません。'})

    def update(self, request, pk=None, *args, **kwargs):
        # 上のparser class により、headerによって処理を分岐
        if request.user.id == int(pk):
            if request.data.get('file') is not None:
                existed_user = get_object_or_404(User, id=request.user.id)
                user_serializer = MyUserSerializer(existed_user, data={'icon': request.data['file']}, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response(user_serializer.data)
                else:
                    print(user_serializer.errors)
                    return Response(status=400)
            else:
                # JsonParserでfile以外のパラメータをアップロード
                return super().update(request, *args, **kwargs)
        else:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを変更することはできません。'})


class UserActivationView(APIView):
    def get (self, request, uid, token):
        web_url = 'http://127.0.0.1:3001' # request.get_host()
        post_url = web_url + "/api/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        try:
            result = requests.post(post_url, data=post_data, timeout=1)
            status_code = result.status_code
            if status_code == 204:
                return render(request, 'custom_email/activation_success.html', status=200)
            else:
                return render(request, 'custom_email/activation_failure.html', status=400)
        except requests.Timeout:
            return render(request, 'custom_email/activation_failure.html', status=401)
        except requests.ConnectionError:
            return render(request, 'custom_email/activation_failure.html', status=402)


def password_reset_form_page(request, uid=None, token=None):
    status_code = 200
    result = None
    if request.method == 'GET':
        if uid is not None and token is not None:
            form = PasswordResetForm(uid=uid, token=token)
            return render(request, 'custom_email/password_reset_form_page.html', {'uid': uid, 'token': token, 'form': form}, status=200)
        else:
            return render(request, 'custom_email/password_reset_error.html', status=400)
    elif request.method == 'POST':
        form = PasswordResetForm(uid=None, token=None, data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            #protocol = 'https://' if request.is_secure() else 'http://'
            #web_url = protocol + 'localhost:3000' # request.get_host()
            web_url = 'http://127.0.0.1:3001' # request.get_host()
            post_url = web_url + "/api/auth/users/reset_password_confirm/"
            post_data = {'uid': cleaned_data['uid'], 'token': cleaned_data['token'], 'new_password': cleaned_data['new_password'], 're_new_password': cleaned_data['re_new_password']}
            try:
                result = requests.post(post_url, data=post_data, timeout=1)
                status_code = result.status_code
                if status_code == 204:
                    return render(request, 'custom_email/password_changed_confirmation.html', status=200)
                else:
                    return render(request, 'custom_email/password_reset_form_page.html', {'uid': uid, 'token': token, 'form': form, 'error_dict': result.json()}, status=200)
            except requests.Timeout:
                return render(request, 'custom_email/password_reset_form_page.html', {'uid': uid, 'token': token, 'form': form, 'error_dict': result.json()}, status=200)
                #return render(request, 'custom_email/password_reset_error.html', status=status_code)
            except requests.ConnectionError:
                return render(request, 'custom_email/password_reset_form_page.html', {'uid': uid, 'token': token, 'form': form, 'error_dict': result.json()}, status=200)
                #return render(request, 'custom_email/password_reset_error.html', status=status_code)

    return render(request, 'custom_email/password_reset_error.html', status=400)

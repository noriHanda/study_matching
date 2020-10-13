from django import forms
from django.utils.safestring import mark_safe


class PasswordResetForm(forms.Form):
    uid = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())
    new_password = forms.CharField(label='新しいパスワード',
                                   widget=forms.PasswordInput())
    re_new_password = forms.CharField(label='新しいパスワード（確認用）',
                                      help_text=mark_safe('<p><ul>'
                                             '<li>メールアドレス・ユーザ名と酷似したパスワードを使用しないでください。</li>'
                                             '<li>半角で英数字の両方を含めた８文字以上を入力してください。</li>'
                                             '<li>一般的で予測されやすいパスワードを使わないでください。</li>'
                                             '</ul></p>'),
                                      widget=forms.PasswordInput())

    def __init__(self,*args,**kwargs):
        self._uid = kwargs.pop('uid')
        self._token = kwargs.pop('token')
        super(PasswordResetForm,self).__init__(*args,**kwargs)
        self.fields['uid'].initial = self._uid
        self.fields['token'].initial = self._token


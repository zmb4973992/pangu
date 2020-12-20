from django import forms


def validator1():
    return True


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, min_length=3, label='用户名',
                               error_messages={'required': '需要填写用户名', 'min_length': '太短了！'},
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

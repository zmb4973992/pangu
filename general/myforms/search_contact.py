from django import forms
from general import models


class SearchContactForm(forms.Form):
    vendor = forms.CharField(label='供应商',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '请填写供应商全称或简称，可以不填，支持模糊搜索'}))
    name = forms.CharField(label='姓名',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': '请填写联系人姓名，可以不填，支持模糊搜索'}))



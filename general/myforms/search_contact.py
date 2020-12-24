from django import forms
from general import models


class SearchContactForm(forms.Form):
    vendor = forms.CharField(label='供应商',
                             required=False,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '供应商全称或简称，可以不填，支持模糊搜索'}))
    name = forms.CharField(label='姓名',
                           required=False,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': '联系人姓名，可以不填，支持模糊搜索'}))

    def clean(self):
        vendor = self.cleaned_data.get('vendor')
        name = self.cleaned_data.get('name')
        if not vendor and not name:
            self.add_error('vendor', '必须填写至少一项')
            self.add_error('name', '必须填写至少一项')
        else:
            return self.cleaned_data

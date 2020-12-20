from django import forms

from general import models


# validator+ 抛异常，更适合cleaned_data以外的错误
# def name_not_found(value):
#     if not Vendor.objects.filter(Q(name__contains=value) | Q(address__contains=value)):
#         raise ValidationError('没有这个name值')

class ContactForm(forms.Form):
    name = forms.CharField(label='姓名', error_messages={'required': '必须填写姓名'})
    vendor_id = forms.CharField(label='供应商', required=True, error_messages={'required': '必须选择供应商'})
    department = forms.CharField(label='部门', required=False)
    title = forms.CharField(max_length=20, label='职务', required=False)
    landline = forms.CharField(max_length=20, label='座机号', required=False)
    mobile = forms.CharField(max_length=15, label='手机号', required=False)
    email = forms.EmailField(max_length=30, label='邮箱', required=False)
    qq = forms.CharField(max_length=20, required=False)
    wechat = forms.CharField(max_length=25, label='微信', required=False)
    remark = forms.CharField(label='备注', widget=forms.Textarea, required=False)

    def clean_name(self):

        if '666' in self.cleaned_data.get('name'):
            self.add_error('name', '禁止666')
            # raise forms.ValidationError('禁止666')
        else:
            return self.cleaned_data.get('name')

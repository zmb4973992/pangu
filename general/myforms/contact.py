from django import forms
from general import models


# validator+ 抛异常，更适合cleaned_data以外的错误
# def name_not_found(value):
#     if not Vendor.objects.filter(Q(name__contains=value) | Q(address__contains=value)):
#         raise ValidationError('没有这个name值')



class ContactForm(forms.Form):
    name = forms.CharField(label='姓名', required=True, error_messages={'required': '请填写姓名'}, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请填写姓名'}))
    # choice的格式为[(1,'a'),(3,'b'),...]
    vendor_id = forms.ChoiceField(label='供应商', required=True, error_messages={'required': '请选择对应的供应商'})
    department = forms.CharField(label='部门', required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': '请填写部门，没有的话可以不填'}))
    title = forms.CharField(max_length=20, label='职务', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请填写职务，没有的话可以不填'}))
    landline = forms.CharField(max_length=20, label='座机号', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请填写座机，没有的话可以不填'}))
    mobile = forms.CharField(max_length=15, label='手机号', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号码，没有的话可以不填'}))
    email = forms.EmailField(max_length=30, label='邮箱', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请填写邮箱，没有的话可以不填'}))
    qq = forms.CharField(max_length=20, required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请填写QQ，没有的话可以不填'}))
    wechat = forms.CharField(max_length=25, label='微信', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请填写微信，没有的话可以不填'}))
    remark = forms.CharField(label='备注', required=False,
                             widget=forms.Textarea(
                                 attrs={'class': 'form-control', 'placeholder': '请填写备注，没有的话可以不填', 'rows': '2'}))

    def clean_name(self):

        if '666' in self.cleaned_data.get('name'):
            self.add_error('name', '禁止666')
            # raise forms.ValidationError('禁止666')
        else:
            return self.cleaned_data.get('name')

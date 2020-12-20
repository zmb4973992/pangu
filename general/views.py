from django import views
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from general import models
from general.myforms.contact import ContactForm
from general.myforms.login import LoginForm
from general.models import UserInformation


class LoginView(views.View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_obj = auth.authenticate(request, username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)
                return redirect('home')  # 不带参数时可以省略reverse
            else:
                return render(request, 'login.html', locals())

        else:
            return render(request, 'login.html', locals())


class LogoutView(views.View):
    def get(self, request):
        auth.logout(request)
        form = LoginForm()
        return render(request, 'login.html', locals())


@method_decorator(login_required, name='dispatch')
class HomeView(views.View):
    def get(self, request):
        return render(request, '1.html')


class Test(views.View):
    def get(self, request):
        UserInformation.objects.create_user(username='bbb', password='bbbb')
        return HttpResponse('ok')


class TestTemplate(views.View):
    def get(self, request):
        return render(request, 'test.html', locals())


class Order(views.View):
    def get(self, request, short_order_number):
        order_list = models.Order.objects.filter(short_order_number=short_order_number)
        vendor_obj = order_list.first().vendor
        contact_list = vendor_obj.contact_set.all()
        return render(request, 'test1.html', locals())


class Add(views.View):
    def get(self, request):
        print(request.POST)
        form = ContactForm()
        vendor_list = models.Vendor.objects.all()

        return render(request, 'add_contact_test.html', locals())

    def post(self, request):
        print(request.POST)
        form = ContactForm(request.POST)


        if form.is_valid():
            # 如果是form里的数据，就到cleaned_data里找；
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            title = form.cleaned_data.get("title")
            landline = form.cleaned_data.get('landline')
            mobile = form.cleaned_data.get('mobile')
            email = form.cleaned_data.get("email")
            qq = form.cleaned_data.get('qq')
            wechat = form.cleaned_data.get('wechat')
            # 如果没有经过form验证，就直接从request.POST里取；
            vendor_id = request.POST.get('vendor_id')
            remark = form.cleaned_data.get('remark')
            print(vendor_id)
            # models.Contact.objects.create(name=name,  vendor_id=vendor_id)
            return HttpResponse('post成功')

        else:
            return render(request, 'add_contact_test.html', locals())

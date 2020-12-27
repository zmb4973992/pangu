from django import views
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from general import models
from general.myforms.contact import ContactForm
from general.myforms.login import LoginForm
from general.models import UserInformation

# 获取供应商清单，给choice使用，格式为[(1,'a'),(3,'b'),...]
from general.myforms.search_contact import SearchContactForm


def get_vendor_list():
    response = []
    for obj in models.Vendor.objects.all():
        if obj.chinese_short_name:
            response += [(obj.id, str(obj.chinese_short_name) + ' -- ' + str(obj.chinese_full_name))]
        else:
            response += [(obj.id, str(obj.english_short_name) + ' -- ' + str(obj.english_full_name))]
    return response


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


@method_decorator(login_required, name='dispatch')
class LogoutView(views.View):
    def get(self, request):
        auth.logout(request)
        form = LoginForm()
        return render(request, 'login.html', locals())


@method_decorator(login_required, name='dispatch')
class HomeView(views.View):
    def get(self, request):
        return render(request, 'home.html')


class Test(views.View):
    def get(self, request):
        UserInformation.objects.create_user(username='bbb', password='bbbb')
        return HttpResponse('ok')


class TestTemplate(views.View):
    def get(self, request):
        return render(request, 'test.html', locals())


@method_decorator(login_required, name='dispatch')
class Order(views.View):
    def get(self, request, short_order_number):
        order_list = models.Order.objects.filter(short_order_number=short_order_number)
        vendor_obj = order_list.first().vendor
        contact_list = vendor_obj.contact_set.all()
        return render(request, 'test1.html', locals())


@method_decorator(login_required, name='dispatch')
class AddContact(views.View):

    # 重写vendor_id的取值方法(只能用于choice，因为是iterable)这个函数有问题，暂时没有引用
    # def get_vendorid(self, request):
    #     r = []
    #     for obj in models.Vendor.objects.all():
    #         if obj.chinese_short_name:
    #             r += [(obj.id, obj.chinese_short_name + '--' + obj.chinese_full_name)]
    #         else:
    #             r += [(obj.id, obj.english_short_name + '--' + obj.english_full_name)]
    #     return r

    def get(self, request):
        form = ContactForm()
        # 获取到form以后，要重新定义choice方法（选项），否则前端传参回来无法通过验证
        form.fields['vendor_id'].choices = get_vendor_list()
        # vendor_list = models.Vendor.objects.all()
        # values = models.Vendor.objects.all().values()
        # values_list = models.Vendor.objects.all().values_list()
        # print(values)

        return render(request, 'add_contact.html', locals())

    def post(self, request):
        # vendor_list = models.Vendor.objects.all()
        form = ContactForm(request.POST)
        # 获取到form以后，要重新定义choice方法（选项），否则前端传参回来无法通过验证
        form.fields['vendor_id'].choices = get_vendor_list()
        # 获取联系人的vendor_id，用来传给前端模板，一定要加int，不然前端总有str、int转换的问题
        if request.POST.get('vendor_id'):
            vendor_id_extracted_from_request = int(request.POST.get('vendor_id'))

        if form.is_valid():
            # 如果是form里的数据，就到cleaned_data里找；
            # 如果没有经过form验证，就直接从request.POST里取；
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            title = form.cleaned_data.get("title")
            landline = form.cleaned_data.get('landline')
            mobile = form.cleaned_data.get('mobile')
            email = form.cleaned_data.get("email")
            qq = form.cleaned_data.get('qq')
            wechat = form.cleaned_data.get('wechat')
            vendor_id = form.cleaned_data.get('vendor_id')
            remark = form.cleaned_data.get('remark')
            last_reviser = request.user.username
            created_by = request.user.username
            models.Contact.objects.create(name=name, department=department, title=title, landline=landline,
                                          mobile=mobile, email=email, qq=qq, wechat=wechat, vendor_id=vendor_id,
                                          remark=remark, last_reviser=last_reviser, created_by=created_by)

            return HttpResponse('添加成功！')

        else:
            return render(request, 'add_contact.html', locals())


@method_decorator(login_required, name='dispatch')
class EditContact(views.View):
    # 定义get路径
    def get(self, request, contact_id):
        # 生成默认的form表单，用于以后post验证。这里全部是空值
        form = ContactForm()
        contact_id = int(contact_id)
        # 从数据库取出所有的供应商，给填表时提供选项
        vendor_list = models.Vendor.objects.all()
        # 根据前端传来的联系人id值，从数据库中获取对应的单条信息，用于填充到表格
        contact_obj = models.Contact.objects.get(id=contact_id)
        # 获取联系人的vendor_id，用来传给前端模板，一定要加int，不然前端总有str、int转换的问题
        vendor_id_of_contact_obj = int(models.Contact.objects.get(id=contact_id).vendor_id)
        return render(request, 'edit_contact_get.html', locals())

    def post(self, request, contact_id):
        vendor_list = models.Vendor.objects.all()
        # 对post传来的参数赋值给form，如果能通过就提交，不能通过也有下面的参数传回给前端
        form = ContactForm(request.POST)
        form.fields['vendor_id'].choices = get_vendor_list()
        # 这是给前端url的参数
        contact_id = int(contact_id)
        # post方法下，需要获取用户刚刚输入的post信息，必须自己提取。
        # 因为可能无效，导致is_valid为false，后面传参失败
        vendor_id = int(request.POST.get('vendor_id'))
        name = request.POST.get('name')
        department = request.POST.get('department')
        title = request.POST.get('title')
        landline = request.POST.get('landline')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        qq = request.POST.get('qq')
        wechat = request.POST.get('wechat')
        remark = request.POST.get('remark')
        last_reviser = request.user.username

        if form.is_valid():
            models.Contact.objects.filter(id=contact_id).update(name=name, department=department, title=title,
                                                                landline=landline,
                                                                mobile=mobile, email=email, qq=qq, wechat=wechat,
                                                                remark=remark,
                                                                vendor_id=vendor_id, last_reviser=last_reviser)
            return HttpResponse('成功')

        else:
            return render(request, 'edit_contact_post.html', locals())


@method_decorator(login_required, name='dispatch')
class SearchContact(views.View):
    def get(self, request):
        form = SearchContactForm()

        return render(request, 'search_contact_test.html', locals())

    def post(self, request):
        form = SearchContactForm(request.POST)

        return render(request, 'search_contact.html', locals())


@method_decorator(login_required, name='dispatch')
class ContactAll(views.View):
    def get(self, request):
        form = models.Contact.objects.all().order_by('vendor__chinese_short_name', 'vendor__english_short_name')
        new_form = JsonResponse(form, safe=False)
        print(new_form)

        return render(request, 'contact_all_test.html', locals())

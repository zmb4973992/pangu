from django.db import models
from django.contrib.auth.models import AbstractUser

# 供应商信息
from django.utils import timezone


class Vendor(models.Model):
    chinese_short_name = models.CharField(max_length=50, verbose_name='中文简称', blank=True, null=True)
    chinese_full_name = models.CharField(max_length=100, verbose_name='中文全称', blank=True, null=True)
    english_short_name = models.CharField(max_length=50, verbose_name='英文简称', blank=True, null=True)
    english_full_name = models.CharField(max_length=100, verbose_name='英文全称', blank=True, null=True)
    chinese_address = models.CharField(max_length=100, verbose_name='中文地址', blank=True, null=True)
    english_address = models.CharField(max_length=100, verbose_name='英文地址', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    remark = models.TextField(max_length=500, verbose_name='备注', default='无')

    class Meta:
        verbose_name = '供应商信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chinese_short_name or self.english_short_name


# 供应商联系人信息
class Contact(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    department = models.CharField(max_length=20, verbose_name='部门', null=True)
    title = models.CharField(max_length=20, verbose_name='职务', blank=True, null=True)
    landline = models.CharField(max_length=20, verbose_name='座机号', blank=True, null=True)
    mobile = models.CharField(max_length=15, verbose_name='手机号', blank=True, null=True)
    email = models.CharField(max_length=30, verbose_name='邮箱', blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=25, verbose_name='微信', blank=True, null=True)
    vendor = models.ForeignKey(to=Vendor, on_delete=models.PROTECT)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    remark = models.TextField(max_length=500, verbose_name='备注', default='无')
    last_reviser = models.CharField(max_length=20, verbose_name='最后修改人', blank=True, null=True)
    created_by = models.CharField(max_length=20, verbose_name='创建人', blank=True, null=True)
    test = models.CharField(max_length=11, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        verbose_name = '供应商联系人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ContactMsn(models.Model):
    msn = models.CharField(max_length=30)
    contact = models.ForeignKey(to=Contact, on_delete=models.PROTECT)


# 合同信息
class Order(models.Model):
    short_order_number = models.CharField(max_length=20, verbose_name='合同号简写')  # 是否允许重复？
    person_in_charge = models.CharField(max_length=10, verbose_name='合同负责人', blank=True, null=True)
    client_type = models.CharField(max_length=20, verbose_name='客户类型')
    country_of_origin = models.CharField(max_length=20, verbose_name='原产地')
    chinese_name_of_equipment = models.CharField(max_length=30, verbose_name='设备名称(中文)', blank=True, null=True)
    english_name_of_equipment = models.CharField(max_length=30, verbose_name='设备名称(英文)', blank=True, null=True)
    project_number = models.CharField(max_length=10, verbose_name='业主项目号', blank=True, null=True)
    po_number = models.CharField(max_length=40, verbose_name='PO号', blank=True, null=True)
    mr_number = models.CharField(max_length=40, verbose_name='MR号', blank=True, null=True)
    currency_of_po = models.CharField(max_length=20, verbose_name='PO的货币类型')
    amount_of_po = models.BigIntegerField(verbose_name='PO金额')
    currency_of_chinese_order = models.CharField(max_length=20, verbose_name='中文合同的货币类型', blank=True, null=True)
    amount_of_chinese_order = models.BigIntegerField(verbose_name='中文合同的金额', blank=True, null=True)
    currency_of_freight = models.CharField(max_length=20, verbose_name='运费的货币类型', blank=True, null=True)
    amount_of_freight = models.CharField(max_length=20, verbose_name='运费金额', blank=True, null=True)
    apg_is_needed = models.CharField(max_length=20, verbose_name='是否需要开预付款保函')
    pg_is_needed = models.CharField(max_length=20, verbose_name='是否需要开履约保函')
    condition_of_coming_into_effectiveness = models.CharField(max_length=20, verbose_name='合同生效条件', blank=True,
                                                              null=True)
    guarantee_period = models.BigIntegerField(verbose_name='质保期(月)', blank=True, null=True)
    date_of_sending_order_to_vendor = models.DateField(verbose_name='PO发给供应商的日期', blank=True, null=True)
    po_signing_date = models.DateField(verbose_name='PO签字日期', blank=True, null=True)
    is_canceled = models.BooleanField(verbose_name='合同是否已取消')
    is_transferred_to_r = models.BooleanField(verbose_name='是否已转让给瑞程')
    date_of_coming_into_effectiveness = models.DateField(verbose_name='合同生效日期', blank=True, null=True)
    comment_for_first_party = models.TextField(verbose_name='给业主/分包商看的注释', blank=True, null=True)
    remark = models.TextField(max_length=500, verbose_name='备注', default='无')
    vendor = models.ForeignKey(to=Vendor, on_delete=models.PROTECT)

    def __str__(self):
        return self.short_order_number

    class Meta:
        verbose_name = '合同信息'
        verbose_name_plural = verbose_name


class Guarantee(models.Model):
    currency = models.CharField(max_length=20, verbose_name='货币类型')
    amount = models.BigIntegerField(verbose_name='保函金额')
    type = models.CharField(max_length=10, verbose_name='保函类型')
    serial_number = models.CharField(max_length=50, verbose_name='保函编号')
    type_of_issuing_institution = models.CharField(max_length=15, verbose_name='开立机构')
    issuing_bank = models.CharField(max_length=50, verbose_name='开立行')
    date_of_issuing = models.DateField(verbose_name='开立日期')
    condition_of_coming_into_effectiveness = models.CharField(max_length=20, verbose_name='生效条件')
    date_of_coming_into_effectiveness = models.DateField(verbose_name='生效日期')
    expiring_date = models.DateField(verbose_name='到期日')
    following_up_serial_number = models.CharField(max_length=50, verbose_name='接续保函编号')
    is_returned = models.BooleanField(verbose_name='是否已退还给供应商')
    remark = models.TextField(max_length=500, verbose_name='备注', default='无')
    short_order_number = models.ManyToManyField(verbose_name='合同号简写', to=Order, through='OrderToGuarantee',
                                                through_fields=('serial_number_of_guarantee', 'short_order_number'), )

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = '保函信息'
        verbose_name_plural = verbose_name


class OrderToGuarantee(models.Model):
    short_order_number = models.ForeignKey(verbose_name='合同号简写', to=Order, on_delete=models.PROTECT)
    serial_number_of_guarantee = models.ForeignKey(verbose_name='保函编号', to=Guarantee, on_delete=models.PROTECT)

    def __str__(self):
        return self.short_order_number + '---' + self.serial_number_of_guarantee

    class Meta:
        verbose_name = '合同保函中间表'
        verbose_name_plural = verbose_name


# 多对多的关系参考第三季p8


class UserInformation(AbstractUser):
    mobile = models.BigIntegerField(verbose_name='手机号', blank=True, null=True)

    class Meta:
        verbose_name = '网站用户信息'
        verbose_name_plural = verbose_name

from rest_framework import serializers

from general.models import Vendor, Contact, Order, Guarantee, Test1, OrderToGuarantee


# 普通序列化器
# class ContactSerializer(serializers.Serializer):
#     name = serializers.CharField(label='姓名')
#     department = serializers.CharField(required=False)
#     title = serializers.CharField(default='default测试', required=False)
#     landline = serializers.CharField(required=False)
#     mobile = serializers.CharField(required=False)
#     email = serializers.CharField(required=False)
#     qq = serializers.CharField(required=False)
#     wechat = serializers.CharField(required=False)
#
#     # Relational field must provide a `queryset` argument, override `get_queryset`, or set read_only = `True`.
#     # vendor = serializers.PrimaryKeyRelatedField(read_only=True)
#     # vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
#     # 获取外键的__str__, 也就是名称
#     # vendor = serializers.StringRelatedField(read_only=True)
#     # 获取外键的全部信息
#     # 如果要获得外键的全部信息，外键的序列化器必须写在前面。不行写2遍
#     # vendor = VendorSerializer()
#
#     vendor_name = serializers.CharField(source='vendor.chinese_short_name', read_only=True)  #
#
#     is_deleted = serializers.BooleanField(default=False, label='逻辑删除')
#
#     # 显示外键信息的方法：source=本表外键字段.关联表待查字段
#
#     def create(self, validated_data):
#         return Contact.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.department = validated_data.get('department', instance.department)
#         instance.save()
#         return instance


class OrderReadSerializer(serializers.ModelSerializer):
    # order表有外键contact字段，所以可以显示所有的联系人
    class Meta:
        model = Order
        exclude = ['id', 'is_deleted', 'created_time', 'updated_time']
        # 自定义外键查询的深度
        # depth = 1

    guarantee_test = serializers.SerializerMethodField()
    vendor_test = serializers.SerializerMethodField()

    # pycharm报错，由于self未使用，根据提示加了@staticmethod改成静态函数，不影响运行
    @staticmethod
    def get_guarantee_test(obj):
        # 先自定义空集
        many_records = []

        # 这里的obj是指传入的order，通过.外键表名（表名！）_set的方法（这是django的方法，不是drf的），获取到外键的全部信息
        for record in obj.guarantee_set.all().values('serial_number', 'currency', 'amount'):
            many_records.append(record)

        return many_records

    # 想要自定义外键的显示字段，只能自己写了
    @staticmethod
    def get_vendor_test(obj):
        record = {}
        record.update(chinese_short_name=obj.vendor.chinese_short_name,
                      chinese_full_name=obj.vendor.chinese_full_name,
                      english_short_name=obj.vendor.english_short_name,
                      english_full_name=obj.vendor.english_full_name,
                      chinese_address=obj.vendor.chinese_address,
                      english_address=obj.vendor.english_address)
        return record


class OrderWriteSerializer(serializers.ModelSerializer):
    # order表有外键contact字段，所以可以显示所有的联系人
    class Meta:
        model = Order
        exclude = ['is_deleted', 'created_time', 'updated_time']
        # 自定义外键查询的深度
        # depth = 1


class ContactReadSerializer(serializers.ModelSerializer):
    # contact没有order的外键字段，所以默认无法显示所有的order
    # 通过查询集的方式，展示当前联系人的所有订单
    # order_set = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        exclude = ['created_time', 'updated_time', 'is_deleted']

        # 要想显示外键的全部信息，就要开启depth
        # depth = 1
        # read可以这么写，write没有这个功能
        # read_only_fields = [""]
        # extra_kwargs = {
        #     'id': {
        #         'write_only': True
        #     }
        # }

    vendor_info = serializers.SerializerMethodField()

    #
    # 这里有大量的复用，还不清楚怎么快捷调用
    @staticmethod
    def get_vendor_info(obj):
        record = {}
        record.update(chinese_short_name=obj.vendor.chinese_short_name,
                      chinese_full_name=obj.vendor.chinese_full_name,
                      english_short_name=obj.vendor.english_short_name,
                      english_full_name=obj.vendor.english_full_name,
                      chinese_address=obj.vendor.chinese_address,
                      english_address=obj.vendor.english_address)
        return record


class ContactWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('created_time', 'updated_time', 'is_deleted')

    # @staticmethod
    # # 这里的data是提交的email内容
    # def validate_email(data):
    #     print(data)
    #     if '@' not in data:
    #         raise serializers.ValidationError('email必须有@')
    #     return data


# 本类仅供作为外键时显示使用，显示的字段更少，加快传输速度
class ContactShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['vendor', 'is_deleted', 'created_time', 'updated_time', 'last_reviser']


class VendorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['is_deleted', 'created_time', 'updated_time']
        # 自定义外键查询的深度
        # depth = 1

    # 查询多方的列表信息，用short序列化器
    contact_set = ContactShortSerializer(read_only=True, many=True)


class Test1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Test1
        fields = '__all__'


class VendorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['is_deleted', 'id', 'created_time', 'updated_time']
        # 自定义外键查询的深度
        # depth = 1

    # 查询多方的列表信息，用short序列化器
    # contact_set = ContactShortSerializer(read_only=True, many=True)


class OrderToGuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderToGuarantee
        fields = '__all__'


class GuaranteeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        exclude = ['is_deleted', 'created_time', 'updated_time']

    order_test = serializers.SerializerMethodField()

    @staticmethod
    def get_order_test(obj):
        a = []
        for row in obj.short_order_number.all().values('short_order_number', 'person_in_charge', 'client_type'):
            a.append(row)
        return a
    # https://www.bilibili.com/video/BV14a4y1Y7Ku?p=18&t=289 这里教的方法，不太懂原理，就没用
    # return [row for row in
    #         obj.short_order_number.all().values('short_order_number', 'person_in_charge', 'client_type')]


class GuaranteeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        exclude = ['is_deleted', 'id', 'created_time', 'updated_time']
#
# class VendorSerializer(serializers.Serializer):
#     chinese_short_name = serializers.CharField(required=False)
#     english_short_name = serializers.CharField(required=False)
#     english_full_name = serializers.CharField(required=False)
#     # 获取供应商下面的所有联系人
#     # 这样写感觉不好，因为供应商下面的联系人并非只读，而且这样取到的是联系人id
#     # contact_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
#     # 取对象集的时候，记得加上many=True
#     # contact_set = serializers.StringRelatedField(read_only=True, many=True)
#     contact_set = ContactSerializer(read_only=True, many=True)
#
#     def create(self, validated_data):
#         return Vendor.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.chinese_short_name = validated_data.get('chinese_short_name', instance.chinese_short_name)
#         instance.english_short_name = validated_data.get('english_short_name', instance.english_short_name)
#         instance.save()
#         return instance

# 不清楚怎么添加外键的信息，所以暂时放弃，用上面的方法
# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ('vendor_chinese_short_name',)
#
#         # exclude = ['id', ]

# 局部钩子和全局钩子也在这里写
# ModelSerializer已经重写了入库方法

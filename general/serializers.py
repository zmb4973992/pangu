from rest_framework import serializers

from general.models import Vendor, Contact


# 普通序列化器
class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(label='姓名')
    department = serializers.CharField(required=False)
    title = serializers.CharField(default='default测试', required=False)
    landline = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    qq = serializers.CharField(required=False)
    wechat = serializers.CharField(required=False)
    # Relational field must provide a `queryset` argument, override `get_queryset`, or set read_only = `True`.
    # vendor = serializers.PrimaryKeyRelatedField(read_only=True)
    # vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    # 获取外键的__str__, 也就是名称
    # vendor = serializers.StringRelatedField(read_only=True)
    # 获取外键的全部信息
    # 如果要获得外键的全部信息，外键的序列化器必须写在前面。不行写2遍
    # vendor = VendorSerializer()

    vendor_name = serializers.CharField(source='vendor.chinese_short_name', read_only=True)  #

    is_deleted = serializers.BooleanField(default=False, label='逻辑删除')

    # 显示外键信息的方法：source=本表外键字段.关联表待查字段

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        return instance


class VendorSerializer(serializers.Serializer):
    chinese_short_name = serializers.CharField(required=False)
    english_short_name = serializers.CharField(required=False)
    english_full_name = serializers.CharField(required=False)
    # 获取供应商下面的所有联系人
    # 这样写感觉不好，因为供应商下面的联系人并非只读，而且这样取到的是联系人id
    # contact_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # 取对象集的时候，记得加上many=True
    contact_set = serializers.StringRelatedField(read_only=True, many=True)
    set = ContactSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.chinese_short_name = validated_data.get('chinese_short_name', instance.chinese_short_name)
        instance.english_short_name = validated_data.get('english_short_name', instance.english_short_name)
        instance.save()
        return instance

# 不清楚怎么添加外键的信息，所以暂时放弃，用上面的方法
# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ('vendor_chinese_short_name',)
#
#         # exclude = ['id', ]

# 局部钩子和全局钩子也在这里写
# ModelSerializer已经重写了入库方法

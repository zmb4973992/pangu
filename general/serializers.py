from rest_framework import serializers

from general.models import Contact


# 普通序列化器
# class ContactSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     department = serializers.CharField()
#
#     def create(self, validated_data):
#         return Contact.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.department = validated_data.get('department', instance.department)
#         instance.save()
#         return instance

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact

        exclude = ['id', ]

    # 局部钩子和全局钩子也在这里写
    # ModelSerializer已经重写了入库方法

import re
from datetime import datetime, timedelta
from MxShop.settings import REGEX_MOBILE
from rest_framework import serializers
from users.models import VerifyCode
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_moblie(self, moblie):
        """
        验证手机号码
        :param moblie:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(moblie=moblie).count():
            raise serializers.ValidationError("用户已存在")

        # 验证手机号码是否合法
        if re.match(REGEX_MOBILE, moblie):
            raise serializers.ValidationError("手机号非法")

        # 验证发送频率

        one_mintes = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes, moblie=moblie):
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return moblie


class UserRegSerializer(serializers.ModelSerializer):
    # write_only=True 序列化时就不会进行序列化
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="验证码",
                                 error_messages={
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text="验证码")

    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])   # username是否唯一

    password = serializers.CharField(
        style={"input_type": "password"}, label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validated_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by
        if verify_records:
            last_record = verify_records[0]
            one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)  # 获取两分钟以前的时间
            if one_mintes_ago > last_record.add_time:  # 当前时间的前2分钟小于验证码获取时间
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile")

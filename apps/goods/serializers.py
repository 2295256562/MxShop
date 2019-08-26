from rest_framework import serializers
from goods import models


class CategorySerializers3(serializers.ModelSerializer):
    """
    三级类目
    """

    class Meta:
        model = models.GoodsCategory
        fields = "__all__"


class CategorySerializers2(serializers.ModelSerializer):
    """
    二级类目
    """
    sub_cat = CategorySerializers3(many=True)

    class Meta:
        model = models.GoodsCategory
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    """
    一级类目
    """
    sub_cat = CategorySerializers2(many=True)

    class Meta:
        model = models.GoodsCategory
        fields = "__all__"


class GoodsSerializers(serializers.ModelSerializer):
    category = CategorySerializers()

    class Meta:
        model = models.Goods
        fields = "__all__"

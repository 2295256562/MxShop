from rest_framework import serializers
from goods import models


class categorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsCategory
        fields = "__all__"

class GoodsSerializers(serializers.ModelSerializer):
    category = categorySerializers()
    class Meta:
        model = models.Goods
        fields = "__all__"

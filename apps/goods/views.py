from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from goods import serializers
from rest_framework.views import APIView
from goods import models
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


# class GoodsView(APIView):
#     def get(self, request):
#         res = {'code': '200', "msg": "true"}
#         all_goods = models.Goods.objects.all()
#         res_obj = serializers.GoodsSerializers(all_goods, many=True)
#         res['data'] = res_obj.data
#         return Response(res)

class GoodSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

class GoodsViewSets(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Goods.objects.all()
    serializer_class = serializers.GoodsSerializers
    pagination_class = GoodSetPagination
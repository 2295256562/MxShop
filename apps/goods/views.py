from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from goods import serializers
from rest_framework.views import APIView
from goods import models
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from goods.filter import GoodsFilter
from rest_framework import filters


# class GoodsView(APIView):
#     def get(self, request):
#         res = {'code': '200', "msg": "true"}
#         all_goods = models.Goods.objects.all()
#         res_obj = serializers.GoodsSerializers(all_goods, many=True)
#         res['data'] = res_obj.data
#         return Response(res)

class GoodSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsViewSets(mixins.ListModelMixin, GenericViewSet):
    """
    商品列表页, 分页，搜搜，过滤，排序
    """
    queryset = models.Goods.objects.all()
    serializer_class = serializers.GoodsSerializers
    pagination_class = GoodSetPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = models.GoodsCategory.objects.filter(category_type=1)
    serializer_class = serializers.CategorySerializers
"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
import xadmin
from MxShop.settings import MIDDLEWARE
from rest_framework.documentation import include_docs_urls
from django.views.static import serve
from goods.views import GoodsViewSets, CategoryViewSets
from rest_framework.authtoken import views
router = routers.SimpleRouter()
router.register(r'goods', GoodsViewSets, base_name='goods')
router.register(r'categorys', CategoryViewSets, base_name='category')

urlpatterns = [
    re_path('xadmin/', xadmin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    # 商品列表
    # re_path(r'goods/',GoodsView.as_view(), name="good_list"),
    re_path(r'^', include(router.urls)),
    re_path(r'docs/', include_docs_urls(title="慕学生鲜")),

    # drf自带的token认证模式
    re_path(r'^api-token-auth/', views.obtain_auth_token),

    # jwt接口认证
    re_path(r'^login/', obtain_jwt_token),
]

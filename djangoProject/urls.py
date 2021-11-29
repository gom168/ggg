"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

import xadmin

from goods.views import GoodsListViewSet, CategoryViewSet, GoodsImageViewSet, BannerViewSet, SettingsViewSet, \
    GoodsOfCategory
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, AddressViewSet
from notes.views import NotesViewSet, CommentViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet

from users.views import UserViewSet,SmsCodeViewSet

router = DefaultRouter()

# 配置goods的路由
router.register(r'goods', GoodsListViewSet, basename='goods')

# 配置categories的路由
router.register(r'categories', CategoryViewSet, basename='categories')

router.register(r'goodsimage', GoodsImageViewSet, basename='goodsImage')
router.register(r'banner', BannerViewSet, basename='banner')
router.register(r'userfavs', UserFavViewSet, basename='userfavs')

router.register(r'settings', SettingsViewSet, basename='settings')

router.register(r'goodsOfcategory', GoodsOfCategory, basename='goodsOfcategory')
# 配置购物车路由
router.register(r'shopcarts', ShoppingCartViewSet, basename='shopcarts')

router.register(r'usercomment', UserLeavingMessageViewSet, basename='usercomment')

router.register(r'user', UserViewSet, basename='user')

router.register(r'orders', OrderViewSet, basename='orders')

router.register(r'address', AddressViewSet, basename='address')

router.register(r'note', NotesViewSet, basename='note')

router.register(r'note_comment', CommentViewSet, basename='note_comment')
router.register(r'codes', SmsCodeViewSet, basename='codes')

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^', include(router.urls)),

    # url(r'^register/$', register),
    # url(r'^activate/(.*)/$', activate_user ,name='active'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # DRF自带认证路由
    url(r'^api-token-auth/', views.obtain_auth_token, name='api_token_auth'),

    # JWT认证路由
    url(r'^login/', obtain_jwt_token),
    # url(r'^settings/$', SettingsViewSet.as_view()),

    url(r'docs/', include_docs_urls(title='联想笔记本商城')),
]

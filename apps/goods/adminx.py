import xadmin
from .models import Goods, GoodsCategory, GoodsImage, GoodsCategoryBrand, Banner, Settings


class GoodsAdmin(object):
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", 'category', 'goods_sn',
                    "price", "goods_brief", "goods_desc", "is_new", "is_hot", "add_time"]
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_per_page = 10
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num",
                   "price", "is_new", "is_hot", "add_time", "category__name"]
    style_fields = {"goods_desc": "ueditor"}

    class GoodsImagesInline(object):
        model = GoodsImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [GoodsImagesInline]


class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class GoodsBrandAdmin(object):
    list_display = ["image", "name", "desc"]

    #  def get_context(self):
    #     context = super(GoodsBrandAdmin, self).get_context()
    #     if 'form' in context:
    #         context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
    #     return context


class SettingsAdmin(object):
    list_display = ["setting_id", "name", "info", "add_time"]
    list_filter = ["setting_id", "name", "info", "add_time"]
    list_pre_page = 10


class BannerGoodsAdmin(object):
    list_display = ["goods", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(Banner, BannerGoodsAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
xadmin.site.register(Settings, SettingsAdmin)
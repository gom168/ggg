import xadmin
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(object):
    list_display = ["user", "goods", "goods_num", ]
    list_per_page = 10


class OrderInfoAdmin(object):
    list_display = ["user", "order_sn", "trade_no", "pay_status", "pay_script", "order_mount",
                    "pay_time", "address", "signer_name", "signer_mobile", "add_time"]
    list_per_page = 10

    class OrderGoodsInline(object):
        model = OrderGoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderGoodsInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)

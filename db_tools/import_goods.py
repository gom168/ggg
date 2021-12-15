import sys, os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

import django

django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import raw_data

for goods_detail in raw_data:
    goods = Goods()
    goods.name = goods_detail['name']
    goods.goods_sn = goods_detail['goods_sn']
    goods.price = float(goods_detail['price'].replace('￥', '').replace('元', ''))
    goods.goods_num = int(goods_detail['num'])
    goods.goods_brief = goods_detail['goods_brief'] if goods_detail['goods_brief'] is not None else ''
    goods.goods_desc = goods_detail['desc'] if goods_detail['desc'] is not None else ''
    goods.goods_front_image = goods_detail['images'][0] if goods_detail['images'] is not None else ''
    goods.detail_image = goods_detail['images'][1] if goods_detail['images'] is not None else ' '
    goods.ship_free = goods_detail['ship_free']
    goods.is_hot = goods_detail['is_hot']
    goods.is_new = goods_detail['is_new']
    goods.fav_num = 0
    goods.click_num = 0
    goods.sold_num = 0
    category_name = goods_detail['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail['images']:
        goods_iamge_instance = GoodsImage()
        goods_iamge_instance.image = goods_image
        goods_iamge_instance.goods = goods
        goods_iamge_instance.save()


print('Goods data imported successfully')
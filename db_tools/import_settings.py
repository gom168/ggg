import sys, os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

import django

django.setup()

from goods.models import Settings

from db_tools.data.setting_data import raw_data


for setting_data in raw_data:

    settings = Settings()
    settings.name = setting_data['name']
    settings.setting_id = setting_data['setting_id']
    settings.goods_sn = setting_data['goods_sn']
    settings.info = setting_data['info']

    settings.save()

print('setting data imported successfully')
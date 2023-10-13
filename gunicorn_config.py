command = '/home/enyoku/work/pet/shop-for-warehouse/venv/bin/gunicorn'
pythonpath = '/home/enyoku/work/pet/shop-for-warehouse/shop'
bind = '127.0.0.1:8000'
workers = 2
user = 'enyoku'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=shop.settings'

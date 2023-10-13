#!/bin/bash
source /home/enyoku/work/pet/shop-for-warehouse/venv/bin/activate
gunicorn -c "/home/enyoku/work/pet/shop-for-warehouse/shop/gunicorn_config.py" shop.wsgi
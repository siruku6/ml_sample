#!/bin/bash

python manage.py migrate

# NOTE: ssl対応したい場合はこちらを参照
#   https://qiita.com/Syoitu/items/6205774c6348bc61df90
#   正式なSSL証明書がないと、利用者がアクセスしにくくなるだけなので注意
# python manage.py runsslserver 0.0.0.0:8000 --certificate docker/web/ssl.crt --key docker/web/ssl.key
python manage.py runserver 0.0.0.0:8000

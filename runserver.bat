@ECHO OFF
SET SECRET_KEY='d2+4^hck=b^@$76wxj52@cba80ug$(uj71a+r0c56^^t_1h3bi'

start /wait "" http://127.0.0.1:8000/
start "" python manage.py %*runserver

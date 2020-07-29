import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail
from flask_apscheduler import APScheduler
from flask_celery import Celery
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

# 集成flask-pyMongo
mongo = PyMongo()

# 集成flask-socket.io
socket_io = SocketIO()

# 集成celery flask_celery
# 启动worker: celery -A starter.celery worker -l info --pool=solo -f logs/celery.log
celery = Celery()

# 集成flask_apscheduler
scheduler = APScheduler(BackgroundScheduler(timezone='Asia/Shanghai'))
# apscheduler日志
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


mail = Mail()

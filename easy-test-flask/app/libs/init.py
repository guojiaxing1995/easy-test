from flask_celery import Celery
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

# 集成flask-pyMongo
mongo = PyMongo()

# 集成flask-socket.io
socket_io = SocketIO()

# 集成celery flask_celery
# 启动worker: celery -A starter.celery worker -l info --pool=solo
celery = Celery()

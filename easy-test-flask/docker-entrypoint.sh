#!/bin/sh
set -e

if [ $1 = "api" ];then
        python starter.py --env=prod
elif [ $1 = "worker" ];then
        celery -A starter.celery worker -l info --pool=solo -f logs/celery.log --host=prod
else
        echo "参数错误 1) api 作为后端主程序启动. 2）worker 作为消费者启动"
        exit 1
fi
FROM python:3.6-slim

MAINTAINER guojiaxing<302802003@qq.com>

EXPOSE 5000

COPY . ./easy-test-flask/

WORKDIR /easy-test-flask/

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN ["pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-r", "requirements.txt"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]

CMD ["api"]

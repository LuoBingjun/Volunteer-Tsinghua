FROM python:3.6.9
ENV PYTHONUNBUFFERED 1
# 添加这两行
RUN sed -i s@/deb.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN sed -i s@/security.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y
RUN mkdir /code
WORKDIR /code
COPY /backend/requirements.txt /code
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
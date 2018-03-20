FROM selenium/standalone-firefox

MAINTAINER SCURSS

ENV LANG C.UTF-8
USER root
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update &&\
    apt install python3-pip -y

RUN pip3 install psycopg2==2.7.3.2 arrow==0.12.0 redis==2.10.6 pyrss2gen==1.1 selenium==3.11.0\
    lxml==4.1.1 requests==2.11.1 ipython==6.2.1 -i https://pypi.douban.com/simple


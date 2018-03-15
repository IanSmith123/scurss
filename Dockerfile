FROM python:3.6.3-jessie

MAINTAINER SCURSS


RUN pip install psycopg2==2.7.3.2 arrow==0.12.0 redis==2.10.6 pyrss2gen==1.1 selenium==3.11.0\
    lxml==4.1.1 requests==2.11.1 ipython==6.2.1 -i https://pypi.douban.com/simple

#ADD https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-linux64.tar.gz /usr/bin/
COPY ./bin/chrome.deb /tmp/chrome.deb
COPY ./bin/chromedriver /usr/bin/chromedriver
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update &&\
    apt install libappindicator1 libasound2 libatk-bridge2.0-0 libatk1.0 libcups2 libdbus-1-3 \
    libnss3 libx11-xcb1 lsb-release xdg-utils libgtk-3-0 libnspr4 fonts-liberation -y
RUN dpkg -i /tmp/chrome.deb &&\
    apt install -f

# CMD ["apache2-foreground"]

FROM php:5.6-apache

MAINTAINER SCURSS

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt install libpq-dev -y --no-install-recommends \
    && docker-php-ext-install pdo pdo_pgsql

EXPOSE 80

# CMD ["apache2-foreground"]
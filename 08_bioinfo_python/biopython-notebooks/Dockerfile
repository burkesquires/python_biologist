FROM andrewosh/binder-base

MAINTAINER Tiago Antao <tiagoantao@gmail.com>

USER root
#RUN apt-get update -y

USER main

COPY docker_prepare.sh /
RUN bash /docker_prepare.sh

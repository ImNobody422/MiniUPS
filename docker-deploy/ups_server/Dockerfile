FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /server_code
WORKDIR /server_code
ADD requirements.txt /server_code/
RUN pip3 install -r requirements.txt
ADD . /server_code
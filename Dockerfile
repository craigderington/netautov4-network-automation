FROM python:3.6-alpine
LABEL maintainer="Craig Derington <cderington@championsg.com>"
RUN apk update && apk upgrade
RUN apk add screen curl
WORKDIR /code
COPY . /code
RUN pip3 install -r requirements-dev.txt
EXPOSE 5555
CMD ["gunicorn", "-b", "0.0.0.0:5555", "-w", "4", "wsgi:app"]
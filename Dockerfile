FROM python:3

WORKDIR /usr/src/app
EXPOSE 20333/tcp
COPY observer.py ./

CMD [ "python", "./observer.py" ]

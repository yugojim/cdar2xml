FROM python:3.9.15
 
ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]
EXPOSE 8100
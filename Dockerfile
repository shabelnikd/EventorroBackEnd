FROM matthewfeickert/docker-python3-ubuntu:latest 

ENV PYTHONUNBUFFERED True 

WORKDIR / 

COPY . . 

USER root 

RUN apt-get update  
RUN apt-get install -y apt-utils 

RUN pip install --upgrade pip 
RUN pip install wheel 
RUN pip install gunicorn 
RUN pip install -r req.txt 

ENV DB_NAME=railway 
ENV DB_USER=postgres 
ENV DB_PASSWORD=QoMm7OGDulnEJNDtT2EV 
ENV DB_HOST=containers-us-west-104.railway.app 
ENV DB_PORT=8042
ENV SECRET_KEY=d1d^r$u47ib(!w)-n_09ggzi_9yy-3)+r)s+tmxvufy18hdehl 

RUN python3 manage.py migrate 
RUN python3 manage.py collectstatic 

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application
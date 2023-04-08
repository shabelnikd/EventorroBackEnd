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

ENV SECRET_KEY==zfb6772hh9_#9*5j$!^h0(8df)(-e^l+5--a-p8j-ljyx9axi
ENV DEBUG=True
ENV ALLOWED_HOSTS='afiche-production.up.railway.app,0.0.0.0'
ENV EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
ENV EMAIL_HOST=smtp.gmail.com
ENV EMAIL_USE_TLS=True
ENV EMAIL_PORT=587
ENV EMAIL_HOST_USER=akimbaeva.a23@gmail.com
ENV EMAIL_HOST_PASSWORD=qolwlivzougccfut
ENV DB_ENGINE=django.db.backends.postgresql
ENV DB_NAME=railway 
ENV DB_USER=postgres
ENV DB_PASSWORD=GPuaar250YuzUPvFgQQd
ENV DB_HOST=containers-us-west-68.railway.app
ENV DB_PORT=6093
ENV DOMAIN=afiche-production.up.railway.app

RUN python3 manage.py migrate 
RUN python3 manage.py collectstatic 

CMD gunicorn --bind 0.0.0.0:8000 afiche.wsgi:application
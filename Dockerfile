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
ENV EMAIL_HOST_PASSWORD=obsjscojziwcatze
ENV DB_ENGINE=django.db.backends.postgresql
ENV DB_NAME=railway 
ENV DB_USER=postgres
ENV DB_PASSWORD=625xGIZaVSM0bAedQNmv
ENV DB_HOST=containers-us-west-127.railway.app
ENV DB_PORT=5527
ENV DOMAIN=https://afiche-production.up.railway.app
ENV LINK=https://afiche-production.up.railway.app/media
ENV CELERY_BROKER_URL=redis://default:ZIe99V0FNdk6NM117Vuu@containers-us-west-135.railway.app:7836
ENV CELERY_RESULT_BACKEND=redis://default:ZIe99V0FNdk6NM117Vuu@containers-us-west-135.railway.app:7836
ENV REDIS_HOST=containers-us-west-135.railway.app
ENV REDIS_PORT=7836
ENV REDIS_PASSWORD=ZIe99V0FNdk6NM117Vuu
RUN python3 manage.py migrate 
RUN python3 manage.py collectstatic 
RUN celery -A afiche purge

CMD celery -A afiche worker -l info && celery -A afiche beat && gunicorn --bind 0.0.0.0:8000 afiche.wsgi:application
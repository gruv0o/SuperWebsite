FROM python:3.12-slim

WORKDIR app

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

ENV FLASK_APP=app
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
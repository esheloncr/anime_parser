FROM python:3.8.3-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV APP_HOME=/usr/src
WORKDIR $APP_HOME
COPY . $APP_HOME
ENTRYPOINT ["/usr/src/entrypoint.sh"]

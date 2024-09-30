FROM python:alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /develop
WORKDIR /develop
RUN pip install --upgrade pip
COPY requirements.txt /develop/
RUN pip install -r requirements.txt
COPY . /develop/
EXPOSE 8000
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

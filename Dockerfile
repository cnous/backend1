FROM python:3.13.0a4-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies

# install dependencies
COPY requirments.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirments.txt


# copy project
COPY . .
CMD ["python3","manage.py","runserver"]
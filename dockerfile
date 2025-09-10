FROM python:3-slim

WORKDIR /usr/src

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt

COPY ./app /usr/src/app

CMD ["python", "/usr/src/app/main.py"]

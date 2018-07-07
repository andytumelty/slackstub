FROM python:3-alpine

COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

EXPOSE 5000

COPY ./server.py /app/
ENTRYPOINT ["python3", "/app/server.py"]

COPY VERSION .

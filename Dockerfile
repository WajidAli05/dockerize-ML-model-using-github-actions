FROM alpine:lastest

WORKDIR /app

COPY . .

RUN pip instll -r requirements.txt

CMD ["python", "model-load.py"]
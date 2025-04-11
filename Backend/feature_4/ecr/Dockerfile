FROM python:3.12-slim-bookworm

WORKDIR /app

COPY ./* .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]

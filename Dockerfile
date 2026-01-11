FROM python:3.12-slim

WORKDIR /src/backend

COPY /src/backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/backend .

CMD ["python", "-m", "main"]

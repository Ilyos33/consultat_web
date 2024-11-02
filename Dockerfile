FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN install -r requirements.txt

COPY . .

EXPOSE 8000

CMD["uvicorn","main:app","--reload"]













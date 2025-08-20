FROM python:3.13-slim

WORKDIR /auth
COPY . .

RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python", "auth.py"]
FROM python:3.9-alpine
COPY ../../../tests /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
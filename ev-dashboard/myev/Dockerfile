FROM python:3.9-alpine
ADD ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

FROM python:3.7
WORKDIR /usr/app
RUN pip install --no-cache-dir shttp redis
COPY ./hello-app.py ./hello-app.py
CMD ["python", "hello-app.py"]

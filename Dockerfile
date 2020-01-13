FROM python:3.7
WORKDIR /usr/app
RUN pip install --no-cache-dir shttp
COPY ./hello-server.py ./hello-app.py
CMD ["python", "hello-app.py"]

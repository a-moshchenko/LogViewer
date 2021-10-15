FROM python:3.9

RUN mkdir ./log_view_web
WORKDIR ./log_view_web
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt


CMD ["python", "server.py"]
FROM python:3.11.4-slim
LABEL authors="alex"
LABEL desc="django dev container"
WORKDIR /usr/src/app
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
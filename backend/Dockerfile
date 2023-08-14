FROM python:alpine
LABEL authors="alex"
LABEL desc="django dev container"
WORKDIR /usr/src/app
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
COPY . .
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
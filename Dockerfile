FROM python:3.7-alpine
RUN apk update && apk add --update gcc python3-dev libc-dev libffi-dev postgresql-dev musl-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV SERVER_NAME="localhost:5000"
ENV SECRET_KEY="my secret key"
ENV DATABASE_URI="sqlite://"
ENV REDDIT_SECRET="my secrety reddit key"
ENV REDDIT_CLIENT_ID="my reddit client ID"

EXPOSE 5000
CMD ["./startup.sh"]
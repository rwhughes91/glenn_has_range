FROM python:3.6-alpine

RUN adduser -D glenn

WORKDIR /home/glenn

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY . .
RUN chmod +x boot.sh

RUN chown -R glenn:glenn ./
USER glenn

ENV SERVER_NAME="localhost:5000"
ENV SECRET_KEY="my secret key"
ENV DATABASE_URI="sqlite://"

EXPOSE 5000
ENTRYPOINT ["./bin/boot.sh"]
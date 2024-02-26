FROM python:3-alpine


RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk add openjdk11
RUN pip3 install Flask psycopg2 tabula-py
RUN apk --purge del .build-deps

WORKDIR /app

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
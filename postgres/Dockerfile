# vim:set ft=dockerfile:
FROM postgres:9.6

LABEL maintainer="kundik.kirill@gmail.com"

# Custom initialization scripts
COPY ./create_pg_users.sh   /docker-entrypoint-initdb.d/10-create_user.sh

FROM mariadb:10.5

ENV MYSQL_ROOT_PASSWORD wikipedia
COPY enwp10_dev.dump.sql /docker-entrypoint-initdb.d

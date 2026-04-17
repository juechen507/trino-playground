#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE metastore;
    CREATE USER hive WITH ENCRYPTED PASSWORD 'hive';
    GRANT ALL PRIVILEGES ON DATABASE metastore TO hive;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "metastore" <<-EOSQL
    GRANT ALL ON ALL TABLES IN SCHEMA public TO hive;
    GRANT ALL ON SCHEMA public TO hive;
    ALTER SCHEMA public OWNER TO hive;
EOSQL
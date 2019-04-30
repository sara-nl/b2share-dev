#!/bin/bash

# sudo -u postgres psql b2share -c "drop database b2share;"
# sudo -u postgres psql b2share -c "create database b2share;"
# sudo -u postgres psql b2share -c "grant all on database b2share to b2share;"
# sudo -u postgres psql b2share < /build/dump/b2share.sql

(
sudo -u postgres psql b2share -P pager=off -t -c \
     "SELECT 'ALTER TABLE '|| schemaname || '.' || tablename ||' OWNER TO b2share;' FROM pg_tables WHERE NOT schemaname IN ('pg_catalog', 'information_schema') ORDER BY schemaname, tablename;"
sudo -u postgres psql b2share -P pager=off -t -c \
     "SELECT 'ALTER SEQUENCE '|| sequence_schema || '.' || sequence_name ||' OWNER TO b2share;' FROM information_schema.sequences WHERE NOT sequence_schema IN ('pg_catalog', 'information_schema') ORDER BY sequence_schema, sequence_name;"
sudo -u postgres psql b2share -P pager=off -t -c \
     "SELECT 'ALTER VIEW '|| table_schema || '.' || table_name ||' OWNER TO b2share;' FROM information_schema.views WHERE NOT table_schema IN ('pg_catalog', 'information_schema') ORDER BY table_schema, table_name;"
) > /tmp/change_owner.sql

sudo -u postgres psql b2share -P pager=off -t < /tmp/change_owner.sql


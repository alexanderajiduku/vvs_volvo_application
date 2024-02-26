\echo 'Delete and recreate your_db_name db?'
\prompt 'Return for yes or control-C to cancel > ' confirmation

\c postgres

DROP DATABASE IF EXISTS vvs_db;
CREATE DATABASE vvs_db;

\c vvs_db

\i vvs-schema.sql
--\i your_db_seed.sql



--psql -U your_username -d your_database_name -f start.sql

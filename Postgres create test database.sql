
/* These statements must be highlighted and executed separately, with no other users active on the database. */

DROP DATABASE IF EXISTS "AG_Test";

CREATE DATABASE "AG_Test"
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'English_United States.1252'
       LC_CTYPE = 'English_United States.1252'
       CONNECTION LIMIT = -1;


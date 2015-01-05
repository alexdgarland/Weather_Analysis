CREATE OR REPLACE FUNCTION staging."AssignAndGetNewLoadID"()
RETURNS integer
AS
'INSERT INTO staging."JCMB_Weather_Loads"("load_start_timestamp") VALUES (clock_timestamp()) RETURNING load_id;'
LANGUAGE SQL;
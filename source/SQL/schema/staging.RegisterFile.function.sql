DROP FUNCTION IF EXISTS staging."RegisterFile"(character varying, timestamp without time zone, integer) CASCADE;

CREATE OR REPLACE FUNCTION staging."RegisterFile"
    (
    filename character varying,
    modified_date timestamp without time zone,
    load_id integer
    )
RETURNS TABLE
    (
    out_file_id integer
    ,out_source_file_name character varying
    ,out_source_file_modified_datetime timestamp without time zone
    ,out_current_state file_state
    ,out_latest_load_id integer
    ,out_latest_event_timestamp timestamp without time zone
    ) AS
$BODY$
DECLARE new_file_id integer;
BEGIN

    WITH CTE_InputValues AS (SELECT filename, modified_date)
    INSERT INTO staging."JCMB_Weather_LoadFiles"
    (
    source_file_name,
    source_file_modified_datetime
    )
    SELECT  iv.*
    FROM    CTE_InputValues AS iv
        LEFT OUTER JOIN staging."JCMB_Weather_LoadFiles" AS stg
            ON  iv.filename = stg.source_file_name
            AND iv.modified_date = stg.source_file_modified_datetime
    WHERE   stg.source_file_name IS NULL
    RETURNING file_id INTO new_file_id;

    IF new_file_id IS NOT NULL THEN
        INSERT INTO staging."JCMB_Weather_LoadFile_Events" ("file_id", "file_event_state", "file_event_load_id")
        SELECT new_file_id, 'registered'::file_state, load_id;
    END IF;

    -- Get current file status details;
    -- this works to get existing status even if we haven't captured new file ID
    RETURN QUERY
        SELECT  file_id
                ,source_file_name
                ,source_file_modified_datetime
                ,current_state
                ,latest_load_id
                ,latest_event_timestamp
        FROM    staging."JCMB_Weather_LoadFiles_WithStatus"
        WHERE   source_file_name = filename
        AND     source_file_modified_datetime = modified_date;

END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION staging."RegisterFile"(character varying, timestamp without time zone, integer)
  OWNER TO postgres;


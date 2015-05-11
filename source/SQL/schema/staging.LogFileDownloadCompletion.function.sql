
CREATE OR REPLACE FUNCTION staging."LogFileDownloadCompletion"
    (
    filename            character varying(1000),
    modified_date       timestamp without time zone,
    in_download_name   character varying(1000),
    load_id             integer
    )
RETURNS integer
AS
$BODY$
DECLARE "downloaded_file_id" integer;
BEGIN
    
    UPDATE  staging."JCMB_Weather_LoadFiles"
    SET     download_name = in_download_name
    WHERE   source_file_name = filename
    AND     source_file_modified_datetime = modified_date
    RETURNING "file_id" INTO "downloaded_file_id";
    
    INSERT INTO staging."JCMB_Weather_LoadFile_Events"
        ("file_id", "file_event_state", "file_event_load_id")
    SELECT  "downloaded_file_id", 'downloaded'::file_state, load_id;
    
    RETURN 0;
    
END
$BODY$
LANGUAGE PLPGSQL;

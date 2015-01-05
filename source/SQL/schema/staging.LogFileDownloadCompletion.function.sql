CREATE OR REPLACE FUNCTION staging."LogFileDownloadCompletion"
	(
	filename	character varying(1000),
	modified_date	timestamp without time zone
	)
RETURNS integer
AS
$BODY$
BEGIN
	UPDATE 	staging."JCMB_Weather_LoadFiles"
	SET 	downloaded_datetime = current_timestamp,
		file_latest_state = 'downloaded'
	WHERE	source_file_name = filename
	AND	source_file_modified_datetime = modified_date;

	RETURN 0;
END
$BODY$
LANGUAGE PLPGSQL;
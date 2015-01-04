

CREATE OR REPLACE FUNCTION staging."InsertFileRecordIfNew"
	(
	filename	character varying(1000),
	modified_date	timestamp without time zone,
	fileupdatename	character varying(1000),
	load_id		integer
	)
RETURNS boolean
AS
$BODY$
DECLARE IsNewFileUpdate boolean;
BEGIN
	WITH CTE_InputValues AS
		(
		SELECT	filename	AS source_file_name,
			modified_date	AS source_file_modified_datetime,
			fileupdatename	AS downloaded_file_name,
			load_id		AS load_id
		),
	CTE_InsertionRows AS
		(
		INSERT INTO staging."JCMB_Weather_LoadFiles"
			(
			source_file_name,
			source_file_modified_datetime,
			downloaded_file_name,
			load_id
			)
		SELECT	iv.*
		FROM 	CTE_InputValues AS iv
			LEFT OUTER JOIN staging."JCMB_Weather_LoadFiles" AS stg
				ON	iv.source_file_name = stg.source_file_name
				AND	iv.source_file_modified_datetime = stg.source_file_modified_datetime
		WHERE	stg.source_file_name IS NULL
		RETURNING 1
		)
	SELECT	CASE COUNT(*)
			WHEN 0 THEN FALSE
			WHEN 1 THEN TRUE
			ELSE NULL
		END	INTO IsNewFileUpdate
	FROM 	CTE_InsertionRows;

	RETURN IsNewFileUpdate;
END
$BODY$
LANGUAGE PLPGSQL;


-- SELECT staging."InsertFileRecordIfNew"('test file', '2015-01-01 15:45:40.00', 'test file', 2)



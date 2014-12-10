
SELECT	f.load_id
	,l.load_start_timestamp
	,l.load_latest_state
	,l.load_end_timestamp 
	,f.file_id
	,f.file_name
	,f.file_registered_timestamp
	,f.file_latest_state
	,f.file_load_complete_timestamp
	,c.file_loaded_row_count
FROM 	staging."JCMB_Weather_LoadFiles" AS f
INNER JOIN staging."JCMB_Weather_Loads" AS l
ON l.load_id = f.load_id
LEFT OUTER JOIN
	(
	SELECT file_id, COUNT(*) AS file_loaded_row_count
	FROM staging."JCMB_Weather_Staging"
	GROUP BY file_id
	) AS c
ON c.file_id = f.file_id
ORDER BY f.file_id DESC;

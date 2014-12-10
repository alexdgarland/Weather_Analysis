
SELECT	f.*, c."RowCount"
FROM 	staging."JCMB_Weather_LoadFiles" AS f
LEFT OUTER JOIN
	(
	SELECT file_id, COUNT(*) AS "RowCount"
	FROM staging."JCMB_Weather_Staging"
	GROUP BY file_id
	) AS c
ON c.file_id = f.file_id
ORDER BY f.file_id DESC;

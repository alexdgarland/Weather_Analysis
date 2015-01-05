CREATE OR REPLACE VIEW staging."JCMB_Weather_Staging_Summary"
AS
	SELECT	LEFT(date_time_text_source, 10) AS DayOfReading,
		COUNT(*)
	FROM 	staging."JCMB_Weather_Staging"
	GROUP BY LEFT(date_time_text_source, 10)
	ORDER BY DayOfReading DESC;
COMMENT ON VIEW staging."JCMB_Weather_Staging_Summary" IS 'Summary view for manual load checking.';
CREATE OR REPLACE FUNCTION staging."Convert_WeatherReading_DateTime"(date_time character varying(500))
RETURNS timestamp without time zone
AS
$BODY$
BEGIN
	RETURN
		CASE WHEN SUBSTRING(date_time, 12, 2) = '24' THEN
			CAST(SUBSTRING(date_time, 1, 10) AS timestamp without time zone) + CAST('1 day' AS interval)
	ELSE	CAST(date_time AS timestamp without time zone)
	END;
END
$BODY$
LANGUAGE PLPGSQL;
COMMENT ON FUNCTION staging."Convert_WeatherReading_DateTime"(character varying(500))
IS 'Converts from text treating midnight as 24:00 in previous day, to standard timestamp treating it as 00:00 the next.';


-- Unit test for date conversion
WITH CTE_Setup ("Input Value", "Expected Output")
AS	(
	-- Value that doesn't need converting other than a straight CAST
	SELECT '2013/01/01 23:00', CAST('2013/01/01 23:00' AS timestamp without time zone) UNION ALL
	-- Value where hour = 24 so day needs incrementing by one and hour setting to zero
	SELECT '2013/01/01 24:00', CAST('2013/01/02 00:00' AS timestamp without time zone) UNION ALL
	-- Value where incrementing the day will roll us into a new month and year
	SELECT '2013/12/31 24:00', CAST('2014/01/01 00:00' AS timestamp without time zone)
	)
,CTE_Process
AS	(
	SELECT 	"Input Value",
		"Expected Output",
		staging."Convert_WeatherReading_DateTime"("Input Value") AS "Actual Output"
		,CASE
			WHEN staging."Convert_WeatherReading_DateTime"("Input Value") = "Expected Output" THEN 'Success'
			ELSE '!!! FAILURE !!!'
		END AS "Test Result"
	FROM 	CTE_Setup
	)
SELECT	*
FROM 	CTE_Process
WHERE	"Test Result" = '!!! FAILURE !!!';

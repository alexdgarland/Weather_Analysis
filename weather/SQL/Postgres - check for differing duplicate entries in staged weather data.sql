
-- Query to check for duplicate records which actually have different data values within staged weather data

SELECT 	s.*
FROM 	staging."JCMB_Weather_Staging" AS s
	INNER JOIN 	(
			SELECT	date_time_text_source
			FROM 	staging."JCMB_Weather_Staging" 
			GROUP BY date_time_text_source
			HAVING COUNT(DISTINCT concat(atmospheric_pressure_mbar, rainfall_mm, wind_speed_m_per_s, wind_direction_degrees, surface_temperature_c,
						relative_humidity_percentage, solar_flux_kw_per_m2, battery_v)) > 1
			) AS d
	ON d.date_time_text_source = s.date_time_text_source
ORDER BY s.date_time_text_source;

-- One duplicate has a negative figure for atmospheric pressure - see if there are any others
SELECT	*
FROM 	staging."JCMB_Weather_Staging"
	WHERE	CAST(atmospheric_pressure_mbar AS numeric(15,3)) < 0;	
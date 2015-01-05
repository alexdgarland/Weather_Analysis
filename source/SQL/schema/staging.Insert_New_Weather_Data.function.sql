/*
Postgres doesn't currently have a single MERGE or UPSERT statement
so will have to do load to public table in two steps (see also staging."Update_Existing_Weather_Data").
*/
CREATE OR REPLACE FUNCTION staging."Insert_New_Weather_Data"(load_id_to_process int)
RETURNS integer
AS
$BODY$
BEGIN
	INSERT INTO public."JCMB_Weather_Data"
		(
		date_time
		,atmospheric_pressure_mbar
		,rainfall_mm
		,wind_speed_m_per_s
		,wind_direction_degrees
		,surface_temperature_c
		,relative_humidity_percentage
		,solar_flux_kw_per_m2
		,battery_v
		,file_id_created
		,file_id_last_updated
		)
	SELECT	s.date_time
		,s.atmospheric_pressure_mbar
		,s.rainfall_mm
		,s.wind_speed_m_per_s
		,s.wind_direction_degrees
		,s.surface_temperature_c
		,s.relative_humidity_percentage
		,s.solar_flux_kw_per_m2
		,s.battery_v
		,s.file_id
		,s.file_id
	FROM	staging."JCMB_Weather_Staging_Conversions" AS s
		LEFT OUTER JOIN public."JCMB_Weather_Data" AS d
		ON s.date_time = d.date_time
	WHERE	d.date_time IS NULL
	AND	s.load_id = load_id_to_process
	/* Return key details so can do more detailed audit logging */
	RETURNING date_time, file_id_created;
END
$BODY$
LANGUAGE PLPGSQL;
/*
Postgres doesn't currently have a single MERGE or UPSERT statement
so will have to do load to public table in two steps (see also staging."Insert_New_Weather_Data").
*/
CREATE OR REPLACE FUNCTION staging."Update_Existing_Weather_Data"(load_id_to_process int)
RETURNS integer
AS
$BODY$
BEGIN
	UPDATE	public."JCMB_Weather_Data" AS d
	SET	atmospheric_pressure_mbar 	= s.atmospheric_pressure_mbar
		,rainfall_mm 			= s.rainfall_mm
		,wind_speed_m_per_s 		= s.wind_speed_m_per_s
		,wind_direction_degrees		= s.wind_direction_degrees
		,surface_temperature_c		= s.surface_temperature_c
		,relative_humidity_percentage	= s.relative_humidity_percentage
		,solar_flux_kw_per_m2		= s.solar_flux_kw_per_m2
		,battery_v			= s.battery_v
		,file_id_last_updated		= s.file_id
	FROM	staging."JCMB_Weather_Staging_Conversions" AS s
	WHERE	s.date_time = d.date_time
	AND	s.load_id = load_id_to_process
	/* Return key details so can do more detailed audit logging */
	RETURNING s.date_time, s.file_id;
END
$BODY$
LANGUAGE PLPGSQL;
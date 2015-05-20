
CREATE OR REPLACE FUNCTION staging."Close_Load_From_Staging"(load_id_to_log int)
RETURNS integer
AS
$BODY$
BEGIN

    -- Record all files covered by load-from-staging as complete
    INSERT INTO staging."JCMB_Weather_LoadFile_Events"
                (
                file_id,
                file_event_state,
                file_event_load_id
                )
    SELECT	DISTINCT file_id,
            'loaded'::staging.file_state,
            load_id_to_log
    FROM 	staging."JCMB_Weather_Staging";

    -- Archive staged data to staging."JCMB_Weather_Staging_History"
    WITH delete_query AS
        (
        DELETE
        FROM    staging."JCMB_Weather_Staging"
        RETURNING   staged_row_id,
                    file_id,
                    date_time_text_source,
                    atmospheric_pressure_mbar,
                    rainfall_mm,
                    wind_speed_m_per_s,
                    wind_direction_degrees,
                    surface_temperature_c,
                    relative_humidity_percentage,
                    solar_flux_kw_per_m2,
                    battery_v
        )
    INSERT INTO staging."JCMB_Weather_Staging_History"
                (
                staged_row_id,
                file_id,
                date_time_text_source,
                atmospheric_pressure_mbar,
                rainfall_mm,
                wind_speed_m_per_s,
                wind_direction_degrees,
                surface_temperature_c,
                relative_humidity_percentage,
                solar_flux_kw_per_m2,
                battery_v,
                load_id
                )
    SELECT  staged_row_id,
            file_id,
            date_time_text_source,
            atmospheric_pressure_mbar,
            rainfall_mm,
            wind_speed_m_per_s,
            wind_direction_degrees,
            surface_temperature_c,
            relative_humidity_percentage,
            solar_flux_kw_per_m2,
            battery_v,
            load_id_to_log
    FROM    delete_query;
            
    RETURN 0;
    
END
$BODY$
LANGUAGE PLPGSQL;

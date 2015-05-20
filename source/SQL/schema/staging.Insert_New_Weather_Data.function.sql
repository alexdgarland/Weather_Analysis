
/*
Postgres (< 9.5) doesn't have a single MERGE or UPSERT statement
so will have to do load to public table in two steps
(see also staging."Update_Existing_Weather_Data").
*/

CREATE OR REPLACE FUNCTION staging."Insert_New_Weather_Data"(load_id_to_log int)
RETURNS integer
AS
$BODY$
BEGIN

    WITH insert_query AS
        (
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
                )
        SELECT  s1.date_time
                ,s1.atmospheric_pressure_mbar
                ,s1.rainfall_mm
                ,s1.wind_speed_m_per_s
                ,s1.wind_direction_degrees
                ,s1.surface_temperature_c
                ,s1.relative_humidity_percentage
                ,s1.solar_flux_kw_per_m2
                ,s1.battery_v
        FROM    staging."JCMB_Weather_Staging_Conversions" AS s1
                LEFT OUTER JOIN public."JCMB_Weather_Data" AS d
                    ON s1.date_time = d.date_time
        WHERE   d.date_time IS NULL
        RETURNING date_time        
        )
    INSERT INTO staging."JCMB_Weather_Data_Audit"
                (
                entry_type,
                date_time,
                file_id,
                load_id
                )
    SELECT  'created'::staging.audit_entry_type,
            insert_query.date_time,
            s2.file_id,
            load_id_to_log
    FROM    insert_query
            INNER JOIN staging."JCMB_Weather_Staging_Conversions" AS s2
                ON s2.date_time = insert_query.date_time;

    RETURN 0;
    
END
$BODY$
LANGUAGE PLPGSQL;

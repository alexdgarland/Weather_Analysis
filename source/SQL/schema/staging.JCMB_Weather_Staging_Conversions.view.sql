
CREATE OR REPLACE VIEW staging."JCMB_Weather_Staging_Conversions"
AS
    SELECT  ConvertAndRank.date_time
            ,ConvertAndRank.atmospheric_pressure_mbar
            ,ConvertAndRank.rainfall_mm
            ,ConvertAndRank.wind_speed_m_per_s
            ,ConvertAndRank.wind_direction_degrees
            ,ConvertAndRank.surface_temperature_c
            ,ConvertAndRank.relative_humidity_percentage
            ,ConvertAndRank.solar_flux_kw_per_m2
            ,ConvertAndRank.battery_v
            ,ConvertAndRank."file_id"
            ,lf.latest_load_id AS "load_id"
    FROM    (
            SELECT  staging."Convert_WeatherReading_DateTime"(date_time_text_source)                AS date_time
                    ,CAST(CAST(atmospheric_pressure_mbar AS numeric(15,3)) AS integer)              AS atmospheric_pressure_mbar
                    ,CAST(rainfall_mm AS numeric(15,3))                                             AS rainfall_mm
                    ,CAST(wind_speed_m_per_s AS numeric(15,3))                                      AS wind_speed_m_per_s
                    ,CAST(wind_direction_degrees AS numeric(15,3))                                  AS wind_direction_degrees
                    ,CAST(surface_temperature_c AS numeric(15,3))                                   AS surface_temperature_c
                    ,CAST(relative_humidity_percentage AS numeric(15,3))                            AS relative_humidity_percentage
                    ,CAST(solar_flux_kw_per_m2 AS numeric(15,3))                                    AS solar_flux_kw_per_m2
                    ,CAST(CASE WHEN battery_v NOT LIKE '%e%' THEN battery_v END AS numeric(15,3))   AS battery_v
                    ,file_id
                    ,ROW_NUMBER() OVER
                        (
                        PARTITION BY staging."Convert_WeatherReading_DateTime"(date_time_text_source)
                        ORDER BY CASE WHEN atmospheric_pressure_mbar LIKE '-%' THEN 1 ELSE 0 END, staged_row_id
                        /* Negative atmospheric pressure readings seem to be bad data so want to use them only if we have no alternative */
                        ) AS LoadRanking
            FROM    staging."JCMB_Weather_Staging"
            ) AS ConvertAndRank
            INNER JOIN staging."JCMB_Weather_LoadFiles_WithStatus" AS lf
                ON lf.file_id = ConvertAndRank.file_id
    WHERE   ConvertAndRank.LoadRanking = 1;

COMMENT ON VIEW staging."JCMB_Weather_Staging_Conversions"
IS 'Handle type conversions in a single place to aid clean upsert in proc.  Also removes duplicates in source data.';

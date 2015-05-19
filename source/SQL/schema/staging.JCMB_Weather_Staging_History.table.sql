
DROP TABLE IF EXISTS staging."JCMB_Weather_Staging_History" CASCADE;

CREATE TABLE staging."JCMB_Weather_Staging_History"
    (
    "staged_row_id"			            integer,
    "file_id"				            integer,
    "date_time_text_source"             character varying (500),
    "atmospheric_pressure_mbar"         character varying (500),
    "rainfall_mm"                       character varying (500),
    "wind_speed_m_per_s"                character varying (500),
    "wind_direction_degrees"            character varying (500),
    "surface_temperature_c"             character varying (500),
    "relative_humidity_percentage"      character varying (500),
    "solar_flux_kw_per_m2"             	character varying (500),
    "battery_v"                         character varying (500),
    "load_id"                           integer
    );

ALTER TABLE staging."JCMB_Weather_Staging_History" OWNER TO postgres;
 
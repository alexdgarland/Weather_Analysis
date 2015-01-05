DROP TABLE IF EXISTS staging."JCMB_Weather_Staging" CASCADE;
CREATE TABLE staging."JCMB_Weather_Staging"
    (
    "staged_row_id"			serial,
    "file_id"				integer NOT NULL,
    "date_time_text_source"             character varying (500),
    "atmospheric_pressure_mbar"         character varying (500),
    "rainfall_mm"                       character varying (500),
    "wind_speed_m_per_s"                character varying (500),
    "wind_direction_degrees"            character varying (500),
    "surface_temperature_c"             character varying (500),
    "relative_humidity_percentage"      character varying (500),
    "solar_flux_kw_per_m2"             	character varying (500),
    "battery_v"                         character varying (500)
    )
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_Staging" OWNER TO postgres;
ALTER TABLE staging."JCMB_Weather_Staging" ADD CONSTRAINT "PK_JCMB_Weather_Staging" PRIMARY KEY ("staged_row_id");
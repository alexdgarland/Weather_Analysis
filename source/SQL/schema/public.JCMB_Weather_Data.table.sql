
DROP TABLE IF EXISTS public."JCMB_Weather_Data";

CREATE TABLE public."JCMB_Weather_Data"
    (
    "date_time"                     timestamp without time zone NOT NULL,
    "atmospheric_pressure_mbar"     integer                     NOT NULL,
    "rainfall_mm"                   numeric(15,3)               NOT NULL,
    "wind_speed_m_per_s"            numeric(15,3)               NOT NULL,
    "wind_direction_degrees"        numeric(15,3)               NOT NULL,           
    "surface_temperature_c"         numeric(15,3)               NOT NULL,
    "relative_humidity_percentage"  numeric(15,3)               NOT NULL,
    "solar_flux_kw_per_m2"          numeric(15,3)               NOT NULL,
    "battery_v"                     numeric(15,3)               NOT NULL
    );

ALTER TABLE public."JCMB_Weather_Data"  OWNER TO postgres;

ALTER TABLE public."JCMB_Weather_Data"
    ADD CONSTRAINT PK_JCMB_Weather_Data
        PRIMARY KEY ("date_time");

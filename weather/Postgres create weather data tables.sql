
CREATE SCHEMA IF NOT EXISTS staging AUTHORIZATION postgres;


DROP TABLE IF EXISTS staging."JCMB_Weather_Loads" CASCADE;
CREATE TABLE staging."JCMB_Weather_Loads"
	(
	"load_id"		serial,
	"load_timestamp"	timestamp without time zone NOT NULL
	)
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_Loads" OWNER TO postgres;
ALTER TABLE staging."JCMB_Weather_Loads" ADD CONSTRAINT PK_JCMB_Weather_Loads PRIMARY KEY ("load_id");


CREATE OR REPLACE FUNCTION staging."AssignAndGetNewLoadID"()
RETURNS integer
AS
'INSERT INTO staging."JCMB_Weather_Loads"("load_timestamp") VALUES (clock_timestamp()) RETURNING load_id;'
LANGUAGE SQL;


DROP TABLE IF EXISTS staging."LoadFile_Statuses";
CREATE TABLE staging."LoadFile_Statuses"
	(
	"LoadFileStatusID"		integer,
	"LoadFileStatusDescription"	character varying(500)
	);
ALTER TABLE staging."LoadFile_Statuses" OWNER TO postgres;
ALTER TABLE staging."LoadFile_Statuses" ADD CONSTRAINT PK_LoadFile_Statuses PRIMARY KEY ("LoadFileStatusID");

INSERT INTO staging."LoadFile_Statuses" ("LoadFileStatusID", "LoadFileStatusDescription")
VALUES	(0, 'Registered, not processed'),
	(1, 'Staged'),
	(2, 'Loaded');


DROP TABLE IF EXISTS staging."JCMB_Weather_LoadFiles";
CREATE TABLE staging."JCMB_Weather_LoadFiles"
	(
	"file_id"		serial,
	"load_id"		integer,
	"load_timestamp"	timestamp without time zone NOT NULL
	)
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_LoadFiles" OWNER TO postgres;
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT PK_JCMB_Weather_LoadFiles PRIMARY KEY("file_id");
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT FK_JCMB_Weather_LoadFiles__LoadID FOREIGN KEY("load_id")
	REFERENCES staging."JCMB_Weather_Loads"("load_id");

DROP TABLE IF EXISTS staging."JCMB_Weather_Staging" CASCADE;
CREATE TABLE staging."JCMB_Weather_Staging"
    (
    "staged_row_id"				serial,
    "date_time"                         character varying (500),
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


CREATE OR REPLACE VIEW staging."JCMB_Weather_Staging_Summary"
AS
	SELECT	LEFT(date_time, 10) AS DayOfReading,
		COUNT(*)
	FROM 	staging."JCMB_Weather_Staging"
	GROUP BY LEFT(date_time, 10)
	ORDER BY DayOfReading DESC;


DROP TABLE IF EXISTS "JCMB_Weather_Data";
CREATE TABLE "JCMB_Weather_Data"
    (
    "date_time"                         timestamp without time zone NOT NULL,
    "atmospheric_pressure_mbar"         integer                     NOT NULL,
    "rainfall_mm"                       integer                     NOT NULL,
    "wind_speed_m_per_s"                numeric(15,3)               NOT NULL,
    "wind_direction_degrees"            numeric(15,3)               NOT NULL,           
    "surface_temperature_c"             numeric(15,3)               NOT NULL,
    "relative_humidity_percentage"      numeric(15,3)               NOT NULL,
    "solar_flux_kw_per_m2"             	integer                     NOT NULL,
    "battery_v"                         numeric(15,3)               NOT NULL
    );
ALTER TABLE "public"."JCMB_Weather_Data"  OWNER TO postgres;
ALTER TABLE "public"."JCMB_Weather_Data" ADD CONSTRAINT PK_JCMB_Weather_Data PRIMARY KEY ("date_time");


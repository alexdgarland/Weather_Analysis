DROP TABLE IF EXISTS staging."JCMB_Weather_LoadFiles" CASCADE;
DROP TYPE IF EXISTS file_state;

CREATE TYPE file_state AS ENUM ('registered', 'downloaded', 'staging started', 'staging complete', 'loaded');

CREATE TABLE staging."JCMB_Weather_LoadFiles"
	(
	"file_id"			serial NOT NULL,
	"source_file_name"		character varying(1000) NOT NULL,
	"source_file_modified_datetime"	timestamp without time zone NOT NULL,
	"load_id"			integer NOT NULL,
	"file_registered_timestamp"	timestamp without time zone NOT NULL DEFAULT clock_timestamp(),
	"file_latest_state"		file_state NOT NULL DEFAULT 'registered',		
	"downloaded_file_name"		character varying(1000) NOT NULL,
	"downloaded_datetime"		timestamp without time zone,
	"file_load_complete_timestamp"	timestamp without time zone
	)
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_LoadFiles" OWNER TO postgres;
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT PK_JCMB_Weather_LoadFiles PRIMARY KEY("file_id");
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT UQ_JCMB_Weather_LoadFiles__Name_ModifiedDate
	UNIQUE("source_file_name", "source_file_modified_datetime");
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT FK_JCMB_Weather_LoadFiles__LoadID FOREIGN KEY("load_id")
	REFERENCES staging."JCMB_Weather_Loads"("load_id");
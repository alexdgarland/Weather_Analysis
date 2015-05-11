DROP TABLE IF EXISTS staging."JCMB_Weather_LoadFile_Events" CASCADE;

CREATE TABLE staging."JCMB_Weather_LoadFile_Events"
    (
    "file_event_id"             serial NOT NULL,
    "file_id"                   integer NOT NULL,
    "file_event_state"          file_state NOT NULL,
    "file_event_load_id"        integer NOT NULL,
    "file_event_timestamp"      timestamp without time zone NOT NULL DEFAULT clock_timestamp()
    )
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_LoadFile_Events"
    ADD CONSTRAINT pk_jcmb_weather_loadfile_events PRIMARY KEY (file_event_id);
ALTER TABLE staging."JCMB_Weather_LoadFile_Events"
    ADD CONSTRAINT fk_jcmb_weather_loadfile_events__fileid FOREIGN KEY (file_id)
        REFERENCES staging."JCMB_Weather_LoadFiles" (file_id);
ALTER TABLE staging."JCMB_Weather_LoadFile_Events"
    ADD CONSTRAINT FK_JCMB_Weather_LoadFile_Events__LoadID FOREIGN KEY("file_event_load_id")
        REFERENCES staging."JCMB_Weather_Loads"("load_id");

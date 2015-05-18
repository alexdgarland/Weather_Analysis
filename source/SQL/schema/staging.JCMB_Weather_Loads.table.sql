
DROP TABLE IF EXISTS staging."JCMB_Weather_Loads" CASCADE;

CREATE TABLE staging."JCMB_Weather_Loads"
    (
    "load_id"               serial,
    "load_start_timestamp"  timestamp without time zone NOT NULL,
    "load_latest_state"     staging.load_state NOT NULL DEFAULT 'in progress',
    "load_end_timestamp"    timestamp without time zone
    )
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_Loads" OWNER TO postgres;
ALTER TABLE staging."JCMB_Weather_Loads" ADD CONSTRAINT PK_JCMB_Weather_Loads PRIMARY KEY ("load_id");

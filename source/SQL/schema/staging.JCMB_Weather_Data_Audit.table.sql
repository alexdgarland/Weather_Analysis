
DROP TABLE IF EXISTS staging."JCMB_Weather_Data_Audit";

CREATE TABLE staging."JCMB_Weather_Data_Audit"
    (
    entry_id        serial                      NOT NULL,
    entry_type      staging.audit_entry_type    NOT NULL,
    entry_timestamp timestamp without time zone NOT NULL default clock_timestamp(),
    date_time       timestamp without time zone NOT NULL,
    file_id         integer                     NOT NULL,
    load_id         integer                     NOT NULL
    );
    
ALTER TABLE staging."JCMB_Weather_Data_Audit" OWNER TO postgres;

ALTER TABLE staging."JCMB_Weather_Data_Audit"
    ADD CONSTRAINT PK_JCMB_Weather_Data_Audit
        PRIMARY KEY (entry_id);

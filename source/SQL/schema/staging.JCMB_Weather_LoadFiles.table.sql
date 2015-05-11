DROP TABLE IF EXISTS staging."JCMB_Weather_LoadFiles" CASCADE;

CREATE TABLE staging."JCMB_Weather_LoadFiles"
    (
    "file_id"                       serial NOT NULL,
    "source_file_name"              character varying(1000) NOT NULL,
    "source_file_modified_datetime" timestamp without time zone NOT NULL,
    "download_name"                 character varying(1000)
    )
WITH (OIDS=FALSE);
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT PK_JCMB_Weather_LoadFiles PRIMARY KEY("file_id");
ALTER TABLE staging."JCMB_Weather_LoadFiles" ADD CONSTRAINT UQ_JCMB_Weather_LoadFiles__Name_ModifiedDate
    UNIQUE("source_file_name", "source_file_modified_datetime");

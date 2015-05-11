CREATE OR REPLACE VIEW staging."JCMB_Weather_LoadFiles_WithStatus"
AS
    SELECT  lf."file_id",
            lf."source_file_name",
            lf."source_file_modified_datetime",
            rnk."file_event_state"              AS "current_state",
            rnk."file_event_load_id"            AS "latest_load_id",
            rnk."file_event_timestamp"          AS "latest_event_timestamp"
    FROM    staging."JCMB_Weather_LoadFiles" AS lf
            INNER JOIN  (
                        /* Rank events so we can get the latest (current) details as rank 1 */
                        SELECT  "file_id",
                                "file_event_state",
                                "file_event_load_id",
                                "file_event_timestamp",
                                row_number() over (PARTITION BY "file_id" ORDER BY "file_event_timestamp" DESC) AS EventRecencyRank
                        FROM    staging."JCMB_Weather_LoadFile_Events"
                        ) AS rnk
            ON  rnk.file_id = lf.file_id
            AND rnk.EventRecencyRank = 1;


CREATE OR REPLACE FUNCTION staging."GetLoadID"()
RETURNS integer
AS
$BODY$
DECLARE out_load_id int;
BEGIN

    -- See if we can get an open load ID from control table
    SELECT  load_id
    FROM    staging."JCMB_Weather_Loads"
    WHERE   staging."IsActiveState"(load_latest_state)
    INTO    out_load_id
    ORDER BY load_start_timestamp DESC
    LIMIT 1;

    IF out_load_id IS NOT NULL THEN
    -- If we got one open load ID, close any ** other ** open load IDs that may be in table.
    -- These should not exist but we should "park" them so can check later.
        UPDATE  staging."JCMB_Weather_Loads"
        SET     load_latest_state = 'automatically closed'
        WHERE   staging."IsActiveState"(load_latest_state)
        AND     load_id <> out_load_id;
    ELSE
    -- Create a new load ID and use it
        INSERT INTO staging."JCMB_Weather_Loads"("load_start_timestamp")
        VALUES (clock_timestamp())
        RETURNING load_id INTO out_load_id;
    END IF;

    RETURN out_load_id;

END
$BODY$
LANGUAGE plpgsql;
ALTER FUNCTION staging."GetLoadID"() OWNER TO postgres;
  

CREATE OR REPLACE FUNCTION staging."LoadIsActive"(load_id_to_check integer)
RETURNS boolean
AS
$BODY$
DECLARE load_is_active boolean;
BEGIN

    SELECT  COUNT(*) != 0 
    FROM    staging."JCMB_Weather_Loads"
    WHERE   load_id = load_id_to_check
    AND     staging."IsActiveState"(load_latest_state)
    INTO    load_is_active;

    RETURN load_is_active;

END
$BODY$
LANGUAGE plpgsql;

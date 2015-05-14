
CREATE OR REPLACE FUNCTION staging."IsActiveState"(state_to_check load_state)
RETURNS BOOLEAN
AS
$BODY$
BEGIN
    RETURN (state_to_check IN ('initialised', 'in progress'));
END
$BODY$
LANGUAGE plpgsql;

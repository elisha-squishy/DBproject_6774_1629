-- PROCEDURE: public.update_maintenance_status(integer, text)

-- DROP PROCEDURE IF EXISTS public.update_maintenance_status(integer, text);

CREATE OR REPLACE PROCEDURE public.update_maintenance_status(
	IN p_req_id integer,
	IN p_new_status text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
  current_status TEXT;
  current_rank INT;
  new_rank INT;
BEGIN
  -- Fetch the current status
  SELECT req_status INTO current_status
  FROM maintenance_req
  WHERE request_id = p_req_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Maintenance request ID % not found', p_req_id;
  END IF;

  -- Assign numeric ranks to statuses for easy comparison
  CASE current_status
    WHEN 'received' THEN current_rank := 1;
    WHEN 'processed' THEN current_rank := 2;
    WHEN 'taken care of' THEN current_rank := 3;
    ELSE RAISE EXCEPTION 'Unknown current status: %', current_status;
  END CASE;

  CASE p_new_status
    WHEN 'received' THEN new_rank := 1;
    WHEN 'processed' THEN new_rank := 2;
    WHEN 'taken care of' THEN new_rank := 3;
    ELSE RAISE EXCEPTION 'Invalid new status: %', p_new_status;
  END CASE;

  -- Check for downgrade
  IF new_rank < current_rank THEN
    RAISE EXCEPTION 'Cannot downgrade status from % to %', current_status, p_new_status;
  END IF;

  -- Perform the update
  UPDATE maintenance_req
  SET req_status = p_new_status
  WHERE request_id = p_req_id;

  -- Log the status update
  INSERT INTO updates_log(description)
  VALUES (
    'Maintenance request ' || p_req_id || ' status updated from "' || current_status || '" to "' || p_new_status || '"'
  );
END;
$BODY$;
ALTER PROCEDURE public.update_maintenance_status(integer, text)
    OWNER TO sibony;

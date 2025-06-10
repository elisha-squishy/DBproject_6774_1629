CREATE OR REPLACE FUNCTION public.check_maintenance_status()
RETURNS trigger
BEGIN
	IF UPPER(NEW.req_status) <> 'RECEIVED' THEN
    RAISE EXCEPTION 'Maintenance request status must be "Received".';
END IF;
RETURN NEW;
END;
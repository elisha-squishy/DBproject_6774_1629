-- update birthdays, make the location of the event at the resident's room and record in log
CREATE OR REPLACE FUNCTION create_upcoming_birthday_events()
RETURNS VOID AS $$
DECLARE
  r RECORD;
  v_event_date DATE := CURRENT_DATE + INTERVAL '1 day';
  v_age INT;
  v_room INT;
  v_event_name VARCHAR(100);
BEGIN
  FOR r IN
    SELECT residentid, firstname, lastname, dateofbirth, roomnumber
    FROM resident re
    JOIN room ro ON re.roomid = ro.roomid 
    WHERE EXTRACT(MONTH FROM re.dateofbirth) = EXTRACT(MONTH FROM v_event_date)
      AND EXTRACT(DAY FROM re.dateofbirth) = EXTRACT(DAY FROM v_event_date)
  LOOP
    -- Use existing function to get current age
    v_age := get_resident_age(r.residentid) + 1;
    v_room := r.roomnumber;

    -- Construct event title
    v_event_name := r.firstname || ' ' || r.lastname || '''s ' || v_age || ' birthday!';

    -- Insert birthday event
    CALL add_event(v_event_name, v_event_date, CAST(v_room AS VARCHAR));

    -- Log the event creation
    INSERT INTO updates_log(description)
    VALUES ('Birthday event added: "' || v_event_name || '" for ' || v_event_date);
  END LOOP;
END;
$$ LANGUAGE plpgsql;

-- select create_upcoming_birthday_events();
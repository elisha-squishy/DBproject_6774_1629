--generates a unique id for an event i want to insert
CREATE OR REPLACE PROCEDURE add_event(
  p_name VARCHAR(100),
  p_date DATE,
  p_location VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_event_id INT;
BEGIN
  -- Generate unique event_id using timestamp and random number
  v_event_id := TRUNC(RANDOM() * 100000)::INT;

  -- Insert into event table
  INSERT INTO event(event_id, event_name, event_date, event_location)
  VALUES (v_event_id, p_name, p_date, p_location);

  -- Optional: output confirmation
  RAISE NOTICE 'Event % added with ID: %', p_name, v_event_id;
END;
$$;

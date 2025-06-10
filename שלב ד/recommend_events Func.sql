CREATE OR REPLACE PROCEDURE log_recommendation_request(
    target_resident_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Simple logging or could do other setup
    INSERT INTO updates_log(description)
	VALUES('Getting recommendations for resident ' || target_resident_id);
END;
$$;

-- Main function - recommend events based on similar age groups
CREATE OR REPLACE FUNCTION recommend_events(target_resident_id INT)
RETURNS TABLE(
    event_date DATE,
    event_location VARCHAR,
    similar_age_attendees BIGINT
)
LANGUAGE plpgsql
AS $$
DECLARE
    target_age INT;
BEGIN
    -- Log the request
    CALL log_recommendation_request(target_resident_id);
    
    -- Get target resident's age
    SELECT get_resident_age(target_resident_id) INTO target_age;
    
    -- Return future events attended by residents within 5 years of target's age
    RETURN QUERY
    SELECT 
        e.event_date,
        e.event_location,
        COUNT(ve.resident_id) as similar_age_attendees
    FROM event e
    JOIN visiting_event ve ON e.event_id = ve.event_id
    -- WHERE e.event_date >= CURRENT_DATE
      WHERE e.event_id NOT IN (
          SELECT event_id 
          FROM visiting_event 
          WHERE resident_id = target_resident_id
      )
      AND get_resident_age(ve.resident_id) BETWEEN (target_age - 5) AND (target_age + 5)
    GROUP BY e.event_id, e.event_date, e.event_location
    ORDER BY COUNT(ve.resident_id) DESC
    LIMIT 10;
END;
$$;

-- SELECT * FROM recommend_events(123);
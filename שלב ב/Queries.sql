//events that a residant visited
SELECT 
    r.resident_name,
    e.event_name,
    e.event_date,
    EXTRACT(YEAR FROM e.event_date) AS event_year,
    EXTRACT(MONTH FROM e.event_date) AS event_month
FROM resident r
JOIN visiting_event ve ON r.resident_id = ve.resident_id
JOIN event e ON ve.event_id = e.event_id
ORDER BY event_year, event_month;

//maintenance_reqs for each room, with the rooms capcity
SELECT 
    rm.room_id,
    rm.capacity,
    COUNT(mr.request_id) AS total_requests
FROM room rm
LEFT JOIN maintenance_req mr ON rm.room_id = mr.room_id
GROUP BY rm.room_id, rm.capacity
ORDER BY total_requests DESC;


//the devision of items: how many have 1 of them, how meny have 2, .. until how many have 6 or more
SELECT 
    CASE 
        WHEN quantity >= 6 THEN '6 or more'
        ELSE quantity::text
    END AS quantity_group,
    COUNT(*) AS item_count
FROM inventory
GROUP BY quantity_group
ORDER BY 
    CASE 
        WHEN quantity_group = '6 or more' THEN 7
        ELSE quantity_group::int
    END;


//the devision of going to events: how many dont go to any, how many go to one, go to 2, go to three and more
WITH event_counts AS (
    SELECT 
        resident_id,
        COUNT(event_id) AS events_visited
    FROM visiting_event
    GROUP BY resident_id
)
SELECT 
    CASE 
        WHEN events_visited IS NULL THEN '0'
        WHEN events_visited >= 3 THEN '3 or more'
        ELSE events_visited::text
    END AS event_count_group,
    COUNT(*) AS resident_count
FROM resident r
LEFT JOIN event_counts ec ON r.resident_id = ec.resident_id
GROUP BY event_count_group
ORDER BY 
    CASE 
        WHEN event_count_group = '0' THEN 0
        WHEN event_count_group = '1' THEN 1
        WHEN event_count_group = '2' THEN 2
        WHEN event_count_group = '3 or more' THEN 3
    END;


//for each staff member, show how many requests he has completed
SELECT 
    s.staff_member_name,
    COUNT(mr.request_id) AS completed_requests
FROM staff_member s
LEFT JOIN maintenance_req mr 
    ON s.staff_member_id = mr.staff_member_id AND mr.req_status = 'Completed'
GROUP BY s.staff_member_name
ORDER BY completed_requests DESC;

//how many chefs are in charge of breakfast over time
SELECT 
    m.date,
    COUNT(DISTINCT ic.staff_member_id) AS breakfast_chefs_count
FROM meal m
JOIN is_chef ic ON m.meal_type = ic.meal_type
WHERE m.meal_type = 'Breakfast'
GROUP BY m.date
ORDER BY m.date;

//amount of residents that have made less than 2 maintenance reqs, and amount of residents that made more than 2 maintenance reqs
WITH req_counts AS (
    SELECT 
        resident_id,
        COUNT(*) AS req_count
    FROM maintenance_req
    GROUP BY resident_id
)
SELECT 
    CASE 
        WHEN req_count < 2 THEN 'Less than 2'
        WHEN req_count > 2 THEN 'More than 2'
    END AS category,
    COUNT(*) AS resident_count
FROM req_counts
WHERE req_count < 2 OR req_count > 2
GROUP BY category;

//missing 1



UPDATE maintenance_req
SET req_status = 'Completed'
WHERE request_id = 101;

UPDATE inventory
SET quantity = quantity - 1
WHERE item_name = 'Milk' AND quantity > 0;

UPDATE room
SET room_floor = 2
WHERE room_id = 'R105';


DELETE FROM maintenance_req
WHERE req_status = 'Completed';

DELETE FROM resident
WHERE resident_dob < '1940-01-01';

DELETE FROM inventory
WHERE quantity = 0;
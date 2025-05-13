-- top 5 events (by the amount of the residents)
SELECT 
    e.event_name,
    COUNT(ve.resident_id) AS num_visitors
FROM 
    event e
JOIN 
    visiting_event ve ON e.event_id = ve.event_id
GROUP BY 
    e.event_id, e.event_name
ORDER BY 
    num_visitors DESC
LIMIT 5;

-- maintenance_reqs for each room, with the rooms capcity
SELECT 
    rm.room_id,
    rm.capacity,
    COUNT(mr.request_id) AS total_requests
FROM room rm
LEFT JOIN maintenance_req mr ON rm.room_id = mr.room_id
GROUP BY rm.room_id, rm.capacity
ORDER BY total_requests DESC;

-- the devision of going to events: how many go to 1 event, 2 events etc..
WITH event_counts AS (
    SELECT 
        resident_id,
        COUNT(event_id) AS events_visited
    FROM visiting_event
    GROUP BY resident_id
)
SELECT events_visited, COUNT(*) AS resident_count
FROM resident r
LEFT JOIN event_counts ec ON r.resident_id = ec.resident_id
GROUP BY events_visited

-- top 3 most used items
SELECT 
	inv.item_name,
    inv.item_id,
    COUNT(mr.request_id) AS num_uses
FROM 
    maintenance_req mr
JOIN 
    inventory inv ON mr.item_id = inv.item_id
GROUP BY 
    inv.item_id
ORDER BY 
    num_uses DESC
LIMIT 3;

-- how many chefs are in charge of meals over time
SELECT
    m.date,
    COUNT(DISTINCT ic.staff_member_id) AS chefs_count
FROM meal m
JOIN is_chef ic ON m.date = ic.date AND m.meal_type = ic.meal_type
GROUP BY m.date
ORDER BY m.date;

-- amount of rooms that have made less than 2 maintenance reqs, and amount of rooms that made more than 2 maintenance reqs
WITH req_counts AS (
    SELECT 
        room_id,
        COUNT(*) AS req_count
    FROM maintenance_req
    GROUP BY room_id
)
SELECT 
    CASE 
		WHEN req_count IS NULL THEN 'Less or equal 2'
        WHEN req_count <= 2 THEN 'Less or equal 2'
        WHEN req_count > 2 THEN 'More than 2'
    END AS category,
    COUNT(*) AS resident_count
FROM req_counts right OUTER JOIN room ON req_counts.room_id = room.room_id
GROUP BY category;

-- for each job title, shows the staff memebers that have completed the most requests
SELECT 
    sm.job_title,
    sm.staff_member_name,
    COUNT(mr.request_id) AS handled_requests
FROM staff_member sm
JOIN maintenance_req mr ON sm.staff_member_id = mr.staff_member_id
GROUP BY sm.job_title, sm.staff_member_name
HAVING COUNT(mr.request_id) = (
    SELECT MAX(request_count)
    FROM (
        SELECT COUNT(mr2.request_id) AS request_count
        FROM staff_member sm2
        JOIN maintenance_req mr2 ON sm2.staff_member_id = mr2.staff_member_id
        WHERE sm2.job_title = sm.job_title
        GROUP BY sm2.staff_member_name
    ) AS subquery
)
ORDER BY sm.job_title;

-- shows for each room its capacity and how many actually lives there
SELECT 
    rm.room_id,
    rm.capacity,
    COUNT(r.resident_id) AS current_occupancy
FROM room rm
LEFT JOIN resident r ON rm.room_id = r.room_id
GROUP BY rm.room_id, rm.capacity
HAVING COUNT(r.resident_id) < rm.capacity
ORDER BY rm.room_id;



UPDATE maintenance_req
SET req_status = 'taken care of'
WHERE request_id = 102;

UPDATE inventory
SET quantity = quantity - 1
WHERE item_id = 15 AND quantity > 0;

UPDATE room
SET room_floor = 3
where room_floor = 4


DELETE FROM room
WHERE capacity > 18;

DELETE FROM resident
WHERE EXTRACT(YEAR FROM resident_dob) < 2020;

DELETE FROM inventory
WHERE quantity < 2;
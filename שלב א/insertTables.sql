-- Insert data into room
INSERT INTO room (room_id, room_floor, capacity) VALUES
(1, 1, 2),
(2, 4, 1),
(3, 7, 3);

-- Insert data into resident
INSERT INTO resident (resident_id, room_id, resident_name, resident_dob) VALUES
(1, 1, 'John Doe', '1945-06-15'),
(2, 2, 'Jane Smith', '1950-09-23'),
(3, 3, 'Alice Johnson', '1938-11-05');

-- Insert data into event
INSERT INTO event (event_id, event_name, event_date, event_location) VALUES
(1, 'Music Night', '2025-04-01', 'Common Hall'),
(2, 'Movie Screening', '2025-04-05', 'Theater Room'),
(3, 'Art Workshop', '2025-04-10', 'Activity Center');

-- Insert data into visiting_event
INSERT INTO visiting_event (resident_id, event_id) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Insert data into staff_member
INSERT INTO staff_member (staff_member_id, staff_member_name, job_title) VALUES
(1, 'Robert Brown', 'Nurse'),
(2, 'Emily Davis', 'Caretaker'),
(3, 'Michael Wilson', 'Chef');

-- Insert data into inventory
INSERT INTO inventory (item_id, item_name, quantity) VALUES
(1, 'Wheelchair', 5),
(2, 'Oxygen Tank', 10),
(3, 'Walking Cane', 15);

-- Insert data into maintenance_req
INSERT INTO maintenance_req (request_id, room_id, staff_member_id, item_id, req_description, req_status) VALUES
(1, 1, 1, 1, 'Wheelchair needs repair', 'Pending'),
(2, 2, 2, 2, 'Oxygen tank replacement', 'Completed'),
(3, 3, 3, 3, 'Walking cane broken', 'In Progress');

-- Insert data into meal
INSERT INTO meal (meal_type, day_of_the_week, menu, date) VALUES
('Breakfast', 'Monday', 'Oatmeal; Toast; Coffee', '1945-06-15'),
('Lunch', 'Wednesday', 'Grilled Chicken; Rice; Salad', '1945-06-16'),
('Dinner', 'Friday', 'Pasta; Garlic Bread; Soup', '1945-06-17');

-- Insert data into is_chef
INSERT INTO is_chef (staff_member_id, meal_type, day_of_the_week, date) VALUES
(3, 'Breakfast', 'Monday', '1945-06-15'),
(3, 'Lunch', 'Wednesday', '1945-06-16'),
(3, 'Dinner', 'Friday', '1945-06-17');
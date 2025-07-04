CREATE TABLE room (
    room_id INT PRIMARY KEY,
    room_floor INT,
    capacity INT
);

CREATE TABLE inventory (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(50),
    quantity INT
);

CREATE TABLE resident (
    residentid INT PRIMARY KEY,
	roomid INT,
    firstname VARCHAR(30),
lastname VARCHAR(30),
    dateofbirth DATE,
FOREIGN KEY (roomid) REFERENCES room(room_id)
);

CREATE TABLE meal (
    meal_type VARCHAR(10),
    day_of_the_week VARCHAR(10),
	menu VARCHAR(100),
	date DATE,
    PRIMARY KEY (meal_type, day_of_the_week, date)
);

CREATE TABLE event (
    event_id INT PRIMARY KEY,
    event_name VARCHAR(50),
    event_date DATE,
    event_location VARCHAR(30)
);

CREATE TABLE visiting_event (
    resident_id INT,
    event_id INT,
    PRIMARY KEY (resident_id, event_id),
    FOREIGN KEY (resident_id) REFERENCES resident(resident_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

CREATE TABLE staff_member (
    staff_member_id INT PRIMARY KEY,
    staff_member_name VARCHAR(30),
    job_title VARCHAR(50)
);

CREATE TABLE maintenance_req (
    request_id INT,
    room_id INT,
	staff_member_id INT,
	item_id INT,
    req_description VARCHAR(100),
    req_status VARCHAR(50),
	PRIMARY KEY (request_id, staff_member_id, room_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id),
	FOREIGN KEY (staff_member_id) REFERENCES staff_member(staff_member_id),
	FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);

CREATE TABLE is_chef (
	date DATE,
    day_of_the_week VARCHAR(10),
    meal_type VARCHAR(10),
    staff_member_id INT,
    PRIMARY KEY (staff_member_id, meal_type, day_of_the_week, date),
    FOREIGN KEY (staff_member_id) REFERENCES staff_member(staff_member_id),
    FOREIGN KEY (meal_type, day_of_the_week, date) REFERENCES meal(meal_type, day_of_the_week, date)
);
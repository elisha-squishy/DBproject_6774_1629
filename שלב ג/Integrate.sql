CREATE TABLE resident_temp (
    resident_id INT PRIMARY KEY,
    room_id INT,
    resident_name VARCHAR(30),
    resident_dob DATE,
    FOREIGN KEY (room_id) REFERENCES room(roomid)
);

MERGE INTO resident AS t1
USING resident_temp AS t2
ON t1.residentid = t2.resident_id
WHEN NOT MATCHED THEN
    INSERT (residentid, firstname, lastname, dateofbirth, admissiondate, roomid)
    VALUES (
        t2.resident_id,
        SPLIT_PART(t2.resident_name, ' ', 1),
        SPLIT_PART(t2.resident_name, ' ', 2),
        t2.resident_dob,
        '01/01/2021',
        t2.room_id
    );
	
drop table resident_temp;
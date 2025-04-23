ALTER TABLE maintenance_req
ALTER COLUMN req_status SET DEFAULT 'Pending';

ALTER TABLE resident
ADD CONSTRAINT uq_resident_name_dob
UNIQUE (resident_name, resident_dob);

ALTER TABLE room
ADD CONSTRAINT chk_smaller_than_ten
CHECK (capacity <= 10);

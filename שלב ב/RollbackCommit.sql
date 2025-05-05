BEGIN;
INSERT INTO resident (resident_id, room_id, resident_name, resident_dob)
VALUES (2000, 2, 'Rachel Green', '1990-03-22');

ROLLBACK;

BEGIN;
INSERT INTO resident (resident_id, room_id, resident_name, resident_dob)
VALUES (2000, 2, 'Rachel Green', '1990-03-22');
COMMIT;
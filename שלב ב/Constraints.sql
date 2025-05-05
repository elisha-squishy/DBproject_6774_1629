ALTER TABLE visiting_event
DROP CONSTRAINT visiting_event_resident_id_fkey;
-- Add the new one with ON DELETE CASCADE
ALTER TABLE visiting_event
ADD CONSTRAINT visiting_event_resident_id_fkey FOREIGN KEY (resident_id)
ON DELETE CASCADE;
REFERENCES resident (resident_id)

ALTER TABLE maintenance_req
ALTER COLUMN req_status SET DEFAULT 'Pending';

ALTER TABLE resident
ADD CONSTRAINT uq_resident_name_dob
UNIQUE (resident_name, resident_dob);

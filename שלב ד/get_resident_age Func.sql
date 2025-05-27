-- helper function to calculate a resident age
CREATE OR REPLACE FUNCTION get_resident_age(p_resident_id INT)
RETURNS INT AS $$
DECLARE
  v_dob DATE;
  v_age INT;
BEGIN
  -- Get the resident's date of birth
  SELECT dateofbirth INTO v_dob
  FROM resident
  WHERE resident_id = p_resident_id;

  -- Calculate the age
  v_age := DATE_PART('year', AGE(CURRENT_DATE, v_dob));

  RETURN v_age;

EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE EXCEPTION 'Resident with ID % not found.', p_resident_id;
END;
$$ LANGUAGE plpgsql;

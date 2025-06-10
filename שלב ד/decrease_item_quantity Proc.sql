CREATE OR REPLACE PROCEDURE decrease_item_quantity(
    target_item_id INT,
    decrease_amount INT DEFAULT 1
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Update the quantity
	
    UPDATE inventory 
    SET quantity = quantity - decrease_amount
    WHERE item_id = target_item_id AND quantity > decrease_amount;
	
    -- Check if update affected any rows
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item with ID % not found', target_item_id;
    END IF;
    
    INSERT INTO updates_log(description)
	VALUES('Decreased quantity of item ' || target_item_id || ' by ' || decrease_amount);
END;
$$;






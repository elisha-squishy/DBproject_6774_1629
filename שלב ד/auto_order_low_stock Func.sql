CREATE OR REPLACE FUNCTION auto_order_low_stock()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if quantity dropped below 5
    IF NEW.quantity < 5 THEN
        -- Check if we haven't already placed a pending order for this item
        IF NOT EXISTS (
            SELECT 1 FROM orders 
            WHERE item_id = NEW.item_id 
            AND status = 'PENDING'
        ) THEN
            -- Insert new order
            INSERT INTO orders (item_id, item_name, order_quantity)
            VALUES (NEW.item_id, NEW.item_name, 10);
            
            RAISE NOTICE 'Auto-ordered 10 units of % (ID: %) - stock level: %', 
                         NEW.item_name, NEW.item_id, NEW.quantity;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$;

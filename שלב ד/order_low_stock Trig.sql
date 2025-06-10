CREATE OR REPLACE TRIGGER order_low_stock
    AFTER UPDATE OF quantity ON inventory
    FOR EACH ROW
    WHEN (NEW.quantity < 5)
    EXECUTE FUNCTION auto_order_low_stock();

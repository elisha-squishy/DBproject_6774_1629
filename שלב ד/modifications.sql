CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    item_name VARCHAR(50),
    order_quantity INT DEFAULT 10,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'PENDING'
);


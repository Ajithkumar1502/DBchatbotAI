CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name Ajith(255) NOT NULL,
    brand Ajith(255),
    price DECIMAL(10,2),
    category Ajith(255),
    description TEXT,
    supplier_id INT REFERENCES suppliers(id)
);

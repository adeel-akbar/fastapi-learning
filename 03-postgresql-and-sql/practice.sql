-- =========================
-- SELECT
-- =========================

-- Show all rows and columns from the products table.
SELECT * FROM products;


-- Show a specific row using a condition.
SELECT * FROM products
WHERE id = 5;


-- Select only specific columns.
SELECT name, price FROM products
WHERE id = 6;


-- =========================
-- WHERE & OPERATORS
-- =========================

-- Greater than
SELECT * FROM products
WHERE price > 20;

-- Less than
SELECT * FROM products
WHERE price < 100;

-- NOT EQUAL
-- <> and != both mean "not equal to".
SELECT * FROM products
WHERE price <> 50;

SELECT * FROM products
WHERE price != 50;


-- Using OR
SELECT * FROM products
WHERE price > 20 OR price < 100;


-- Using IN
-- Checks whether a value matches any value in the list.
SELECT * FROM products
WHERE id IN (1, 2, 3);


-- Using LIKE
-- % means any number of characters.
SELECT * FROM products
WHERE name LIKE '%phone%';


-- =========================
-- INSERT
-- =========================

-- Insert a new row.
INSERT INTO products (name, price)
VALUES ('Laptop', 500);


-- =========================
-- UPDATE
-- =========================

-- Modify existing data.
UPDATE products
SET name = 'Updated Laptop', price = 600
WHERE id = 5;


-- =========================
-- DELETE
-- =========================

-- Delete a specific row.
DELETE FROM products
WHERE id = 5;


-- =========================
-- ORDER BY
-- =========================

-- Sort by price from lowest to highest.
SELECT * FROM products
ORDER BY price ASC;


-- =========================
-- LIMIT & OFFSET
-- =========================

-- Return a limited number of rows and skip the first 2 rows.
SELECT * FROM products
LIMIT 6 OFFSET 2;
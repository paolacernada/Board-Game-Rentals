-- Project Group 102

-- Team Members Names:
-- Luis Sosa Lora 
-- Paola Cernada

-- Project Title:
-- Board Game Rentals


-- SELECT QUERIES FOR ALL FIVE TABLES --

-- Get all the customers IDs to populate the add and update invoices dropdown
SELECT customer_id, customer_name FROM customers;

-- Get all the employees IDs and names to populate the add and update invoices dropdown
SELECT employee_id, employee_full_name FROM employees;

-- Get all board game details for the Board Games page
SELECT
    bg_id AS "Board Game ID",
    bg_name AS "Board Game Name",
    daily_rental_rate AS "Daily Rental Rate",
    number_of_copies_in_stock AS "Copies In Stock",
    available_to_rent AS "Copies Available to Rent",
    quantity_checked_out AS "Copies Checked Out"
FROM
    board_games
ORDER BY
    bg_id ASC;

-- Get all customer details for the Customers page
SELECT
    customer_id AS "Customer ID",
    customer_name AS "Name",
    email AS "Email",
    total_quantity_of_bgs_checked_out AS "Games Checked Out",
    total_amount_spent AS "Total Amount Spent"
FROM
    customers;

-- Get data of one customer to update the customer's information
SELECT * FROM customers WHERE customer_id = %s;

-- Get all employee details for the Employees page
SELECT
    employee_id AS "Employee ID",
    employee_full_name AS "Employee Name"
FROM
    employees;

-- Get all invoice table info for the Invoices page
SELECT
    invoices.invoice_id AS "Invoice ID",
    CONCAT(
        customers.customer_id,
        ' - ',
        customers.customer_name
    ) AS "Customer ID - Name",
    IFNULL(employees.employee_id, "NULL") AS "Employee ID",
    date_checked_out AS "Date Checked Out",
    total_due AS "Total Due"
FROM
    invoices
    INNER JOIN customers ON customers.customer_id = invoices.customer_id
    LEFT JOIN employees ON employees.employee_id = invoices.employee_id
ORDER BY
    invoice_id ASC;

-- Get all invoice details table info for the Invoice Details page
SELECT
    invoice_details.invoice_details_id AS "Invoice Details ID",
    invoices.invoice_id AS "Invoice ID",
    CONCAT(board_games.bg_id, ' - ', board_games.bg_name) AS "Board Game ID - Name",
    length_of_rental AS "Length of Rental",
    board_games.daily_rental_rate AS "Daily Rental Rate",
    line_total AS "Line Total"
FROM
    invoice_details
    INNER JOIN invoices ON invoices.invoice_id = invoice_details.invoice_id
    INNER JOIN board_games ON board_games.bg_id = invoice_details.bg_id
ORDER BY
    invoice_details_id ASC;

-- QUERIES FOR THE BOARD GAMES TABLE --

-- Add a board game
INSERT INTO board_games (bg_name, daily_rental_rate, number_of_copies_in_stock, available_to_rent, quantity_checked_out) VALUES (%s, %s, %s, %s, %s);

-- Update a board game's data
UPDATE board_games SET bg_name = %s, daily_rental_rate = %s, number_of_copies_in_stock = %s, available_to_rent = %s, quantity_checked_out = %s WHERE bg_id = %s;

-- Delete a board game
DELETE FROM board_games WHERE bg_id = %s;

-- QUERIES FOR THE CUSTOMERS TABLE --

-- Add a customer
INSERT INTO customers (customer_name, email, total_quantity_of_bgs_checked_out, total_amount_spent) VALUES (%s, %s, %s, %s);

-- Update a customer's information
UPDATE customers SET customer_name = %s, email = %s, total_quantity_of_bgs_checked_out = %s, total_amount_spent = %s WHERE customer_id = %s;

-- Delete a customer
DELETE FROM customers WHERE customer_id = %s;

-- QUERIES FOR THE EMPLOYEES TABLE --

-- Add an employee
INSERT INTO
    employees (employee_full_name)
VALUES
    (:employee_full_name_Input);

-- Update an employee's information
UPDATE employees SET employee_full_name = %s WHERE employee_id = %s;

-- Delete an employee
DELETE FROM employees WHERE employee_id = %s;

-- QUERIES FOR THE INVOICES TABLE --

-- Add an invoice if employee_id is NULL
INSERT INTO invoices (customer_id, date_checked_out, total_due) VALUES (%s, %s, %s);

-- Add an invoice if employee_id is not NULL
INSERT INTO invoices (customer_id, employee_id, date_checked_out, total_due) VALUES (%s, %s, %s, %s);

-- Update an invoice
UPDATE invoices SET customer_id = %s, employee_id = %s, date_checked_out = %s, total_due = %s WHERE invoice_id = %s;

-- Delete an invoice
DELETE FROM invoices WHERE invoice_id = %s;

-- Select for dynamic drop-downs
SELECT
    customer_id,
    customer_name
FROM
    customers;

SELECT
    employee_id,
    employee_full_name
FROM
    employees;

-- QUERIES FOR THE INVOICE DETAILS TABLE --

-- Add data to invoice details
INSERT INTO invoice_details (invoice_id, bg_id, length_of_rental, daily_rental_rate, line_total) VALUES (%s, %s, %s, %s, %s);

-- Update an invoice details' data
UPDATE invoice_details SET invoice_id = %s, bg_id = %s, length_of_rental = %s, daily_rental_rate = %s, line_total = %s WHERE invoice_details_id = %s;

-- Delete an invoice details' data
DELETE FROM invoice_details WHERE invoice_details_id = %s;

-- Select for dynamic drop-downs
SELECT
    invoice_id
FROM
    invoices
ORDER BY
    invoice_id ASC;

SELECT
    bg_id
FROM
    board_games
ORDER BY
    bg_id ASC;

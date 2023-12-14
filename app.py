from flask import Flask, request, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from datetime import datetime
import os
import database.db_connector as db

app = Flask(__name__, static_folder='./static')
db_connection = db.connect_to_database()

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_cernadap'
app.config['MYSQL_PASSWORD'] = 'Natasha2*' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_cernadap'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# The above import statements and connections where adapted from the starter code.
# The below routes where adapted from the starter code.

# Routes
@app.route('/')
def root():

    return render_template("index.html")


@app.route('/index.html')
def index():

    return render_template("index.html")


# Board Games Table

@app.route('/board_games.html', methods=["POST", "GET"])
def board_games():
    if request.method == "POST":
        if request.form.get("add_board_game"):
            # grab user form inputs
            bg_name = request.form["bg_name"]
            daily_rental_price = request.form["daily_rental_price"]
            copies_in_stock = request.form["copies_in_stock"]
            copies_available_to_rent = request.form["copies_available_to_rent"]
            copies_checked_out = request.form["copies_checked_out"]

            query = "INSERT INTO board_games (bg_name, daily_rental_rate, number_of_copies_in_stock, available_to_rent, quantity_checked_out) VALUES (%s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (bg_name, daily_rental_price, copies_in_stock, copies_available_to_rent, copies_checked_out))
            mysql.connection.commit()
        return redirect("/board_games.html")

    query = 'SELECT bg_id AS "Board Game ID", bg_name AS "Board Game Name", daily_rental_rate AS "Daily Rental Rate", number_of_copies_in_stock AS "Copies In Stock", available_to_rent AS "Copies Available to Rent", quantity_checked_out AS "Copies Checked Out" FROM board_games ORDER BY bg_id ASC;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("board_games.jinja", board_games=results)

@app.route('/board_games-add.html', methods=["POST", "GET"])
def board_games_add():
    return render_template("board_games-add.jinja")

@app.route('/board_games-update.html', methods=["POST", "GET"])
def board_games_update():
    if request.method == "POST":
        if request.form.get("update_board_game"):
            # Process the form submission for updating the board game
            bg_id = request.form["bg_id"]
            bg_name = request.form["bg_name"]
            daily_rental_price = request.form["daily_rental_price"]
            copies_in_stock = request.form["copies_in_stock"]
            copies_available_to_rent = request.form["copies_available_to_rent"]
            copies_checked_out = request.form["copies_checked_out"]

            query = "UPDATE board_games SET bg_name = %s, daily_rental_rate = %s, number_of_copies_in_stock = %s, available_to_rent = %s, quantity_checked_out = %s WHERE bg_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (bg_name, daily_rental_price, copies_in_stock, copies_available_to_rent, copies_checked_out, bg_id))
            mysql.connection.commit()
            return redirect("/board_games.html")

    bg_id = request.args.get("bg_id")  # Get the bg_id from the URL query parameters
    query = "SELECT * FROM board_games WHERE bg_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (bg_id,))
    result = cur.fetchone()

    if result is None:
        # Handle the case when no record is found
        print("No record found for bg_id:", bg_id)
        return redirect("/board_games.html")

    # Debugging statements
    print("Result:", result)

    bg_id = result['bg_id']
    bg_name = result['bg_name']
    daily_rental_price = result['daily_rental_rate']
    copies_in_stock = result['number_of_copies_in_stock']
    copies_available_to_rent = result['available_to_rent']
    copies_checked_out = result['quantity_checked_out']

    board_games = [bg_id, bg_name, daily_rental_price, copies_in_stock, copies_available_to_rent, copies_checked_out]

    return render_template("board_games-update.jinja", board_games=board_games)

@app.route('/delete_board_game/<int:bg_id>', methods=["POST", "GET"])
def delete_board_game(bg_id):
    query = "DELETE FROM board_games WHERE bg_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (bg_id,))
    mysql.connection.commit()
    return redirect("/board_games.html")

# Customers Table

@app.route('/customers.html', methods=["POST", "GET"])
def customers():
    if request.method == "POST":
        if request.form.get("add_customer"):
            # grab user form inputs
            customer_name = request.form["customer_name"]
            email = request.form["email"]
            total_quantity_of_bgs_checked_out = request.form["total_quantity_of_bgs_checked_out"]
            total_amount_spent = request.form["total_amount_spent"]

            query = "INSERT INTO customers (customer_name, email, total_quantity_of_bgs_checked_out, total_amount_spent) VALUES (%s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, email, total_quantity_of_bgs_checked_out, total_amount_spent))
            mysql.connection.commit()
        return redirect("/customers.html")

    query = 'SELECT customer_id AS "Customer ID", customer_name AS "Name", email AS "Email", total_quantity_of_bgs_checked_out AS "Games Checked Out", total_amount_spent AS "Total Amount Spent" FROM customers ORDER BY customer_id ASC;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    customers_results = cursor.fetchall()
    return render_template("customers.jinja", customers=customers_results)

@app.route('/customers-add.html', methods=["POST", "GET"])
def customers_add():
    return render_template("customers-add.jinja")

@app.route('/customers-update.html', methods=["POST", "GET"])
def customers_update():
    if request.method == "POST":
        if request.form.get("update_customer"):
            # Process the form submission for updating the customer
            customer_id = request.form["customer_id"]
            customer_name = request.form["customer_name"]
            email = request.form["email"]
            total_quantity_of_bgs_checked_out = request.form["total_quantity_of_bgs_checked_out"]
            total_amount_spent = request.form["total_amount_spent"]

            query = "UPDATE customers SET customer_name = %s, email = %s, total_quantity_of_bgs_checked_out = %s, total_amount_spent = %s WHERE customer_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, email, total_quantity_of_bgs_checked_out, total_amount_spent, customer_id))
            mysql.connection.commit()
            return redirect("/customers.html")

    customer_id = request.args.get("customer_id")  # Get the customer_id from the URL query parameters
    query = "SELECT * FROM customers WHERE customer_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (customer_id,))
    result = cur.fetchone()

    if result is None:
        # Handle the case when no record is found
        print("No record found for customer_id:", customer_id)
        return redirect("/customers.html")

    # Debugging statements
    print("Result:", result)

    customer_id = result['customer_id']
    customer_name = result['customer_name']
    email = result['email']
    total_quantity_of_bgs_checked_out = result['total_quantity_of_bgs_checked_out']
    total_amount_spent = result['total_amount_spent']

    customers = [customer_id, customer_name, email, total_quantity_of_bgs_checked_out, total_amount_spent]

    return render_template("customers-update.jinja", customers=customers)

@app.route('/delete_customer/<int:customer_id>', methods=["POST", "GET"])
def delete_customer(customer_id):
    query = "DELETE FROM customers WHERE customer_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (customer_id,))
    mysql.connection.commit()
    return redirect("/customers.html")

# Employees Table

@app.route('/employees.html', methods=["POST", "GET"])
def employees():
    if request.method == "POST":
        if request.form.get("add_employee"):
            # grab user form inputs
            employee_full_name = request.form["employee_full_name"]

            query = "INSERT INTO employees (employee_full_name) VALUES (%s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (employee_full_name,))
            mysql.connection.commit()
        return redirect("/employees.html")

    query = 'SELECT employee_id AS "Employee ID", employee_full_name AS "Employee Name" FROM employees ORDER BY employee_id ASC;'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employees_results = cursor.fetchall()
    return render_template("employees.jinja", employees=employees_results)

@app.route('/employees-add.html', methods=["POST", "GET"])
def employees_add():
    return render_template("employees-add.jinja")

@app.route('/employees-update.html', methods=["POST", "GET"])
def employees_update():
    if request.method == "POST":
        if request.form.get("update_employee"):
            # Process the form submission for updating the board game
            employee_id = request.form["employee_id"]
            employee_full_name = request.form["employee_full_name"]

            query = "UPDATE employees SET employee_full_name = %s WHERE employee_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (employee_full_name, employee_id))
            mysql.connection.commit()
            return redirect("/employees.html")

    employee_id = request.args.get("employee_id")  # Get the employee_id from the URL query parameters
    query = "SELECT * FROM employees WHERE employee_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (employee_id,))
    result = cur.fetchone()

    if result is None:
        # Handle the case when no record is found
        print("No record found for employee_id:", employee_id)
        return redirect("/employees.html")

    # Debugging statements
    print("Result:", result)

    employee_id = result['employee_id']
    employee_full_name = result['employee_full_name']

    employees = [employee_id, employee_full_name]

    return render_template("employees-update.jinja", employees=employees)

@app.route('/delete_employee/<int:employee_id>', methods=["POST", "GET"])
def delete_employee(employee_id):
    query = "DELETE FROM employees WHERE employee_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (employee_id,))
    mysql.connection.commit()
    return redirect("/employees.html")

# Invoices Table

@app.route('/invoices.html', methods=["GET", "POST"])
def invoices():
    if request.method == "POST":
        if request.form.get("add_invoice"):
            # Grab user form inputs
            customer_id = request.form["customer_id"]
            employee_id = request.form["employee_id"]
            date_checked_out = request.form["date_checked_out"]
            total_due = request.form["total_due"]

            # Perform the insert query
            if employee_id == "":
                query = "INSERT INTO invoices (customer_id, date_checked_out, total_due) VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_id, date_checked_out, total_due))
                mysql.connection.commit()
            else:
                query = "INSERT INTO invoices (customer_id, employee_id, date_checked_out, total_due) VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_id, employee_id, date_checked_out, total_due))
                mysql.connection.commit()
            return redirect("/invoice_details-add.html")

    if request.method == "GET":

        # Handle the GET request to fetch and display invoices
        query = '''
            SELECT 
            invoices.invoice_id AS "Invoice ID", 
            CONCAT(customers.customer_id, ' - ', customers.customer_name) AS "Customer ID - Name",
            IFNULL(employees.employee_id, "NULL") AS "Employee ID", date_checked_out AS "Date Checked Out", 
            total_due AS "Total Due" 
            FROM invoices 
            INNER JOIN customers ON customers.customer_id = invoices.customer_id 
            LEFT JOIN employees ON employees.employee_id = invoices.employee_id
            ORDER BY invoice_id ASC;
        '''
        cur = mysql.connection.cursor()
        cur.execute(query)
        invoices_results = cur.fetchall()

        return render_template("invoices.jinja", invoices=invoices_results)

@app.route('/invoices-add.html', methods=["POST", "GET"])
def invoices_add():

    customer_query = "SELECT customer_id, customer_name FROM customers;"
    cur = mysql.connection.cursor()
    cur.execute(customer_query)
    customers = cur.fetchall()

    employee_query = "SELECT employee_id, employee_full_name FROM employees;"
    cur = mysql.connection.cursor()
    cur.execute(employee_query)
    employees = cur.fetchall()
    return render_template("invoices-add.jinja", customers=customers, employees=employees)

@app.route('/invoices-update.html', methods=["POST", "GET"])
def invoices_update():
    if request.method == "POST":
        if request.form.get("update_invoice"):
            # Process the form submission for updating the invoice
            invoice_id = request.form["invoice_id"]
            customer_id = request.form["customer_id"]
            employee_id = request.form["employee_id"]
            date_checked_out = request.form["date_checked_out"]
            total_due = request.form["total_due"]

            # Check if employee_id is NULL
            if employee_id == "NULL":
                employee_id = None

            query = "UPDATE invoices SET customer_id = %s, employee_id = %s, date_checked_out = %s, total_due = %s WHERE invoice_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id, employee_id, date_checked_out, total_due, invoice_id))
            mysql.connection.commit()
            return redirect("/invoices.html")

    invoice_id = request.args.get("invoice_id")  # Get the invoice_id from the URL query parameters
    query = "SELECT * FROM invoices WHERE invoice_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoice_id,))
    result = cur.fetchone()

    if result is None:
        # Handle the case when no record is found
        print("No record found for invoice_id:", invoice_id)
        return redirect("/invoices.html")

    # Debugging statements
    print("Result:", result)

    invoice_id = result['invoice_id']
    customer_id = result['customer_id']
    employee_id = result['employee_id']
    date_checked_out = result['date_checked_out']
    total_due = result['total_due']

    query = "SELECT employee_id, employee_full_name FROM employees;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    employees = cur.fetchall()

    invoices = [invoice_id, customer_id, employee_id, date_checked_out, total_due]

    return render_template("invoices-update.jinja", invoices=invoices, employees=employees)

@app.route('/delete_invoices/<int:invoice_id>', methods=["POST", "GET"])
def delete_invoices(invoice_id):
    query = "DELETE FROM invoices WHERE invoice_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoice_id,)) 
    mysql.connection.commit()
    return redirect("/invoices.html")


# Invoice Details Table

@app.route('/invoice_details.html', methods=["POST", "GET"])
def invoice_details():
    if request.method == "POST":
        if request.form.get("add_invoice_details"):
            # grab user form inputs
            invoice_id = request.form["invoice_id"]
            bg_id = request.form["bg_id"]
            length_of_rental = request.form["length_of_rental"]
            daily_rental_rate = request.form["daily_rental_rate"]
            line_total = request.form["line_total"]

            query = "INSERT INTO invoice_details (invoice_id, bg_id, length_of_rental, daily_rental_rate, line_total) VALUES (%s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (invoice_id, bg_id, length_of_rental, daily_rental_rate, line_total))
            mysql.connection.commit()
            return redirect("/invoice_details.html")

    if request.method == "GET":
        query = '''
            SELECT
                invoice_details.invoice_details_id AS "Invoice Details ID",
                invoices.invoice_id AS "Invoice ID",
                CONCAT(board_games.bg_id, ' - ', board_games.bg_name) AS "Board Game ID - Name",
                length_of_rental AS "Length of Rental",
                board_games.daily_rental_rate AS "Daily Rental Rate",
                line_total AS "Line Total"
            FROM
                invoice_details
            INNER JOIN
                invoices ON invoices.invoice_id = invoice_details.invoice_id
            INNER JOIN
                board_games ON board_games.bg_id = invoice_details.bg_id
            ORDER BY 
                invoice_details_id ASC;            
        '''
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        return render_template("invoice_details.jinja", invoice_details=results)

@app.route('/invoice_details-add.html', methods=["POST", "GET"])
def invoice_details_add():
    invoice_query = "SELECT invoice_id FROM invoices ORDER BY invoice_id ASC;"
    cur = mysql.connection.cursor()
    cur.execute(invoice_query)
    invoices = cur.fetchall()

    bg_id_query = "SELECT bg_id FROM board_games ORDER BY bg_id ASC;"
    cur = mysql.connection.cursor()
    cur.execute(bg_id_query)
    board_games = cur.fetchall()

    return render_template("invoice_details-add.jinja", invoices=invoices, board_games=board_games)

@app.route('/get_daily_rental_rate')
def get_daily_rental_rate():
    bg_id = request.args.get('bg_id')
    query = "SELECT daily_rental_rate FROM board_games WHERE bg_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(query, (bg_id,))
    result = cur.fetchone()

    if result:
        daily_rental_rate = result['daily_rental_rate']
        return str(daily_rental_rate)
    else:
        return "0"  # or any other default value if no result is found

@app.route('/invoice_details-update.html', methods=["POST", "GET"])
def invoice_details_update():
    if request.method == "POST":
        if request.form.get("update_invoice_details"):
            # Process the form submission for updating the invoice
            invoice_details_id = request.form["invoice_details_id"]
            invoice_id = request.form["invoice_id"]
            bg_id = request.form["bg_id"]
            length_of_rental = request.form["length_of_rental"]
            daily_rental_rate = request.form["daily_rental_rate"]
            line_total = request.form["line_total"]

            query = "UPDATE invoice_details SET invoice_id = %s, bg_id = %s, length_of_rental = %s, daily_rental_rate = %s, line_total = %s WHERE invoice_details_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (invoice_id, bg_id, length_of_rental, daily_rental_rate, line_total, invoice_details_id))
            mysql.connection.commit()
            return redirect("/invoice_details.html")

    invoice_details_id = request.args.get("invoice_details_id")  # Get the invoice_details_id from the URL query parameters
    query = "SELECT * FROM invoice_details WHERE invoice_details_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoice_details_id,))
    result = cur.fetchone()

    if result is None:
        # Handle the case when no record is found
        print("No record found for invoice_details_id:", invoice_details_id)
        return redirect("/invoice_details.html")

    # Debugging statements
    print("Result:", result)

    invoice_details_id = result['invoice_details_id']
    invoice_id = result['invoice_id']
    bg_id = result['bg_id']
    length_of_rental = result['length_of_rental']
    daily_rental_rate = result['daily_rental_rate']
    line_total = result['line_total']

    invoice_details = [invoice_details_id, invoice_id, bg_id, length_of_rental, daily_rental_rate, line_total]

    return render_template("invoice_details-update.jinja", invoice_details=invoice_details)

@app.route('/delete_invoice_details/<int:invoice_details_id>', methods=["POST", "GET"])
def delete_invoice_details(invoice_details_id):
    query = "DELETE FROM invoice_details WHERE invoice_details_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoice_details_id,)) 
    mysql.connection.commit()
    return redirect("/invoice_details.html")

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    #Start the app on port 3000, it will be different once hosted
    app.run(port = port, debug=True)


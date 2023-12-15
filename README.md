# Board Game Rentals 

#### Project created by:

--Luis Sosa Lora
--Paola Cernada

## Project Overview

Our project aims to deliver a high-quality board game rental café application. The purpose of this document is to provide a comprehensive overview of the project, including the goals, specifications, and the changes made based on valuable feedback received.

## Project Goals

In this project, we aimed to achieve the following objectives:

1. Implement all the database-related skills learned in the CS340 and CS290 courses.
2. Transform an idea into a functional database.
3. Develop a web-based user interface (UI) that provides Create-Read-Update-Delete (CRUD) functionalities for the database.
4. Work in steps towards accomplishing a larger goal.

## Specifications

The Board Game Rentals Project adheres to the following specifications:

1. The database is pre-populated with sample data, with a minimum of three rows per table. The sample data effectively demonstrates the functionality of each table, including many-to-many relationships.
2. The database consists of at least four entities and four relationships, including one many-to-many relationship. These entities and relationships fulfill the operational requirements of the project.
3. The web interface is designed for administrators of the database, not customers. Therefore, there is no need for login pages, sessions, registration/password functionality, shopping cart, check-out, and similar features. The project solely focuses on providing a user interface for the tables.
4. Each entity implemented as a table in the database is represented by roughly one web app page in the front end user experience (UX). For many-to-many relationships between two tables, both tables are managed on a single web page.
5. Optionally, a home page can be added to the project, but it is not required.

## Executive Summary: 

### Project Feedback and Changes Made

Our project aimed to deliver a high-quality board game rental café application. Throughout the development process, we received valuable user feedback from testers that guided us in making significant changes. This is overview of the major changes made, primarily focusing on the database design process and implementation steps.

### Database Design Process

1. Removed the redundant intersection table ("customer_has_board_games").
2. Updated and improved the remaining intersection table ("invoice_details").
3. Merged the attributes of the "Customers Revenue" table into the "Customers" table for better data organization.

### Implementation Steps

1. Added nullable relationships for optional associations in the "Invoices" and "Employees" entities.
2. Implemented on cascade delete to maintain data integrity and remove associated invoices and invoice details when a customer is deleted.
3. Utilized join queries to combine data from different tables, resulting in improved query efficiency.

Additionally, we made a significant change in transitioning the project from Node.js to Flask. This decision was based on the challenges and limitations experienced with Node.js on the Flip server. Flask simplified the development process and provided a more straightforward and lightweight framework.

The feedback received during the project was instrumental in shaping its development. Suggestions from peer reviews led to significant changes, including the removal of redundant tables, updating and merging relevant information, implementing nullable relationships, and utilizing join queries. These changes enhanced functionality, improved data organization and integrity, and increased query efficiency. As a result, our project now stands poised to deliver a high-quality board game rental café application.

## Project Outline

### Problem

During the pandemic, when people were confined to their homes, the popularity of board games soared. Consequently, many board game cafés emerged. However, most of these small businesses lacked a proper Customer Relationship Management (CRM) system to effectively manage their rentals and inventory.

### Solution

Our database-driven website addresses the problem by recording rental orders of board games for café patrons. It allows café administrators to keep track of their board game inventory checked out by customers.

## Technologies Used

For the implementation of our project, we utilized the following technologies:

1. Flask: We chose Flask as our web framework for its simplicity, flexibility, and compatibility with Python. Flask allowed us to develop our web-based UI efficiently.

2. MySQL: We used MySQL as our relational database management system (RDBMS) to store and manage our project's data. MySQL provided robust data storage and retrieval capabilities.

3. phpMyAdmin: We utilized phpMyAdmin as a web-based tool for managing our MySQL database. It provided a user-friendly interface to interact with the database, allowing us to perform various administrative tasks.

4. SQL Workbench: SQL Workbench served as our integrated development environment (IDE) for writing and executing SQL queries. It provided a powerful interface for managing the database schema, executing queries, and analyzing the data.

5. Jinja2: Jinja2 is a templating engine used in Flask to generate dynamic HTML content. We leveraged Jinja2 to integrate Python code seamlessly into our HTML templates, enabling dynamic rendering of data on the web pages.

6. Bootstrap: We utilized Bootstrap, a popular CSS framework, to enhance the user interface of our web application. Bootstrap provided responsive design elements and pre-built components, ensuring a visually appealing and user-friendly experience.

## Deployment and Testing on Local Server

To deploy and test the project on a local server, follow these steps:

1. Install Python: Ensure that Python is installed on your system. You can download and install the latest version of Python from the official Python website (python.org).

2. Set Up a Virtual Environment: Create a virtual environment for your project to isolate its dependencies. Open your command-line interface, navigate to the project directory, and run the following command:
   ```
   python -m venv venv
   ```

3. Activate the Virtual Environment: Activate the virtual environment by running the appropriate command for your operating system:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install Dependencies: Install the required Python packages by executing the following command:
   ```
   pip install -r requirements.txt
   ```

5. Set Up the Database: Set up a MySQL database using phpMyAdmin or any other MySQL administration tool. Create a new database for the project and import the provided SQL file to initialize the tables and sample data.

6. Configure the Database Connection: In the project's configuration file (`config.py` or similar), modify the database connection settings to match your local MySQL configuration. Update the database host, username, password, and database name accordingly.

7. Run the Application: Start the Flask development server by running the following command in the project directory:
   ```
   flask run
   ```

8. Access the Application: Open a web browser and navigate to `http://localhost:5000` (or the URL provided by the Flask server). The application should now be running locally.

9. Test the Application: Use the web interface to interact with the database and test the CRUD functionalities. Create, read, update, and delete records to ensure that the application behaves as expected. Verify that the data is correctly stored and retrieved from the database.

By following these steps, you should be able to successfully deploy and test the project on your local server.

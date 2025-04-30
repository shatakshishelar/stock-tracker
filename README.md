# Stock Market Tracker – CS348 Project

This is a Django web application developed for the CS348 Database Systems course at Purdue University. It allows users to record stock purchases, update current stock prices, and generate reports showing portfolio performance.

## Project Overview

The application is designed to help a user manage a virtual portfolio of stocks. It supports basic operations such as adding purchases, updating prices, and reviewing performance in the form of gains or losses.

### Core Features

1. **Add Stock Purchases**  
   Users can enter the stock symbol, company name, quantity purchased, and purchase price.

2. **Update Current Prices**  
   Current prices can be updated for each stock. These are used to calculate gains or losses.

3. **Dashboard View**  
   The dashboard displays each purchase along with the current value, original cost, and net gain/loss.

4. **Report Generation**  
   A summary report shows the total quantity, average buy price, current price, and overall gain/loss for each stock.

## Database Design

The database consists of three main tables:

- `Stock`: Stores stock symbol and company name.
- `Purchase`: Records individual purchase transactions.
- `CurrentPrice`: Tracks the latest price for each stock.

Each purchase is linked to a stock using a foreign key. Current prices are updated and stored in a separate table for flexibility.

## Implementation Details

- The application is built using Django’s model-view-template (MVT) structure.
- Django ORM is used for form processing and simple queries.
- A raw SQL query is used to generate the portfolio report.
- Forms are dynamically populated from the database (e.g., dropdown to select a stock).

## Stage 3 Features and Justifications

The following additional features were implemented to meet Stage 3 requirements:

### 1. Indexes

Indexes were added to improve performance:
- `symbol` field in the `Stock` table (frequently searched)
- `stock_id` in the `Purchase` table (frequently joined)
- A composite index on (`stock`, `buy_price`) for report filtering

These indexes support queries on the dashboard and reports.

### 2. Two Access Methods

- **Django ORM** is used for inserting and updating data (e.g., purchases and prices).
- **Raw SQL** is used for the report generation in `portfolio_report`.

Each access method is used for different purposes to improve readability and performance.

### 3. Transactions

Django’s `transaction.atomic()` is used to ensure that data updates are done safely. If any part of a stock purchase or price update fails, the transaction is rolled back. This ensures database consistency.

### 4. Dynamic UI from Database

Dropdowns used in the forms (e.g., for selecting a stock) are populated dynamically from the database using ORM queries. No hardcoded values are used.

### 5. Concurrency and Isolation

Although SQLite does not support full isolation level control, Django’s transaction handling ensures atomicity. In a production environment, the same code could be deployed using PostgreSQL with proper isolation levels to avoid concurrency issues like race conditions.

### 6. Lessons Learned

During the development of this project, I learned how to:
- Use indexing effectively for query optimization
- Combine Django ORM with raw SQL for flexibility
- Use transactions to ensure data consistency
- Design clean database models and use them effectively with forms and views

## How to Run

1. Clone the repository  
2. Set up a Python virtual environment  
3. Install required packages using `pip install -r requirements.txt`  
4. Run `python manage.py migrate`  
5. Start the server using `python manage.py runserver`

## Author

Shatakshi Shelar  
Purdue University – CS348 Database Systems


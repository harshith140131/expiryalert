import sqlite3

# Function to create database table
def create_table():
    conn = sqlite3.connect('invoiceItems.db')  # Create a new connection within the function
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS invoice_items
                 (email TEXT, item TEXT, expiry_date TEXT,
                  PRIMARY KEY (email, item))''')  # Define email and item as the primary key
    conn.commit()
    conn.close()  # Close the connection after executing the query

# Function to insert data into the database
def insert_data(email, item, expiry_date):
    conn = sqlite3.connect('invoiceItems.db')  # Create a new connection within the function
    c = conn.cursor()
    c.execute("INSERT INTO invoice_items (email, item, expiry_date) VALUES (?, ?, ?)", (email, item, expiry_date))
    conn.commit()
    conn.close()  # Close the connection after executing the query

# Function to commit changes to the database
def commit():
    conn = sqlite3.connect('invoiceItems.db')  # Create a new connection within the function
    conn.commit()
    conn.close()  # Close the connection after committing

# Function to close the database connection
def close():
    conn = sqlite3.connect('invoiceItems.db')  # Create a new connection within the function
    conn.close()  # Close the connection

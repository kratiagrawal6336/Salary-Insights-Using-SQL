import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Connect to SQLite database 
conn = sqlite3.connect('test_data.db')
cursor = conn.cursor()



# Read data from Excel file
salary_excel_file_path = r'D:\SalaryData2.xlsx'
salary_data= pd.read_excel(salary_excel_file_path)

employee_excel_file_path = r'D:\EmployeeData.xlsx'
employee_data = pd.read_excel(employee_excel_file_path)

# Create EMPLOYEE table in SQLITE test_data.db database
cursor.execute('''
    CREATE TABLE Employee (
        employee_id INTEGER,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        Phone_Number TEXT,
        DEPARTMENT_ID TEXT
    )
''')

# Create Salary table in SQLITE test_data.db database
cursor.execute('''
    CREATE TABLE Salary (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        salary REAL,
        disbursement_date DATE,
        FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
    )
''')

# Insert data from the Excel file into Employee table
for index, row in employee_data.iterrows():
    
    cursor.execute('''
        INSERT INTO Employee (employee_id, first_name, last_name, email, Phone_Number, DEPARTMENT_ID)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['EMPLOYEE_ID'], row['FIRST_NAME'], row['LAST_NAME'], row['EMAIL'], row['PHONE_NUMBER'], row['DEPARTMENT_ID']))

# Insert data from the Excel file into Salary table
for index, row in salary_data.iterrows():
    # Convert Timestamp to string in the 'YYYY-MM-DD' format
    disbursement_date = row['disbursement_date'].strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO Salary (employee_id, salary, disbursement_date)
        VALUES (?, ?, ?)
    ''', (row['employee_id'], row['salary'], disbursement_date))

# Commit changes and close connection
conn.commit()
conn.close()

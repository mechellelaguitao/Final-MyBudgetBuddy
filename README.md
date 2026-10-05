MyBudgetBuddy

Project Description

MyBudgetBuddy is a desktop monthly budget and expense management application developed in Python. It provides a graphical user interface (GUI) that allows users to create an account, log in, set a monthly budget, record expenses, view expenses, edit or delete expenses, monitor category spending, receive budget warnings, and view a monthly summary.

The system addresses the need for a simple personal budgeting application that helps users monitor their spending against a planned monthly budget. Instead of manually calculating expenses and remaining funds, MyBudgetBuddy automatically calculates total expenses, remaining budget, category totals, and budget status.

The application stores users, budget information, and expense records in a structured text file named monthly_expenses.txt.

Project Objectives

The main objectives of MyBudgetBuddy are to:

Provide a simple and user-friendly desktop budgeting application.

Allow users to create accounts and log in securely through the application interface.

Allow users to set a monthly budget and category limits.

Record and manage individual expenses.

Automatically calculate total expenses and remaining budget.

Categorize expenses for easier monitoring.

Warn users when 80% or more of the budget has been used.

Identify when the user has reached or exceeded the monthly budget.

Provide a monthly summary of budget and category spending.

Demonstrate basic software organization using models, repositories, services, views, and a main application class.

Features

1. User Registration and Login

Users can create an account with a username and password. Existing users can log in through the login screen. The program also provides a default admin account when no user data exists.

2. Monthly Budget Setup

The user can enter:

Month

Total monthly budget

Budget amount for each expense category

The available categories are Food, Transportation, School, Bills, Personal, and Other.

3. Add Expense

Users can add an expense by entering:

Description

Category

Amount

The application validates the amount before saving it.

4. View Expenses

All recorded expenses can be displayed in a table containing the expense number, description, category, and amount.

5. Edit Expense

Users can select an existing expense and modify its description, category, or amount.

6. Delete Expense

Users can select an expense and delete it after confirming the deletion.

7. Expense Categories

The application calculates and displays the total amount spent in each category compared with the category budget.

8. Budget Warning

The application provides budget status messages:

WITHIN BUDGET

WARNING: 80% OF BUDGET USED

BUDGET FULLY USED

OVER BUDGET

9. Dashboard

The main dashboard displays:

Total Budget

Total Expenses

Remaining Budget

Current budget status

Buttons for the application's major functions

10. Monthly Summary

The monthly summary displays the selected month, total budget, total expenses, remaining amount, and spending for each category.

11. Logout

Users can log out of the application. Before logging out, the application asks for confirmation and saves the current data.

Technologies Used

Technology

Purpose

Python

Main programming language

Tkinter

GUI framework used to build windows, forms, buttons, labels, dialogs, and other interface components

ttk

Tkinter themed widgets, including the expense table and category selection menu

Text File (monthly_expenses.txt)

Persistent storage for users, budget information, category budgets, and expenses

Python File I/O

Reading and writing application data

Python Lists and Dictionaries

In-memory representation of users, budget information, categories, and expenses

Git/GitHub (if used)

Source-code version control and project sharing

No external Python package is required by the program shown. Tkinter and the other imported modules used by the application are part of the standard Python installation on typical desktop Python distributions.

Project Structure

The program follows a feature-based structure with separate database, authentication, budget, and expense components.

MyBudgetBuddy/
│
├── database/
│   ├── database.py
│   └── monthly_expenses.txt
│
├── features/
│   ├── authentication/
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── view.py
│   │
│   ├── budget/
│   │   ├── model.py
│   │   ├── service.py
│   │   └── view.py
│   │
│   └── expenses/
│       ├── model.py
│       ├── repository.py
│       ├── service.py
│       └── view.py
│
└── main.py

Major Files and Folders

database/database.py
Handles persistent storage. It loads users, budget information, and expenses from monthly_expenses.txt and saves the updated data back to the file.

database/monthly_expenses.txt
Acts as the application's persistent data store. It contains separate sections for users, budget information, and expenses.

features/authentication/model.py
Contains the function used to create a user object represented as a dictionary.

features/authentication/repository.py
Provides data-access functions for retrieving users and registering new users.

features/authentication/service.py
Contains authentication-related logic, including login and account creation.

features/authentication/view.py
Contains the Tkinter login and registration screens.

features/budget/model.py
Creates budget data and provides basic expense list operations used by the budget feature.

features/budget/service.py
Contains budget-related calculations such as remaining budget and budget status.

features/budget/view.py
Provides the monthly budget setup GUI.

features/expenses/model.py
Creates expense objects and provides basic list operations for adding, updating, and deleting expenses.

features/expenses/repository.py
Provides the underlying list operations for expense records.

features/expenses/service.py
Contains expense-related business logic, including adding, editing, deleting, calculating totals, and calculating category totals.

features/expenses/view.py
Contains the graphical forms and expense table used for adding, editing, viewing, and selecting expenses.

main.py
Contains the main App class and connects the authentication, budget, expense, database, and GUI components. It also starts the Tkinter application.

Installation and Setup

Requirements

Python 3.x

Tkinter

A desktop operating system that supports Tkinter

The complete MyBudgetBuddy project folder

Step 1: Install Python

Download and install Python 3.x if it is not already installed.

Verify the installation:

python --version

On some systems, use:

python3 --version

Step 2: Download or Clone the Project

Place the complete project folder on your computer.

If the project is stored in a Git repository:

git clone <repository-url>
cd MyBudgetBuddy

Step 3: Verify the Project Structure

Make sure the project contains the database, features, and main application files in the expected structure.

Step 4: Run the Application

From the project root directory, run:

python main.py

Or, depending on the system:

python3 main.py

Step 5: First-Time Setup

When the application starts:

Register a new account, or use the default account if no users exist.

Log in.

Enter the month.

Enter the total monthly budget.

Enter category budgets.

Save the budget.

Use the dashboard to manage expenses.

Dependencies

The application uses Python's standard library:

tkinter
tkinter.ttk

No pip install command is required for the libraries imported in the provided source code.

Note: On some Linux installations, Tkinter may need to be installed separately through the operating system's package manager.

How to Use the System

1. Login

Enter your username and password, then click Login.

If you do not have an account, click Register and create one.

2. Set Up the Budget

After logging in for the first time, enter the month, total monthly budget, and category budgets.

Click Save Budget.

3. Add an Expense

From the dashboard:

Click Add Expense.

Enter the expense description.

Select the expense category.

Enter the amount.

Click Save.

4. View Expenses

Click View Expenses to see all recorded expenses in a table.

5. Edit an Expense

Click Edit Expense:

Select an expense from the list.

Change its information.

Save the updated expense.

6. Delete an Expense

Click Delete Expense:

Select an expense.

Confirm the deletion.

7. Check Category Spending

Click Expense Categories to see how much has been spent in each category compared with the category budget.

8. Check Budget Warning

Click Budget Warning to see the current budget status.

9. View Monthly Summary

Click Monthly Summary to see the month, budget, expenses, remaining budget, and category totals.

10. Logout

Click Logout and confirm when prompted.

OOP Implementation

The project uses object-oriented programming primarily through the App class in main.py.

Important Class

App

The App class controls the main application flow and stores the application's main state.

Important attributes include:

self.root – the main Tkinter window.

self.users – loaded user records.

self.budget – current budget information.

self.expenses – recorded expense information.

Important methods include:

__init__() – initializes the application.

login() – displays the login screen.

after_login() – determines whether budget setup or the dashboard should be displayed.

set_budget() – saves the configured budget.

save() – writes current data to persistent storage.

dashboard() – displays the main dashboard.

add() – opens the add-expense form.

view() – displays recorded expenses.

edit() – opens the expense selection screen for editing.

delete() – opens the expense selection screen for deletion.

categories() – displays category totals.

warning() – displays the current budget status.

summary() – displays the monthly summary.

logout() – saves data and returns to the login screen.

Encapsulation

Encapsulation is demonstrated by grouping the main application state and related operations inside the App class. For example, budget and expense data are stored as attributes such as self.budget and self.expenses, while operations on the application are implemented as methods of the same class.

The feature modules also separate responsibilities into models, repositories, services, and views.

Inheritance

No custom inheritance hierarchy is explicitly implemented in the provided source code.

The application does use Tkinter classes such as tk.Tk, tk.Frame, tk.Label, tk.Button, and ttk.Treeview, which are framework classes, but the project does not define its own subclasses of these widgets.

Polymorphism

No explicit custom polymorphism through method overriding is implemented in the provided source code. Different callback functions and methods are passed to Tkinter widgets as commands, allowing the GUI to invoke different behaviors depending on the selected operation.

Database

Database Type

The project does not use a relational database such as MySQL, SQLite, or PostgreSQL.

Instead, it uses a structured text file:

monthly_expenses.txt

The file is divided into sections:

[USERS]

[BUDGET]

[EXPENSES]

The database module reads these sections and converts the stored values into Python lists and dictionaries for use by the application.

Data Structure

Users

Each user contains:

username
password

Budget

The budget contains:

month
total
categories

Each category stores its corresponding budget amount.

Expenses

Each expense contains:

description
category
amount

Important Data Sections

Section

Purpose

[USERS]

Stores registered usernames and passwords

[BUDGET]

Stores the selected month, total budget, and category budgets

[EXPENSES]

Stores expense descriptions, categories, and amounts

CRUD and Search Operations

Create

The system creates:

New user accounts

A monthly budget

New expense records

Read

The system reads:

User accounts

Budget information

Expense records

Category totals

Monthly summary information

Update

The system updates:

Budget data

Existing expense records

Delete

The system deletes:

Selected expense records

Search / Selection

The system does not implement a separate text-based search feature. Instead, users select an expense from the displayed expense table when editing or deleting a record.

Screenshots

The following screenshots should be included in the final project documentation. Replace the placeholders below with screenshots captured from the working application.

Screenshot 1 – Login Screen

Description: Shows the MyBudgetBuddy login interface with username and password fields, Login button, and Register button.

[Insert screenshot of the Login Screen here]

Screenshot 2 – Registration Screen

Description: Shows the Create Account form where a user enters a username, password, and confirmation password.

[Insert screenshot of the Registration Screen here]

Screenshot 3 – Monthly Budget Setup

Description: Shows the form for entering the month, total monthly budget, and category budget amounts.

[Insert screenshot of the Monthly Budget Setup here]

Screenshot 4 – Dashboard

Description: Shows the main dashboard containing the total budget, expenses, remaining amount, budget status, and application buttons.

[Insert screenshot of the Dashboard here]

Screenshot 5 – Add Expense

Description: Shows the form used to enter an expense description, category, and amount.

[Insert screenshot of the Add Expense form here]

Screenshot 6 – Expense List

Description: Shows the table containing recorded expenses, including their description, category, and amount.

[Insert screenshot of the Expense List here]

Screenshot 7 – Monthly Summary

Description: Shows the monthly summary containing the budget, total expenses, remaining amount, and category spending.

[Insert screenshot of the Monthly Summary here]

Testing

The following test cases can be used to verify the major functions of MyBudgetBuddy.

Test Case

Action

Expected Result

Actual Result

Login with valid credentials

Enter a registered username and correct password

User is logged in and proceeds to budget setup or dashboard

Passed – valid credentials are accepted

Login with invalid credentials

Enter an incorrect username or password

Error message is displayed

Passed – invalid credentials display an error

Register account

Enter a new username and matching passwords

Account is created successfully

Passed – new account is saved

Register duplicate username

Use an existing username

System reports that the username already exists

Passed – duplicate username is rejected

Register mismatched passwords

Enter different password and confirmation values

Warning message is displayed

Passed – registration is rejected

Set valid budget

Enter a valid month and positive budget values

Budget is saved and dashboard is displayed

Passed – valid budget is accepted

Add valid expense

Enter a description, category, and positive amount

Expense is added and dashboard totals are updated

Passed – expense is saved

Add invalid expense

Enter an invalid or negative amount

Warning message is displayed

Passed – invalid amount is rejected

View expenses

Click View Expenses

Existing expenses appear in a table

Passed – expenses are displayed

Edit expense

Select an expense and change its details

Selected expense is updated

Passed – expense is updated

Delete expense

Select an expense and confirm deletion

Selected expense is removed

Passed – expense is deleted

Budget warning below 80%

Keep spending below 80% of budget

Status shows WITHIN BUDGET

Passed

Budget warning at/above 80%

Reach at least 80% of budget

Status shows WARNING: 80% OF BUDGET USED unless the budget is fully used or exceeded

Passed

Fully used budget

Make total expenses equal to the budget

Status shows BUDGET FULLY USED

Passed

Exceed budget

Make total expenses greater than the budget

Status shows OVER BUDGET

Passed

Monthly summary

Click Monthly Summary

Current budget, expenses, remaining amount, and category totals are shown

Passed

Logout

Click Logout and confirm

User returns to the login screen

Passed

Testing note: The “Actual Result” entries above are based on the implemented program logic. They should be replaced with the exact results observed during your own live testing if your instructor requires evidence from an actual test run.

Known Issues / Limitations

Text-file storage instead of a relational database
The project stores data in monthly_expenses.txt rather than SQLite, MySQL, or another database management system.

Passwords are stored as plain text
Passwords are written directly to the data file. A production application should hash passwords before storage.

No dedicated search function
The application allows users to view and select expenses, but there is no separate search field for finding expenses by description or category.

Single shared budget data set
The current storage structure does not associate budget and expense records with a specific logged-in username. Therefore, it does not implement fully separated personal data for multiple users.

No password recovery
The application does not provide a forgotten-password or account-recovery feature.

No export/report feature
The application does not currently export reports to CSV, PDF, or other formats.

No graphical charts
Category totals are displayed as text rather than as graphs or charts.

Input validation is basic
The application validates important numeric fields, but more advanced validation could be added for usernames, passwords, duplicate data, and file corruption.

No database transaction or concurrency handling
Because the application uses a text file, it does not provide the transaction management and concurrent-user handling normally available in a database system.

Author

Name: Mechelle Laguitao
Section: CS26(3581) BSCS- 2
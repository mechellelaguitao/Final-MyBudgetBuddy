# MyBudgetBuddy

## Project Description

MyBudgetBuddy is a simple budgeting and expense tracking system that is made using Python and Tkinter.

The system helps users manage their monthly budget and keep track of their expenses. Users can set a budget, add expenses, edit or delete expenses, and see how much money they have spent and how much is remaining.

This system was created to help users easily monitor their spending and avoid going over their monthly budget.

## Project Objectives

The main objectives of MyBudgetBuddy are:

- To create a simple budgeting system.
- To help users track their expenses.
- To allow users to set a monthly budget.
- To show the total expenses and remaining budget.
- To provide a simple monthly summary.
- To practice Python and Object-Oriented Programming.

## Features

### Login and Registration

Users can create an account, login, and logout.

### Budget Period

Users can set their:

- Month
- Year
- Total monthly budget
- Budget for each category

### Add Expenses

Users can add multiple expenses by entering the description, category, and amount.

### View Expenses

Users can view all recorded expenses in a table.

### Edit Expense

Users can edit an existing expense.

### Delete Expense

Users can delete an expense after confirming the deletion.

### Dashboard

The dashboard shows:

- Total Budget
- Total Expenses
- Remaining Budget
- Budget Status

The budget status can be:

- Within Budget
- Over Budget

### Monthly Summary

The monthly summary shows:

- Month and Year
- Total Budget
- Total Expenses
- Remaining Budget
- Budget for each category
- Spending for each category
- Overall budget status

## Technologies Used

- **Programming Language:** Python
- **GUI:** Tkinter
- **Data Storage:** Text File
- **Other Libraries:** tkinter and tkinter.ttk

No third-party Python packages are required.

## Project Structure

```text
MyBudgetBuddy/
├── main.py
├── monthly_expenses.txt
├── database/
│   ├── __init__.py
│   └── database.py
└── features/
    ├── __init__.py
    ├── authentication/
    │   ├── __init__.py
    │   ├── model.py
    │   ├── repository.py
    │   ├── service.py
    │   └── view.py
    ├── budget/
    │   ├── __init__.py
    │   ├── model.py
    │   ├── service.py
    │   └── view.py
    ├── expenses/
    │   ├── __init__.py
    │   ├── model.py
    │   ├── repository.py
    │   ├── service.py
    │   └── view.py
    └── dashboard/
        ├── __init__.py
        └── view.py
```

### Main Files

- `main.py` - Starts the application.
- `monthly_expenses.txt` - Stores the users, budget, and expenses.
- `database/database.py` - Loads and saves the data.
- `authentication/` - Handles login and registration.
- `budget/` - Handles the budget information.
- `expenses/` - Handles adding, viewing, editing, and deleting expenses.
- `dashboard/` - Contains the main dashboard and monthly summary.

## Installation and Setup

### Requirements

- Python 3.x
- Tkinter

No additional packages are needed.

### Steps

1. Install Python on your computer.
2. Download or clone this project.
3. Open the project folder in the terminal.
4. Run:

```bash
python main.py
```

5. The MyBudgetBuddy login screen should appear.

## How to Use the System

1. Open the application.
2. Login using an existing account or create a new account.
3. Set the month, year, and monthly budget.
4. Enter the budget for each category.
5. Use the dashboard to view the current budget.
6. Select **Add Expenses** to record expenses.
7. Select **View Expenses** to see your expenses.
8. Select **Edit Expense** to change an expense.
9. Select **Delete Expense** to remove an expense.
10. Select **Monthly Summary** to see the budget and spending summary.
11. Select **Logout** when finished.

### Default Account

Username: `admin`  
Password: `admin123`

## OOP Implementation

The main class used in the system is `App`.

The `App` class stores the users, budget, expenses, and contains methods for the dashboard operations.

### Encapsulation

Related data and functions are grouped inside classes and modules.

### Inheritance

No custom inheritance is used in the project.

### Polymorphism

No major custom polymorphism is used in the project.

## Database

MyBudgetBuddy does not use a traditional database such as MySQL or SQLite.

Instead, the system uses a text file called:

```text
monthly_expenses.txt
```

The file contains the following sections:

```text
[USERS]
[BUDGET]
[EXPENSES]
```

### Data Stored

- **Users** - Stores usernames and passwords.
- **Budget** - Stores the current month, year, total budget, and category budgets.
- **Expenses** - Stores expense descriptions, categories, and amounts.

### CRUD Operations

The system supports:

- **Create** - Create accounts and add expenses.
- **Read** - View saved users, budget, and expenses.
- **Update** - Update the budget and edit expenses.
- **Delete** - Delete expenses.

The system does not have a separate search feature.

## Screenshots

Screenshots can be added here after taking screenshots of the system.

Example:

```markdown
![Login Screen](screenshots/login.png)

![Budget Period](screenshots/budget-period.png)

![Dashboard](screenshots/dashboard.png)

![Add Expenses](screenshots/add-expenses.png)

![View Expenses](screenshots/view-expenses.png)

![Monthly Summary](screenshots/monthly-summary.png)
```

## Testing

The following features were tested:

| Feature | Test | Expected Result | Actual Result |
|---|---|---|---|
| Login | Correct username and password | User can login | Passed |
| Login | Wrong username or password | Error message appears | Passed |
| Register | Create new account | Account is created | Passed |
| Budget | Enter valid budget | Budget is saved | Passed |
| Add Expense | Add an expense | Expense is added | Passed |
| View Expense | Open expense list | Expenses are displayed | Passed |
| Edit Expense | Edit an expense | Expense is updated | Passed |
| Delete Expense | Delete an expense | Expense is removed | Passed |
| Summary | Open monthly summary | Summary is displayed | Passed |

## Known Issues / Limitations

- Expenses are stored in one list.
- Changing the budget period does not create a separate expense list for each month.
- There is no monthly expense history.
- There is no separate search function.
- Passwords are stored in a text file and are not encrypted.
- The system does not use a traditional database.
- The system does not have charts or graphs.

## Author

**Name:** Mechelle Laguitao  
**Section:** CS26(3581) BSCS-2
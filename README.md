# Banking Automation Project Documentation


## Project Overview

The Banking Automation Project is a Python application built using the Tkinter library for the graphical user interface (GUI). It provides functionalities for user account management, including login, account creation, balance checking, deposits, withdrawals, transfers, and transaction history. The application features captcha verification for login, email notifications for account creation and password recovery, and a user-friendly interface with animated elements.

## Installation Instructions

1. Ensure you have Python installed on your system.
2. Install the required libraries:
   ```bash
   pip install tkinter pillow sqlite3 gmail tkintertable
   ```
3. Run the application:
   ```bash
   python banking_project.py
   ```

## Usage Instructions

- **User Roles**:
  - **Admin**: Can create, view, and block user accounts.
  - **User**: Can check balance, deposit, withdraw, transfer funds, and view transaction history.

## Code Structure

- **Classes and Functions**:
  - `SliderAnimation`: Handles the animation of a label on the GUI.
  - `main_screen()`: Displays the main login screen with user input fields.
  - `welcome_admin_screen()`: Admin interface for managing user accounts.
  - `welcome_user_screen()`: User interface for account management.
  - Functions for creating, viewing, blocking users, and handling transactions (deposit, withdraw, transfer).

## Database Schema

- The application uses SQLite for storing user data and transaction history. The database includes tables for users and transactions.

## Error Handling

- The application validates user input and displays appropriate error messages for invalid entries.

## Future Enhancements

- Potential improvements could include adding more user roles, enhancing security features, and implementing a more robust email notification system.

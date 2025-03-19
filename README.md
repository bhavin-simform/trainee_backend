# Todo App

This project consists of:  
1. **Trainee Backend** - Developed using **Python (Flask)**  

## Table of Contents
- [Project Information](#project-information)

### Tech Stack
- **Backend**: Python (Flask)
- **Database**: MySQL

---

## Note: Make sure you have Flask installed on the system. If not, then run `pip install flask` and configure the MySQL database according to your credentials.

## MySQL Database Setup

Before running the backend application, you need to configure the MySQL database.

### Steps:

1. **Create a Database**:
   - Open MySQL command line or use a MySQL GUI tool (e.g., MySQL Workbench).
   - Create a new database for the project:
     ```sql
     CREATE DATABASE todo_app;
     ```

2. **Create a User and Set Permissions** (Optional but recommended):
   - Create a MySQL user for the app:
     ```sql
     CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'your_password';
     ```
   - Grant necessary permissions to the database:
     ```sql
     GRANT ALL PRIVILEGES ON todo_app.* TO 'todo_user'@'localhost';
     ```

3. **Configure Database in the Backend**:
   - In the backend folder, create a `.env` file (if it doesn't already exist).
   - Inside the `.env` file, add the following database credentials:
     ```plaintext
     DB_HOST=localhost
     DB_PORT=3306
     DB_NAME=todo_app
     DB_USER=todo_user
     DB_PASSWORD=your_password
     ```

   Make sure to replace `your_password` with the actual password you've set for the MySQL user.

---


## Backend Setup 

1. go to the backend directory by run this command
   ```bash
   cd trainne_backend

2. Follow this steps:
   ```bash
   sudo apt-get install python3-pip
   pip install flask flask_cors mysql_connector dotenv

3. Install the packges using 
    ```bash
    python server.py

4. Backend application will start/run in this URL http://localhost:5000

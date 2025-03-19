from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Get the frontend's URL (allow dynamic port change)
frontend_url = os.getenv('FRONTEND_URL')

# CORS configuration: Allow the frontend URL to make requests to the backend
CORS(app, origins=frontend_url)  # To allow cross-origin requests from the frontend

# Database connection function using credentials from environment variables
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connection

# GET: Retrieve all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(todos)

@app.route('/api/todos/<int:id>', methods=['GET'])
def get_todo(id):
    try:
        # Create a database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute the query to fetch the todo item by id
        cursor.execute("SELECT * FROM todos WHERE id = %s", (id,))
        todo = cursor.fetchone()  # Fetch one todo item

        cursor.close()
        connection.close()

        # If the todo item doesn't exist, return a 404 error
        if not todo:
            return jsonify({"message": "Todo not found"}), 404

        # Return the found todo item
        return jsonify(todo)

    except Error as err:
        print(f"Error: {err}")
        return jsonify({"message": "Failed to fetch todo"}), 500
    
# POST: Add a new todo
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    task = data['task']
    done = data.get('done', False)
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todos (task, done) VALUES (%s, %s)", (task, done))
    connection.commit()
    
    # Fetch the inserted todo
    cursor.execute("SELECT * FROM todos WHERE id = LAST_INSERT_ID()")
    new_todo = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return jsonify(new_todo), 201

# PUT method
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    task = data.get("task")
    done = data.get("done")

    if not task:
        return jsonify({"message": "Task is required"}), 400  # Error if task is missing

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the todo exists before updating
    cursor.execute("SELECT * FROM todos WHERE id = %s", (id,))
    existing_todo = cursor.fetchone()

    if not existing_todo:
        cursor.close()
        connection.close()
        return jsonify({"message": "Todo not found"}), 404  # If todo doesn't exist, return 404

    # Proceed with the update if todo exists
    cursor.execute("UPDATE todos SET task = %s, done = %s WHERE id = %s", (task, done, id))
    connection.commit()

    # Fetch the updated todo
    cursor.execute("SELECT * FROM todos WHERE id = %s", (id,))
    updated_todo = cursor.fetchone()
    
    cursor.close()
    connection.close()

    print(f"Updated Todo: {updated_todo}")  # Debugging print statement

    return jsonify(updated_todo)  # Return the updated todo

# DELETE: Delete a todo
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Todo deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, jsonify, send_file
import pymysql.cursors

app = Flask(__name__)

# Connect to the database using Cloud SQL Proxy
def connect_to_database():
    # Check if running locally or on Google Cloud Platform
    if os.environ.get('GAE_INSTANCE'):
        # Running on Google Cloud Platform
        db_host = '/cloudsql/linear-elf-419922:us-central1:test'
    else:
        # Running locally
        db_host = '104.155.175.73'  # Cloud SQL instance IP address
    
    # Connection details
    db_user = 'root'
    db_password = 'root'  # No password
    db_name = 'test_db'
    
    # Create connection object
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # Return connection object
    return connection

# Route to fetch data from Cloud SQL
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Connect to the database
        connection = connect_to_database()
        
        # Execute SQL query
        with connection.cursor() as cursor:
            sql = "SELECT * FROM message"
            cursor.execute(sql)
            result = cursor.fetchall()
        
        # Close connection
        connection.close()

        # Return data as JSON
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve the HTML file
@app.route('/')
def serve_html():
    return send_file('testUI.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

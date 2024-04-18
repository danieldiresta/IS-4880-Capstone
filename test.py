import os
from flask import Flask, jsonify, send_file
import pymysql.cursors

app = Flask(__name__)

def connect_to_database():
    # Check if running locally or on Google Cloud Platform
    if os.environ.get('GAE_INSTANCE'):
        db_host = '/cloudsql/linear-elf-419922:us-central1:test'
    else:
        # Running locally
        db_host = '104.155.175.73'  # IP address for cloud SQL
    
    # Way to connect 
    db_user = 'root'
    db_password = 'root'  
    db_name = 'test_db'
    
    # Object for connection 
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    return connection

# Fetches data from cloud SQL 
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Connect to the database
        connection = connect_to_database()
        
        with connection.cursor() as cursor:
            sql = "SELECT * FROM message"
            cursor.execute(sql)
            result = cursor.fetchall()

        connection.close()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HTML route 
@app.route('/')
def serve_html():
    return send_file('testUI.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

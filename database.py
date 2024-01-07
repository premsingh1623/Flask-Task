import MySQLdb

def get_db():
    try:
        connection = MySQLdb.connect(
            host='mysql-db',
            user='admin',
            password='qwerty',
            db='task_manager',
            charset='utf8mb4'
        )
        return connection
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise

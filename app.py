from flask import Flask, jsonify, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from controller.user_controller import register_user, login_user, logout
from controller.task_controller import create_task, get_tasks, update_task, delete_task
from database import get_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prem@123'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

with get_db() as conn, conn.cursor() as cur:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')

with get_db() as conn, conn.cursor() as cur:
    cur.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')

@app.route('/verify', methods=['POST'])
@jwt_required()
def verify():
    user_id = get_jwt_identity()
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        user_data = cur.fetchone()

    if user_data:
        user_info = {'user_id': user_data[0], 'username': user_data[1]}
        return jsonify({'success': True, 'user_info': user_info}), 200
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/profile', methods=['GET'])
def home_page():
    return render_template('task.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    return register_user()

@app.route('/profile', methods=['POST'])
def login():
    return login_user()

@app.route('/logout', methods=['GET'])
@jwt_required()
def logout_route():
    return logout()

@app.route('/create_task', methods=['POST'])
@jwt_required()
def create_task_route():
    return create_task()

@app.route('/get_tasks', methods=['GET'])
@jwt_required()
def get_tasks_route():
    return get_tasks()

@app.route('/update_task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task_route(task_id):
    return update_task(task_id)

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task_route(task_id):
    return delete_task(task_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

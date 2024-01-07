from flask import jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db

def authenticate(username, password):
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE username=%s", (username,))
        user_data = cur.fetchone()

    if user_data and check_password_hash(user_data[2], password):
        return user_data

def identity(payload):
    user_id = payload['identity']
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        user_data = cur.fetchone()
    return user_data

def register_user():
    username, password = request.form.get('username'), request.form.get('password')

    if not username or not password:
        return render_template('register.html', error='Username and password are required')

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    with get_db() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

    return render_template('register.html', success='User created successfully, Login Now')

def login_user():
    username, password = request.json.get('username'), request.json.get('password')

    if not username or not password:
        return jsonify({'status': False, 'mssg': 'Username and password are required'})

    user = authenticate(username, password)

    if user:
        access_token = create_access_token(identity=user[0])
        return {'status': True, 'mssg': access_token}
    
    else:
        return {'status': False, 'mssg': 'Invalid Credentials. Please try again.'}

def logout():
    resp = redirect(url_for('home'))
    unset_jwt_cookies(resp)
    return resp, 200

from flask import jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db

def create_task():
    data = request.get_json()
    text = data.get('text')
    user_id = get_jwt_identity()
    if not text:
        return jsonify({'status': False, 'message': 'Text is required for a task'}), 400

    with get_db() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO task (text, user_id) VALUES (%s, %s)", (text, user_id))
        conn.commit()

    return jsonify({'status': True, 'message': 'Task created successfully'}), 201


def get_tasks():
    user_id = get_jwt_identity()
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM task WHERE user_id=%s", (user_id,))
        tasks = cur.fetchall()

    task_list = [{'id': task[0], 'text': task[1], 'timestamp': task[2]} for task in tasks]
    print(task_list)
    return jsonify({'status': True, 'message': task_list}), 201


def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.form  
    new_text = data.get('text')

    if not new_text:
        return jsonify({'success': False, 'message': 'Text is required for updating a task item'}), 400

    with get_db() as conn, conn.cursor() as cur:
        cur.execute("UPDATE task SET text=%s WHERE id=%s AND user_id=%s", (new_text, task_id, user_id))
        if cur.rowcount == 0:
            return jsonify({'success': False, 'message': 'Task item not found or does not belong to the authenticated user'}), 404
        conn.commit()

    return jsonify({'success': True, 'message': 'Task item updated successfully'}), 200

def delete_task(task_id):
    user_id = get_jwt_identity()

    with get_db() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM task WHERE id=%s AND user_id=%s", (task_id, user_id))
        if cur.rowcount == 0:
            return jsonify({'success': False, 'message': 'Task item not found or does not belong to the authenticated user'}), 404
        conn.commit()

    return jsonify({'success': True, 'message': 'Task item deleted successfully'}), 200
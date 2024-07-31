from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, BigInteger, String, Integer, insert, text
from sqlalchemy.orm import declarative_base, Session

# Flask app
app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL = "postgresql://user:pass@db:5432/todo"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid input"}), 400

    ids = request_data.get("ids")
    limit = request_data.get("limit", 10)
    offset = request_data.get("offset", 0)

    if not ids:
        return jsonify({"error": "IDs are required"}), 400

    # Handle the case where limit is 0 or negative
    if limit <= 0:
        limit = 10
    tasks = []
    query = text("""
        SELECT t.id, t.name, ts.name
        FROM tasks as t
        INNER JOIN task_status as ts ON ts.id = t.status_id
        WHERE t.id in :ids
        ORDER BY t.id ASC
        LIMIT :limit OFFSET :offset
    """)
    params = {'ids': tuple(ids), 'limit': limit, 'offset': offset}

    with engine.connect() as connection:
        results = connection.execute(query, params)
        for row in results:
            task = {
                'id': row[0],
                'name': row[1],
                'status': row[2]
            }
            tasks.append(task)
    connection.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['PUT'])
def update_task():
    request_data = request.get_json()

    if not isinstance(request_data, list):
        return jsonify({'error': 'Invalid data format, expected a list'}), 400
    response_data = []

    try:
        with engine.connect() as connection:
            for task in request_data:
                taskID = task.get('id')
                taskName = task.get('name')
                statusName = task.get('status_name')

                if not taskName or not statusName:
                    return jsonify({'error': 'Both name and status_name are required'}), 400

                ids = connection.execute(
                    text("SELECT id FROM task_status WHERE name = :name"),
                    {'name': statusName}
                ).first()

                if ids is None:
                    return jsonify({'error': 'Not Found status name'}), 400

                for id in ids:
                    connection.execute(
                        text("UPDATE tasks SET name = :name, status_id = :status_id WHERE id = :id"),
                        {'name': taskName, 'status_id': id, 'id': taskID}
                    )
                    connection.commit()
            return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['POST'])
def add_task():
    request_data = request.get_json()

    if not isinstance(request_data, list):
        return jsonify({'error': 'Invalid data format, expected a list'}), 400

    response_data = []

    try:
        with engine.connect() as connection:
            for task in request_data:
                taskName = task.get('name')
                statusName = task.get('status_name')

                if not taskName or not statusName:
                    return jsonify({'error': 'Both name and status_name are required'}), 400

                ids = connection.execute(
                    text("SELECT id FROM task_status WHERE name = :name"),
                    {'name': statusName}
                ).first()
                if ids is None:
                    return jsonify({'error': 'Not Found status name'}), 400
                for id in ids:
                    connection.execute(
                        text("INSERT INTO tasks (name, status_id) VALUES (:name, :status_id)"),
                        {'name': taskName, 'status_id': id}
                    )
                    connection.commit()
                    return jsonify({'id': id})
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tasks', methods=['DELETE'])
def delete_tasks():
    requestData  = request.get_json()
    if not isinstance(requestData, object):
        return jsonify({'error': 'Invalid data format, expected a list'}), 400
    try:
        with engine.connect() as connection:
            taskIDs  = requestData.get('ids')
            if not isinstance(taskIDs, list):
                return jsonify({'error': 'Invalid data format, expected a list'}), 400
            for taskID in taskIDs:
                connection.execute(
                        text("DELETE FROM tasks WHERE id = :id"),
                        {'id': taskID}
                    )
                connection.commit()
        return jsonify({'Message': 'OK'}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)

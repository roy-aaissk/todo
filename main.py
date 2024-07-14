from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, BigInteger, String, Integer, insert, text
from sqlalchemy.orm import declarative_base, Session

@dataclass
class Money:
    amount: int
    currency: str

    def __post_init__(self):
        if (self.amount is None or not self.amount) or (self.currency is None or not self.currency):
            raise ValueError("value is None or not value")

    def Add(self, arg: 'Money'):
        if self.currency != arg.currency:
            raise ValueError("different currencies")
        return Money(self.amount + arg.amount, self.currency)

money = Money(100, "JPY")
money1 = Money(1, 'JPY')
print(money.Add(money1))

# Flask app
app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL = "postgresql://user:pass@db:5432/todo"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(Integer, default=0)

# Create tables
Base.metadata.create_all(engine)

# Seed data
with Session(engine) as session:
    session.execute(
        insert(Task),
        [
            {"name": "task1", "status": 0},
            {"name": "task2", "status": 0}
        ],
    )
    session.execute(
        text("UPDATE tasks SET name = :name, status = :status WHERE id = :id").bindparams(name="task3", status=1, id=1)
    )
    session.commit()

with Session(engine) as session:
    session.execute(
        text("DELETE FROM tasks WHERE status = :status").bindparams(status=1)
    )
    session.commit()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with Session(engine) as session:
        tasks = session.query(Task).all()
        result = [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]
    return jsonify(result)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == id).first()
        if task:
            result = {"id": task.id, "name": task.name, "status": task.status}
            return jsonify(result)
        else:
            return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

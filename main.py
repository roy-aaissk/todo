from dataclasses import dataclass

@dataclass
class Money:
  amount: int
  currency: str
  
  def __post_init__(self):
    if (self.amount is None or not self.amount) or (self.currency is None or not self.currency):
      raise ValueError("value s None or not value")
  def Add(self, arg :'Money'):
    if self.currency != arg.currency:
      raise ValueError("different currencies")
    return Money(self.amount + arg.amount,  self.currency)

money = Money(100, "JPY")
money1 = Money(1, 'JPY')
print(money.Add(money1))

# api Server作成
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



from sqlalchemy import create_engine, Column, BigInteger, String, Integer

# データベースの接続文字列を設定します。例: SQLiteを使用する場合
DATABASE_URL = "postgresql://user:pass@db:5432/todo"

# エンジンを作成します
engine = create_engine(DATABASE_URL)

@app.route('/tasks', methods=['GET'])
def get_tasks():
  return jsonify({"message": "ok"})

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Taskテーブルのモデルを定義します
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(Integer, default=0)

# テーブルを作成します
Base.metadata.create_all(engine)
from sqlalchemy.orm import Session
from sqlalchemy import insert, text, bindparam
with Session(engine) as session:
  session.execute(
    insert(Task),
    [
      {"name":"task1","status":0},
      {"name":"task2","status":0}
    ],
  )
  session.execute(
    text("UPDATE tasks SET name = :name, status = :status WHERE id = :id").bindparams(name="task3", status= 1, id = 1)
  )
  session.commit()

with Session(engine) as session:
  session.execute(
    text("DELETE FROM  tasks WHERE status = :status").bindparams(status= 1)
  )
  session.commit()
  







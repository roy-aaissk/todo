from dataclasses import dataclass, field
from domain.task_id import TaskID
# import uuid


# frozen=True: オブジェクトを不変にする
# eq=True: __eq__ を自動実装する (デフォルトTrue)
@dataclass(frozen=True)
class Task:
  # id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
  id: TaskID
  title: str
  content: str
  
  def __post_init__(self):
    if self.title is None or not self.title:
      raise ValueError("title is None or not value ")
    if self.content is None or not self.content:
      raise ValueError("content is None or not value ")


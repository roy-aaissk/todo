from dataclasses import dataclass
from domain.task import Task

@dataclass(frozen=False)
class TaskService:
  def exists(self, task: Task) -> bool:
    # データストアに問い合わせて確認する。
    # repository層でやる役割な気がする。
    return True

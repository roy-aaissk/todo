from dataclasses import dataclass
from domain.task import Task
from service.task import TaskService

@dataclass
class TaskUseCase:
  TaskService: TaskService
  def CreateTask(self, task: Task) -> Task:
    userService = TaskService()
    if (userService.exists(task)) == False:
      raise ValueError("userSerive.exists")

    
    return task
    # ユーザー作成処理

from abc import ABC, abstractmethod
from domain.task import Task

class ITaskRepository(ABC):
  @abstractmethod
  def Save(task: Task):
    pass
  @abstractmethod
  def Find(task: Task):
    pass
  # NOTE: リポジトリの責務は、オブジェクトの永続化そのため何を持って重複とするかのルールはドメインで管理するべき内容そうすること重複のルールが変わってもリポジトリの動作が変わらないことを保証できる
  @abstractmethod
  def Exist(task: Task):
    pass
  
class TaskRepostiory(ITaskRepository):
  def Save(task: Task):
    return super().Save()
  def Find(task: Task):
    return super().Find()
  def Exist(task: Task):
    return super().Exist()


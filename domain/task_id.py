from dataclasses import dataclass, field
import uuid

@dataclass(frozen=True)
class TaskID:
  id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)

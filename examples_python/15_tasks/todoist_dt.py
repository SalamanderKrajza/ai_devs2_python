from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IDue:
    date: str
    timezone: str
    string: str
    lang: str
    is_recurring: bool
    datetime: str

@dataclass
class ITaskModify:
    id: Optional[str] = None
    content: Optional[str] = None
    due_string: Optional[str] = None
    is_completed: Optional[bool] = None

@dataclass
class ITaskClose:
    id: str

@dataclass
class ITask:
    id: str
    assigner_id: Optional[str]
    assignee_id: Optional[str]
    project_id: str
    section_id: Optional[str]
    parent_id: Optional[str]
    order: int
    content: str
    description: str
    is_completed: bool
    labels: List[str]
    priority: int
    comment_count: int
    creator_id: str
    created_at: str
    due: IDue
    url: str
    duration: Optional[str]

"""
Task Orchestrator for MAXX Project
Manages task execution, delegation, and tracking across AI agents.
"""

import os
import json
import time
import uuid
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from datetime import datetime
from loguru import logger

from .memory_client import AgentBrainClient
from .checkpoint_manager import CheckpointManager, CheckpointType, CheckpointResult


class TaskStatus(str, Enum):
    """Task status."""
    PLANNED = "planned"
    RESEARCH = "research"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    TESTING = "testing"
    DOCUMENTING = "documenting"
    COMPLETE = "complete"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """Task definition."""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PLANNED
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: str = ""  # Agent name: claude, codex, mesh, minimax, unity
    sprint: str = "001"
    percent_complete: int = 0
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    research_docs: List[str] = field(default_factory=list)
    test_results: Dict[str, Any] = field(default_factory=dict)
    documentation: List[str] = field(default_factory=list)
    pr_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(**data)


@dataclass
class Sprint:
    """Sprint definition."""
    id: str
    name: str
    goal: str = ""
    start_date: str = ""
    end_date: str = ""
    tasks: List[str] = field(default_factory=list)  # Task IDs
    status: str = "planned"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TaskOrchestrator:
    """Orchestrates tasks across AI agents."""
    
    def __init__(
        self,
        client: Optional[AgentBrainClient] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        tasks_file: str = "docs/planning/TASKS_INDEX.md"
    ):
        self.client = client or AgentBrainClient()
        self.checkpoint_manager = checkpoint_manager or CheckpointManager(self.client)
        self.tasks_file = Path(tasks_file)
        self.tasks: Dict[str, Task] = {}
        self.sprints: Dict[str, Sprint] = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from TASKS_INDEX.md (markdown table format)."""
        if not self.tasks_file.exists():
            logger.warning(f"Tasks file not found: {self.tasks_file}")
            return
        
        content = self.tasks_file.read_text()
        tasks = self._parse_markdown_table(content)
        for task in tasks:
            self.tasks[task.id] = task
        
        logger.info(f"Loaded {len(self.tasks)} tasks from {self.tasks_file}")
    
    def _parse_markdown_table(self, content: str) -> List[Task]:
        """Parse markdown table into Task objects."""
        tasks = []
        lines = content.split("\n")
        
        in_table = False
        headers = []
        
        for line in lines:
            if line.startswith("| ID | Task |"):
                in_table = True
                headers = [h.strip() for h in line.split("|")[1:-1]]
                continue
            
            if in_table and line.startswith("|---"):
                continue
            
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 9:
                    task = Task(
                        id=parts[0],
                        title=parts[1],
                        status=self._parse_status(parts[2]),
                        percent_complete=self._parse_percent(parts[3]),
                        assignee=parts[4],
                        # docs, tests, pr, notes from remaining columns
                    )
                    tasks.append(task)
            
            if in_table and not line.startswith("|") and not line.strip():
                in_table = False
        
        return tasks
    
    def _parse_status(self, status_str: str) -> TaskStatus:
        """Parse status emoji to enum."""
        status_map = {
            "✅": TaskStatus.COMPLETE,
            "🔄": TaskStatus.IN_PROGRESS,
            "⏳": TaskStatus.PLANNED,
            "❓": TaskStatus.BLOCKED,
            "🔬": TaskStatus.RESEARCH,
            "📝": TaskStatus.DOCUMENTING,
            "🧪": TaskStatus.TESTING,
            "🚀": TaskStatus.IN_REVIEW,
            "📋": TaskStatus.PLANNED,
        }
        for emoji, status in status_map.items():
            if emoji in status_str:
                return status
        return TaskStatus.PLANNED
    
    def _parse_percent(self, percent_str: str) -> int:
        """Parse percentage string to int."""
        try:
            return int(percent_str.replace("%", "").strip())
        except:
            return 0
    
    def _save_tasks(self):
        """Save tasks back to TASKS_INDEX.md."""
        # This would regenerate the markdown table
        # For now, we keep the file as source of truth and update via agent
        pass
    
    def create_task(
        self,
        task_id: str,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        assignee: str = "",
        sprint: str = "001",
        dependencies: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create a new task."""
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            sprint=sprint,
            dependencies=dependencies or [],
            tags=tags or [],
        )
        self.tasks[task_id] = task
        self._save_tasks()
        logger.info(f"Created task {task_id}: {title}")
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def update_task(
        self,
        task_id: str,
        status: Optional[TaskStatus] = None,
        percent_complete: Optional[int] = None,
        **kwargs
    ) -> Optional[Task]:
        """Update task fields."""
        task = self.tasks.get(task_id)
        if not task:
            logger.warning(f"Task not found: {task_id}")
            return None
        
        if status:
            task.status = status
            if status == TaskStatus.IN_PROGRESS and not task.started_at:
                task.started_at = datetime.now().isoformat()
            elif status == TaskStatus.COMPLETE and not task.completed_at:
                task.completed_at = datetime.now().isoformat()
        
        if percent_complete is not None:
            task.percent_complete = max(0, min(100, percent_complete))
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.now().isoformat()
        self._save_tasks()
        
        # Sync to Agent Brain
        self._sync_task_to_memory(task)
        
        return task
    
    def _sync_task_to_memory(self, task: Task):
        """Sync task to Agent Brain memory."""
        try:
            memory_key = f"task:{task.id}"
            self.client.write_memory(
                section="tasks",
                content=f"# Task {task.id}: {task.title}\n\n"
                        f"Status: {task.status.value}\n"
                        f"Progress: {task.percent_complete}%\n"
                        f"Assignee: {task.assignee}\n"
                        f"Updated: {task.updated_at}\n"
            )
        except Exception as e:
            logger.warning(f"Failed to sync task to memory: {e}")
    
    def start_task(self, task_id: str, assignee: str = "") -> Optional[Task]:
        """Start working on a task."""
        task = self.update_task(
            task_id,
            status=TaskStatus.IN_PROGRESS,
            percent_complete=10,
        )
        if task and assignee:
            task.assignee = assignee
            self._save_tasks()
        
        # Notify Agent Brain
        self.client.send_message(
            to_session="broadcast",
            subject=f"Task Started: {task_id}",
            body=f"Agent {assignee} started task {task_id}: {task.title}"
        )
        
        return task
    
    def complete_task(
        self,
        task_id: str,
        test_results: Optional[Dict[str, Any]] = None,
        documentation: Optional[List[str]] = None,
        pr_url: Optional[str] = None,
        require_checkpoint: bool = True
    ) -> Optional[Task]:
        """Complete a task with optional checkpoint."""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # Update task
        task = self.update_task(
            task_id,
            status=TaskStatus.COMPLETE,
            percent_complete=100,
            test_results=test_results or {},
            documentation=documentation or [],
            pr_url=pr_url,
        )
        
        # Require checkpoint for completion
        if require_checkpoint:
            result = self.checkpoint_manager.task_complete_checkpoint(
                f"{task.id}: {task.title}",
                next_steps=["Continue with next task", "Review completed work", "End session"]
            )
            task.metadata["checkpoint_result"] = {
                "status": result.status.value,
                "response": result.response,
                "selected_option": result.selected_option,
            }
            self.checkpoint_manager.log_checkpoint(result)
        
        # Notify completion
        self.client.send_message(
            to_session="broadcast",
            subject=f"Task Completed: {task_id}",
            body=f"Task {task_id} completed: {task.title}"
        )
        
        return task
    
    def block_task(self, task_id: str, reason: str) -> Optional[Task]:
        """Mark task as blocked."""
        return self.update_task(
            task_id,
            status=TaskStatus.BLOCKED,
            metadata={"blocked_reason": reason, "blocked_at": datetime.now().isoformat()}
        )
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with given status."""
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_tasks_by_assignee(self, assignee: str) -> List[Task]:
        """Get all tasks assigned to an agent."""
        return [t for t in self.tasks.values() if t.assignee == assignee]
    
    def get_tasks_by_sprint(self, sprint: str) -> List[Task]:
        """Get all tasks in a sprint."""
        return [t for t in self.tasks.values() if t.sprint == sprint]
    
    def get_next_task(self, assignee: str) -> Optional[Task]:
        """Get next available task for an assignee."""
        # Find planned tasks with no unmet dependencies
        candidates = [
            t for t in self.tasks.values()
            if t.assignee == assignee
            and t.status == TaskStatus.PLANNED
            and all(self.tasks.get(dep, Task(id=dep, title="", status=TaskStatus.COMPLETE)).status == TaskStatus.COMPLETE
                    for dep in t.dependencies)
        ]
        
        if not candidates:
            return None
        
        # Sort by priority
        priority_order = {TaskPriority.CRITICAL: 0, TaskPriority.HIGH: 1, TaskPriority.MEDIUM: 2, TaskPriority.LOW: 3}
        candidates.sort(key=lambda t: priority_order.get(t.priority, 99))
        
        return candidates[0]
    
    def generate_task_report(self) -> str:
        """Generate a markdown report of all tasks."""
        lines = [
            "# Task Report",
            f"Generated: {datetime.now().isoformat()}",
            f"Total Tasks: {len(self.tasks)}",
            "",
        ]
        
        for status in TaskStatus:
            tasks = self.get_tasks_by_status(status)
            if tasks:
                lines.append(f"## {status.value.replace('_', ' ').title()} ({len(tasks)})")
                for task in tasks:
                    lines.append(f"- **{task.id}**: {task.title} ({task.percent_complete}%) - {task.assignee}")
                lines.append("")
        
        return "\n".join(lines)
    
    def export_tasks_json(self, filepath: str):
        """Export tasks to JSON."""
        data = {
            "tasks": {tid: task.to_dict() for tid, task in self.tasks.items()},
            "exported_at": datetime.now().isoformat(),
        }
        Path(filepath).write_text(json.dumps(data, indent=2))
    
    def close(self):
        """Close connections."""
        if self.client:
            self.client.close()


# Task decorators for easy task management
def task(
    task_id: str,
    title: str,
    priority: TaskPriority = TaskPriority.MEDIUM,
    assignee: str = "",
    sprint: str = "001",
    dependencies: Optional[List[str]] = None
):
    """Decorator to register a task function."""
    def decorator(func: Callable):
        orchestrator = TaskOrchestrator()
        orchestrator.create_task(
            task_id=task_id,
            title=title,
            priority=priority,
            assignee=assignee,
            sprint=sprint,
            dependencies=dependencies,
        )
        
        def wrapper(*args, **kwargs):
            orchestrator.start_task(task_id, assignee)
            try:
                result = func(*args, **kwargs)
                orchestrator.complete_task(task_id)
                return result
            except Exception as e:
                orchestrator.block_task(task_id, str(e))
                raise
            finally:
                orchestrator.close()
        
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test
    orchestrator = TaskOrchestrator()
    print(f"Loaded {len(orchestrator.tasks)} tasks")
    print(orchestrator.generate_task_report())
    orchestrator.close()
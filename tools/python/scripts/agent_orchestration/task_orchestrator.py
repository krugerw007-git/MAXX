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
        
        for line in lines:
            if line.startswith("| ID | Task |"):
                in_table = True
                continue
            
            if in_table and line.startswith("|---"):
                continue
            
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 9:
                    task = self._parse_task_row(parts)
                    if task:
                        tasks.append(task)
                continue
            
            if in_table and not line.startswith("|"):
                # End of table
                in_table = False
        
        return tasks
    
    def _parse_task_row(self, parts: List[str]) -> Optional[Task]:
        """Parse a single task row."""
        try:
            task_id = parts[0]
            title = parts[1]
            status_str = parts[2]
            percent_str = parts[3].replace("%", "")
            assignee = parts[4]
            docs_str = parts[5]
            tests_str = parts[6]
            pr_str = parts[7]
            notes = parts[8] if len(parts) > 8 else ""
            
            # Parse status
            status_map = {
                "✅": TaskStatus.COMPLETE,
                "🔄": TaskStatus.IN_PROGRESS,
                "📋": TaskStatus.PLANNED,
                "❓": TaskStatus.BLOCKED,
                "🔬": TaskStatus.RESEARCH,
                "📝": TaskStatus.DOCUMENTING,
                "🧪": TaskStatus.TESTING,
            }
            status = TaskStatus.PLANNED
            for emoji, s in status_map.items():
                if emoji in status_str:
                    status = s
                    break
            
            # Parse percent
            try:
                percent = int(percent_str)
            except ValueError:
                percent = 0
            
            return Task(
                id=task_id,
                title=title,
                status=status,
                percent_complete=percent,
                assignee=assignee.lower(),
                metadata={"notes": notes, "docs": docs_str, "tests": tests_str, "pr": pr_str},
            )
        except Exception as e:
            logger.warning(f"Failed to parse task row: {e}")
            return None
    
    def _save_tasks(self):
        """Save tasks back to markdown table."""
        # Read existing content to preserve structure
        content = self.tasks_file.read_text()
        
        # Generate new table
        table_lines = self._generate_markdown_table()
        
        # Replace table in content
        lines = content.split("\n")
        new_lines = []
        in_table = False
        table_replaced = False
        
        for line in lines:
            if line.startswith("| ID | Task |"):
                in_table = True
                if not table_replaced:
                    new_lines.extend(table_lines)
                    table_replaced = True
                continue
            
            if in_table:
                if line.startswith("|---"):
                    continue
                elif line.startswith("|"):
                    continue
                else:
                    in_table = False
                    new_lines.append(line)
                    continue
            
            new_lines.append(line)
        
        if not table_replaced:
            # No existing table, append at end
            new_lines.extend(table_lines)
        
        self.tasks_file.write_text("\n".join(new_lines))
        logger.info(f"Saved {len(self.tasks)} tasks to {self.tasks_file}")
    
    def _generate_markdown_table(self) -> List[str]:
        """Generate markdown table from tasks."""
        lines = [
            "| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |",
            "|----|------|--------|---|----------|------|-------|----|-------|",
        ]
        
        # Sort by sprint then ID
        sorted_tasks = sorted(self.tasks.values(), key=lambda t: (t.sprint, t.id))
        
        for task in sorted_tasks:
            status_emoji = self._status_emoji(task.status)
            docs = "✅" if task.documentation else ("📝" if task.status == TaskStatus.DOCUMENTING else "⏳")
            tests = "✅" if task.test_results else ("🧪" if task.status == TaskStatus.TESTING else "⏳")
            pr = task.pr_url or "⏳"
            notes = task.metadata.get("notes", "")
            
            lines.append(
                f"| {task.id} | {task.title} | {status_emoji} | {task.percent_complete}% | "
                f"{task.assignee} | {docs} | {tests} | {pr} | {notes} |"
            )
        
        return lines
    
    def _status_emoji(self, status: TaskStatus) -> str:
        """Get emoji for status."""
        emoji_map = {
            TaskStatus.PLANNED: "📋",
            TaskStatus.RESEARCH: "🔬",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.IN_REVIEW: "👀",
            TaskStatus.TESTING: "🧪",
            TaskStatus.DOCUMENTING: "📝",
            TaskStatus.COMPLETE: "✅",
            TaskStatus.BLOCKED: "❌",
            TaskStatus.CANCELLED: "⏭️",
        }
        return emoji_map.get(status, "📋")
    
    # ========================================
    # TASK MANAGEMENT
    # ========================================
    
    def create_task(
        self,
        task_id: str,
        title: str,
        description: str = "",
        assignee: str = "",
        sprint: str = "001",
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> Task:
        """Create a new task."""
        if task_id in self.tasks:
            raise ValueError(f"Task {task_id} already exists")
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            assignee=assignee.lower(),
            sprint=sprint,
            priority=priority,
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
        **kwargs
    ) -> Optional[Task]:
        """Update task fields."""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.now().isoformat()
        
        if "status" in kwargs:
            new_status = kwargs["status"]
            if new_status == TaskStatus.IN_PROGRESS and not task.started_at:
                task.started_at = datetime.now().isoformat()
            elif new_status == TaskStatus.COMPLETE and not task.completed_at:
                task.completed_at = datetime.now().isoformat()
                task.percent_complete = 100
        
        self._save_tasks()
        return task
    
    def start_task(self, task_id: str, assignee: str = "") -> bool:
        """Mark task as in progress."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        # Check dependencies
        for dep_id in task.dependencies:
            dep = self.tasks.get(dep_id)
            if dep and dep.status != TaskStatus.COMPLETE:
                logger.warning(f"Task {task_id} blocked by dependency {dep_id}")
                self.update_task(task_id, status=TaskStatus.BLOCKED)
                return False
        
        if assignee:
            task.assignee = assignee.lower()
        
        self.update_task(task_id, status=TaskStatus.IN_PROGRESS)
        logger.info(f"Started task {task_id}")
        return True
    
    def complete_task(
        self,
        task_id: str,
        test_results: Optional[Dict[str, Any]] = None,
        documentation: Optional[List[str]] = None,
        pr_url: Optional[str] = None,
    ) -> bool:
        """Mark task as complete with validation."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        # Validate completion criteria
        if not test_results and task.status != TaskStatus.TESTING:
            logger.warning(f"Task {task_id} completed without test results")
        
        updates = {"status": TaskStatus.COMPLETE, "percent_complete": 100}
        if test_results:
            updates["test_results"] = test_results
        if documentation:
            updates["documentation"] = documentation
        if pr_url:
            updates["pr_url"] = pr_url
        
        self.update_task(task_id, **updates)
        
        # Checkpoint for task completion
        result = self.checkpoint_manager.task_complete_checkpoint(
            f"Task {task_id} complete: {task.title}",
            next_steps=self._get_next_tasks(task)
        )
        
        logger.info(f"Completed task {task_id}: {result.status.value}")
        return True
    
    def _get_next_tasks(self, current_task: Task) -> List[str]:
        """Get suggested next tasks."""
        next_tasks = []
        for task in self.tasks.values():
            if (task.status == TaskStatus.PLANNED and 
                current_task.id in task.dependencies):
                next_tasks.append(f"Start {task.id}: {task.title}")
            elif task.status == TaskStatus.PLANNED and not task.dependencies:
                next_tasks.append(f"Start {task.id}: {task.title}")
        return next_tasks[:3]
    
    # ========================================
    # SPRINT MANAGEMENT
    # ========================================
    
    def create_sprint(
        self,
        sprint_id: str,
        name: str,
        goal: str = "",
        start_date: str = "",
        end_date: str = "",
        task_ids: Optional[List[str]] = None,
    ) -> Sprint:
        """Create a new sprint."""
        sprint = Sprint(
            id=sprint_id,
            name=name,
            goal=goal,
            start_date=start_date or datetime.now().strftime("%Y-%m-%d"),
            end_date=end_date,
            tasks=task_ids or [],
        )
        self.sprints[sprint_id] = sprint
        return sprint
    
    def get_sprint_tasks(self, sprint_id: str) -> List[Task]:
        """Get all tasks for a sprint."""
        sprint = self.sprints.get(sprint_id)
        if not sprint:
            # Find tasks with matching sprint field
            return [t for t in self.tasks.values() if t.sprint == sprint_id]
        return [self.tasks[tid] for tid in sprint.tasks if tid in self.tasks]
    
    def get_sprint_progress(self, sprint_id: str) -> Dict[str, Any]:
        """Get sprint progress summary."""
        tasks = self.get_sprint_tasks(sprint_id)
        if not tasks:
            return {"total": 0, "complete": 0, "in_progress": 0, "blocked": 0, "percent": 0}
        
        total = len(tasks)
        complete = sum(1 for t in tasks if t.status == TaskStatus.COMPLETE)
        in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        blocked = sum(1 for t in tasks if t.status == TaskStatus.BLOCKED)
        percent = int((complete / total) * 100) if total > 0 else 0
        
        return {
            "sprint_id": sprint_id,
            "total": total,
            "complete": complete,
            "in_progress": in_progress,
            "blocked": blocked,
            "planned": sum(1 for t in tasks if t.status == TaskStatus.PLANNED),
            "research": sum(1 for t in tasks if t.status == TaskStatus.RESEARCH),
            "percent": percent,
        }
    
    # ========================================
    # AGENT DELEGATION
    # ========================================
    
    def delegate_task(
        self,
        task_id: str,
        agent: str,  # claude, codex, mesh, minimax, unity
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Delegate task to an agent via Agent Brain mailbox."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        # Update assignee
        task.assignee = agent.lower()
        self._save_tasks()
        
        # Send mailbox message
        self.client.send_message(
            to_session=agent.lower(),
            subject=f"Task Assignment: {task_id} - {task.title}",
            body=json.dumps({
                "task_id": task_id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "dependencies": task.dependencies,
                "context": context or {},
                "assigned_at": datetime.now().isoformat(),
            }, indent=2),
        )
        
        logger.info(f"Delegated task {task_id} to {agent}")
        return True
    
    def get_agent_workload(self, agent: str) -> List[Task]:
        """Get tasks assigned to an agent."""
        return [t for t in self.tasks.values() if t.assignee == agent.lower()]
    
    # ========================================
    # RESEARCH TRACKING
    # ========================================
    
    def start_research(self, task_id: str, research_topic: str) -> bool:
        """Mark task as in research phase."""
        return self.update_task(task_id, status=TaskStatus.RESEARCH) is not None
    
    def add_research_doc(self, task_id: str, doc_path: str) -> bool:
        """Add research document to task."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        if doc_path not in task.research_docs:
            task.research_docs.append(doc_path)
            task.updated_at = datetime.now().isoformat()
            self._save_tasks()
        return True
    
    def complete_research(self, task_id: str, findings: str) -> bool:
        """Complete research phase."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.metadata["research_findings"] = findings
        return self.update_task(task_id, status=TaskStatus.IN_PROGRESS) is not None
    
    # ========================================
    # QUERY & REPORTING
    # ========================================
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with given status."""
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_tasks_by_assignee(self, assignee: str) -> List[Task]:
        """Get all tasks assigned to agent."""
        return [t for t in self.tasks.values() if t.assignee == assignee.lower()]
    
    def get_tasks_by_sprint(self, sprint: str) -> List[Task]:
        """Get all tasks in a sprint."""
        return [t for t in self.tasks.values() if t.sprint == sprint]
    
    def get_blocked_tasks(self) -> List[Task]:
        """Get all blocked tasks."""
        return self.get_tasks_by_status(TaskStatus.BLOCKED)
    
    def get_overdue_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks not updated in N days."""
        cutoff = datetime.now().timestamp() - (days * 86400)
        overdue = []
        for task in self.tasks.values():
            if task.status in (TaskStatus.IN_PROGRESS, TaskStatus.IN_REVIEW, TaskStatus.TESTING):
                updated = datetime.fromisoformat(task.updated_at).timestamp()
                if updated < cutoff:
                    overdue.append(task)
        return overdue
    
    def generate_report(self) -> str:
        """Generate project status report."""
        report = [
            "# MAXX Project Status Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Summary",
            f"- Total Tasks: {len(self.tasks)}",
            f"- Complete: {len(self.get_tasks_by_status(TaskStatus.COMPLETE))}",
            f"- In Progress: {len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))}",
            f"- Blocked: {len(self.get_tasks_by_status(TaskStatus.BLOCKED))}",
            f"- Planned: {len(self.get_tasks_by_status(TaskStatus.PLANNED))}",
            "",
            "## By Sprint",
        ]
        
        for sprint_id in sorted(set(t.sprint for t in self.tasks.values())):
            progress = self.get_sprint_progress(sprint_id)
            report.append(f"### Sprint {sprint_id}")
            report.append(f"- Progress: {progress['percent']}%")
            report.append(f"- Complete: {progress['complete']}/{progress['total']}")
            report.append("")
        
        report.append("## By Agent")
        for agent in ["claude", "codex", "mesh", "minimax", "unity"]:
            tasks = self.get_tasks_by_assignee(agent)
            if tasks:
                complete = sum(1 for t in tasks if t.status == TaskStatus.COMPLETE)
                report.append(f"- {agent.capitalize()}: {complete}/{len(tasks)} complete")
        
        report.append("")
        report.append("## Blocked Tasks")
        for task in self.get_blocked_tasks():
            report.append(f"- {task.id}: {task.title} (depends on: {', '.join(task.dependencies)})")
        
        return "\n".join(report)
    
    def close(self):
        """Close connections."""
        if self.client:
            self.client.close()


if __name__ == "__main__":
    orchestrator = TaskOrchestrator()
    print(orchestrator.generate_report())
    orchestrator.close()
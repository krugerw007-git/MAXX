"""
Checkpoint Manager for MAXX Project
Handles mandatory checkpoints via Agent Brain for human-in-the-loop decisions.
"""

import os
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path
from loguru import logger


class CheckpointStatus(Enum):
    PENDING = "pending"
    RESPONDED = "responded"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"


@dataclass
class CheckpointResult:
    """Result of a checkpoint interaction."""
    status: CheckpointStatus
    question: str
    options: List[str]
    response: Optional[str] = None
    selected_option: Optional[int] = None
    session_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class CheckpointManager:
    """Manages checkpoints for human-in-the-loop decision making."""
    
    def __init__(
        self,
        agent_brain_client=None,
        project_key: Optional[str] = None,
        checkpoint_log_path: Optional[str] = None,
        default_timeout: int = 86400,  # 24 hours
    ):
        self.client = agent_brain_client
        self.project_key = project_key or os.getenv("AGENT_BRAIN_PROJECT_KEY", "")
        self.checkpoint_log_path = checkpoint_log_path or os.getenv(
            "CHECKPOINT_LOG_PATH",
            "docs/runtime/CHECKPOINTS_LOG.md"
        )
        self.default_timeout = default_timeout
        self.checkpoints_history: List[CheckpointResult] = []
        
        # Load existing history
        self._load_history()
    
    def _load_history(self):
        """Load checkpoint history from log file."""
        log_file = Path(self.checkpoint_log_path)
        if log_file.exists():
            # Parse markdown log - simplified for now
            logger.info(f"Loaded checkpoint history from {log_file}")
    
    def _log_checkpoint(self, result: CheckpointResult):
        """Log checkpoint to file and history."""
        self.checkpoints_history.append(result)
        
        # Append to markdown log
        log_entry = f"""## Checkpoint: {result.timestamp}

**Question**: {result.question}

**Options**: {", ".join(f"{i+1}. {opt}" for i, opt in enumerate(result.options))}

**Status**: {result.status.value}

**Response**: {result.response or "N/A"}

**Selected**: {result.selected_option + 1 if result.selected_option is not None else "N/A"} ({result.options[result.selected_option] if result.selected_option is not None else "N/A"})

**Duration**: {result.duration_seconds:.1f}s

---
"""
        
        log_file = Path(self.checkpoint_log_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a") as f:
            f.write(log_entry)
        
        logger.info(f"Checkpoint logged: {result.question[:50]}...")
    
    def create_checkpoint(
        self,
        question: str,
        options: List[str],
        timeout: Optional[int] = None,
        session_id: Optional[str] = None,
        context: Optional[str] = None,
        require_response: bool = True,
    ) -> CheckpointResult:
        """
        Create a checkpoint and wait for human response.
        
        This uses Agent Brain's checkpoint API which blocks until response or timeout.
        """
        import time
        start_time = time.time()
        
        if not self.client:
            # Fallback: prompt locally (for development)
            logger.warning("No Agent Brain client - using local prompt fallback")
            return self._local_prompt(question, options, timeout or self.default_timeout)
        
        try:
            # Use Agent Brain checkpoint API (MCP tool for Claude Code, curl for Codex)
            if hasattr(self.client, 'agent_brain_checkpoint'):
                # MCP tool available
                response = self.client.agent_brain_checkpoint(
                    project=self.project_key,
                    question=question,
                    options=options,
                    session_id=session_id,
                    timeout=timeout or self.default_timeout,
                )
            else:
                # HTTP fallback
                response = self._http_checkpoint(question, options, timeout, session_id)
            
            duration = time.time() - start_time
            
            result = CheckpointResult(
                status=CheckpointStatus(response.get("status", "timeout")),
                question=question,
                options=options,
                response=response.get("response"),
                selected_option=response.get("selected_option"),
                session_id=session_id or response.get("session_id"),
                duration_seconds=duration,
                metadata={"context": context} if context else {},
            )
            
        except Exception as e:
            logger.error(f"Checkpoint failed: {e}")
            result = CheckpointResult(
                status=CheckpointStatus.TIMEOUT,
                question=question,
                options=options,
                duration_seconds=time.time() - start_time,
                metadata={"error": str(e), "context": context} if context else {"error": str(e)},
            )
        
        self._log_checkpoint(result)
        return result
    
    def _http_checkpoint(
        self,
        question: str,
        options: List[str],
        timeout: Optional[int],
        session_id: Optional[str],
    ) -> Dict[str, Any]:
        """HTTP fallback for checkpoint."""
        # This would use the client's HTTP methods
        # Simplified for now
        return {
            "status": "timeout",
            "response": None,
            "selected_option": None,
        }
    
    def _local_prompt(
        self,
        question: str,
        options: List[str],
        timeout: int,
    ) -> CheckpointResult:
        """Local interactive prompt for development."""
        import sys
        import select
        import time
        
        print(f"\n{'='*60}")
        print(f"CHECKPOINT REQUIRED")
        print(f"{'='*60}")
        print(f"\nQuestion: {question}")
        print(f"\nOptions:")
        for i, opt in enumerate(options):
            print(f"  {i+1}. {opt}")
        print(f"\nTimeout: {timeout}s (press Ctrl+C to skip)")
        
        start = time.time()
        
        # Non-blocking input with timeout
        try:
            if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
                choice = sys.stdin.readline().strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(options):
                        duration = time.time() - start
                        return CheckpointResult(
                            status=CheckpointStatus.RESPONDED,
                            question=question,
                            options=options,
                            response=choice,
                            selected_option=idx,
                            duration_seconds=duration,
                        )
                except ValueError:
                    pass
        except KeyboardInterrupt:
            pass
        
        # Timeout or invalid input
        duration = time.time() - start
        return CheckpointResult(
            status=CheckpointStatus.TIMEOUT,
            question=question,
            options=options,
            duration_seconds=duration,
        )
    
    # ========================================
    # SPECIALIZED CHECKPOINTS
    # ========================================
    
    def task_complete_checkpoint(
        self,
        task_summary: str,
        next_steps: Optional[List[str]] = None,
    ) -> CheckpointResult:
        """Checkpoint for task completion - asks what to do next."""
        options = next_steps or [
            "Continue with next task",
            "Review current work",
            "Change direction",
            "End session",
        ]
        
        return self.create_checkpoint(
            question=f"Task complete: {task_summary}. What would you like me to work on next?",
            options=options,
            context="task_completion",
        )
    
    def design_decision_checkpoint(
        self,
        decision: str,
        options: List[str],
        context: Optional[str] = None,
    ) -> CheckpointResult:
        """Checkpoint for design/architecture decisions."""
        return self.create_checkpoint(
            question=f"Design decision needed: {decision}",
            options=options,
            context=f"design_decision:{context}" if context else "design_decision",
        )
    
    def plan_approval_checkpoint(
        self,
        plan_summary: str,
        options: Optional[List[str]] = None,
    ) -> CheckpointResult:
        """Checkpoint for plan approval before execution."""
        return self.create_checkpoint(
            question=f"Approve plan: {plan_summary}",
            options=options or ["Approve and proceed", "Modify plan", "Cancel"],
            context="plan_approval",
        )
    
    def clarification_checkpoint(
        self,
        question: str,
        options: List[str],
    ) -> CheckpointResult:
        """Checkpoint for clarifying ambiguity."""
        return self.create_checkpoint(
            question=f"Clarification needed: {question}",
            options=options,
            context="clarification",
        )
    
    def get_history(self, limit: Optional[int] = None) -> List[CheckpointResult]:
        """Get checkpoint history."""
        history = self.checkpoints_history
        if limit:
            history = history[-limit:]
        return history
    
    def get_pending_checkpoints(self) -> List[CheckpointResult]:
        """Get checkpoints still awaiting response."""
        return [c for c in self.checkpoints_history if c.status == CheckpointStatus.PENDING]
    
    def export_history(self, filepath: str):
        """Export checkpoint history to JSON."""
        data = {
            "checkpoints": [
                {
                    "status": c.status.value,
                    "question": c.question,
                    "options": c.options,
                    "response": c.response,
                    "selected_option": c.selected_option,
                    "session_id": c.session_id,
                    "timestamp": c.timestamp,
                    "duration_seconds": c.duration_seconds,
                    "metadata": c.metadata,
                }
                for c in self.checkpoints_history
            ],
            "exported_at": datetime.now().isoformat(),
        }
        Path(filepath).write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    # Test
    manager = CheckpointManager()
    result = manager.task_complete_checkpoint(
        "Created project structure and GitHub repo",
        ["Setup Docker infrastructure", "Configure Agent Brain MCP", "Start Unity project init"]
    )
    print(f"Result: {result.status.value}, Selected: {result.selected_option}")
"""
Agent Brain Client for MAXX Project
Provides MCP-compatible interface to Agent Brain memory, mailbox, and checkpoints.
"""

import os
import json
import httpx
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
from loguru import logger


@dataclass
class AgentBrainConfig:
    """Configuration for Agent Brain connection."""
    base_url: str = "http://localhost:3030"
    project_key: str = ""
    timeout: float = 30.0
    
    @classmethod
    def from_env(cls) -> "AgentBrainConfig":
        """Create config from environment variables."""
        return cls(
            base_url=os.getenv("AGENT_BRAIN_URL", "http://localhost:3030"),
            project_key=os.getenv("AGENT_BRAIN_PROJECT_KEY", ""),
        )


class AgentBrainClient:
    """Client for interacting with Agent Brain API."""
    
    def __init__(self, config: Optional[AgentBrainConfig] = None):
        self.config = config or AgentBrainConfig.from_env()
        self._client: Optional[httpx.AsyncClient] = None
        self._sync_client: Optional[httpx.Client] = None
    
    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.config.base_url,
                timeout=self.config.timeout,
            )
        return self._client
    
    @property
    def sync_client(self) -> httpx.Client:
        """Get or create sync HTTP client."""
        if self._sync_client is None:
            self._sync_client = httpx.Client(
                base_url=self.config.base_url,
                timeout=self.config.timeout,
            )
        return self._sync_client
    
    def close(self):
        """Close HTTP clients."""
        if self._client:
            self._client.close()
        if self._sync_client:
            self._sync_client.close()
    
    async def aclose(self):
        """Async close HTTP clients."""
        if self._client:
            await self._client.aclose()
        if self._sync_client:
            self._sync_client.close()
    
    # ========================================
    # MEMORY OPERATIONS
    # ========================================
    
    def read_memory(
        self,
        sections: Optional[List[str]] = None,
        task: Optional[str] = None,
        project_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Read project memory from Agent Brain."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        params = {}
        if sections:
            params["sections"] = ",".join(sections)
        if task:
            params["task"] = task
        
        response = self.sync_client.get(f"/api/memory/{project}", params=params)
        response.raise_for_status()
        return response.json()
    
    async def aread_memory(
        self,
        sections: Optional[List[str]] = None,
        task: Optional[str] = None,
        project_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Async read project memory."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        params = {}
        if sections:
            params["sections"] = ",".join(sections)
        if task:
            params["task"] = task
        
        response = await self.client.get(f"/api/memory/{project}", params=params)
        response.raise_for_status()
        return response.json()
    
    def write_memory(self, content: str, project_key: Optional[str] = None) -> Dict[str, Any]:
        """Write project memory to Agent Brain."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        response = self.sync_client.put(
            f"/api/memory/{project}",
            json={"content": content}
        )
        response.raise_for_status()
        return response.json()
    
    async def awrite_memory(self, content: str, project_key: Optional[str] = None) -> Dict[str, Any]:
        """Async write project memory."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        response = await self.client.put(
            f"/api/memory/{project}",
            json={"content": content}
        )
        response.raise_for_status()
        return response.json()
    
    def list_memory_sections(self, project_key: Optional[str] = None) -> List[str]:
        """List available memory sections."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        response = self.sync_client.get(f"/api/memory/{project}?list=true")
        response.raise_for_status()
        return response.json().get("sections", [])
    
    # ========================================
    # DAILY LOG
    # ========================================
    
    def write_daily_log(self, content: str, project_key: Optional[str] = None) -> Dict[str, Any]:
        """Append daily log entry."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        response = self.sync_client.post(
            f"/api/memory/{project}/daily",
            json={"content": content}
        )
        response.raise_for_status()
        return response.json()
    
    # ========================================
    # MAILBOX OPERATIONS
    # ========================================
    
    def check_mailbox(
        self,
        project: str = "broadcast",
        unread_only: bool = True,
        project_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Check mailbox for messages."""
        target = project_key or self.config.project_key
        if project != "broadcast" and not target:
            raise ValueError("Project key required for project-specific mailbox")
        
        params = {"unread": str(unread_only).lower()}
        if project != "broadcast":
            params["project"] = target
        
        response = self.sync_client.get(f"/api/mailbox/{project}", params=params)
        response.raise_for_status()
        return response.json().get("messages", [])
    
    def send_message(
        self,
        to_session: str,
        subject: str,
        body: str,
        from_session: Optional[str] = None,
        project_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send message to another session/project."""
        from_sess = from_session or project_key or self.config.project_key
        if not from_sess:
            raise ValueError("From session (project key) is required")
        
        response = self.sync_client.post(
            "/api/mailbox",
            json={
                "from_session": from_sess,
                "to_session": to_session,
                "subject": subject,
                "body": body
            }
        )
        response.raise_for_status()
        return response.json()
    
    def mark_read(self, message_id: str) -> Dict[str, Any]:
        """Mark message as read."""
        response = self.sync_client.post(f"/api/mailbox/{message_id}/read")
        response.raise_for_status()
        return response.json()
    
    # ========================================
    # CHECKPOINT OPERATIONS
    # ========================================
    
    def create_checkpoint(
        self,
        question: str,
        options: Optional[List[str]] = None,
        session_id: Optional[str] = None,
        claude_session_id: Optional[str] = None,
        project_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a checkpoint for user approval."""
        project = project_key or self.config.project_key
        if not project:
            raise ValueError("Project key is required")
        
        payload = {
            "project_dir": project,
            "question": question,
        }
        if options:
            payload["options"] = options
        if session_id:
            payload["session_id"] = session_id
        if claude_session_id:
            payload["claude_session_id"] = claude_session_id
        
        response = self.sync_client.post("/api/checkpoints", json=payload)
        response.raise_for_status()
        return response.json()
    
    def wait_for_checkpoint(self, checkpoint_id: str, timeout: float = 86400) -> Dict[str, Any]:
        """Wait for checkpoint response (blocking)."""
        # This would use long-polling or WebSocket in real implementation
        # For now, return the checkpoint status
        response = self.sync_client.get(f"/api/checkpoints/{checkpoint_id}")
        response.raise_for_status()
        return response.json()
    
    # ========================================
    # HEALTH CHECK
    # ========================================
    
    def health_check(self) -> bool:
        """Check if Agent Brain is healthy."""
        try:
            response = self.sync_client.get("/health", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False
    
    async def ahealth_check(self) -> bool:
        """Async health check."""
        try:
            response = await self.client.get("/health", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False


# ========================================
# HIGH-LEVEL HELPERS
# ========================================

def get_project_key() -> str:
    """Get project key from environment or compute from cwd."""
    key = os.getenv("AGENT_BRAIN_PROJECT_KEY")
    if key:
        return key
    
    # Compute from current working directory
    cwd = Path.cwd()
    return str(cwd).replace("/", "-").replace("\\", "-").replace(":", "-")


def create_client() -> AgentBrainClient:
    """Create AgentBrainClient with auto-detected project key."""
    config = AgentBrainConfig.from_env()
    if not config.project_key:
        config.project_key = get_project_key()
    return AgentBrainClient(config)


# ========================================
# CONTEXT MANAGER SUPPORT
# ========================================

class AgentBrainSession:
    """Context manager for Agent Brain session lifecycle."""
    
    def __init__(self, client: Optional[AgentBrainClient] = None):
        self.client = client or create_client()
        self.session_started = False
    
    def __enter__(self) -> AgentBrainClient:
        # Read memory at session start
        try:
            memory = self.client.read_memory()
            logger.info(f"Loaded project memory: {len(str(memory))} chars")
        except Exception as e:
            logger.warning(f"Could not load memory: {e}")
        
        # Check mailbox
        try:
            messages = self.client.check_mailbox("broadcast")
            if messages:
                logger.info(f"Found {len(messages)} broadcast messages")
            messages = self.client.check_mailbox(self.client.config.project_key)
            if messages:
                logger.info(f"Found {len(messages)} project messages")
        except Exception as e:
            logger.warning(f"Could not check mailbox: {e}")
        
        self.session_started = True
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Write memory at session end (would need updated content)
        # This is a placeholder - actual implementation would track changes
        self.client.close()
        return False


# Example usage
if __name__ == "__main__":
    # Quick test
    client = create_client()
    print(f"Project key: {client.config.project_key}")
    print(f"Health check: {client.health_check()}")
    client.close()
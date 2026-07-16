"""
Docker Manager for MAXX Project
Handles Docker Compose operations, image building, and container management.
"""

import os
import subprocess
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
from loguru import logger


@dataclass
class DockerConfig:
    """Docker configuration."""
    compose_file: str = "docker-compose.yml"
    project_name: str = "maxx"
    registry: str = "docker.io"
    build_parallel: bool = True


class DockerManager:
    """Manages Docker operations for the project."""
    
    def __init__(self, config: Optional[DockerConfig] = None):
        self.config = config or DockerConfig()
        self.project_root = Path.cwd()
    
    def _run(self, cmd: List[str], capture: bool = True) -> subprocess.CompletedProcess:
        """Run a command."""
        full_cmd = ["docker"] + cmd
        logger.debug(f"Running: {' '.join(full_cmd)}")
        
        result = subprocess.run(
            full_cmd,
            cwd=self.project_root,
            capture_output=capture,
            text=True,
        )
        
        if result.returncode != 0:
            logger.error(f"Command failed: {' '.join(full_cmd)}")
            logger.error(f"stderr: {result.stderr}")
        
        return result
    
    def _compose_cmd(self, *args: str) -> List[str]:
        """Build docker-compose command."""
        cmd = ["compose", "-f", self.config.compose_file, "-p", self.config.project_name]
        cmd.extend(args)
        return cmd
    
    # ========================================
    # COMPOSE OPERATIONS
    # ========================================
    
    def up(
        self,
        services: Optional[List[str]] = None,
        profiles: Optional[List[str]] = None,
        detach: bool = True,
        build: bool = False,
    ) -> bool:
        """Start services with docker-compose up."""
        cmd = self._compose_cmd("up")
        
        if detach:
            cmd.append("-d")
        if build:
            cmd.append("--build")
        
        if profiles:
            for p in profiles:
                cmd.extend(["--profile", p])
        
        if services:
            cmd.extend(services)
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    def down(self, volumes: bool = False, remove_orphans: bool = True) -> bool:
        """Stop and remove containers."""
        cmd = self._compose_cmd("down")
        
        if volumes:
            cmd.append("-v")
        if remove_orphans:
            cmd.append("--remove-orphans")
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    def ps(self, services: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """List running containers."""
        cmd = self._compose_cmd("ps", "--format", "json")
        if services:
            cmd.extend(services)
        
        result = self._run(cmd)
        if result.returncode != 0:
            return []
        
        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    containers.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return containers
    
    def logs(
        self,
        service: Optional[str] = None,
        follow: bool = False,
        tail: Optional[int] = 100,
    ) -> str:
        """Get container logs."""
        cmd = self._compose_cmd("logs")
        
        if follow:
            cmd.append("-f")
        if tail:
            cmd.extend(["--tail", str(tail)])
        if service:
            cmd.append(service)
        
        result = self._run(cmd)
        return result.stdout
    
    def exec(
        self,
        service: str,
        command: List[str],
        user: Optional[str] = None,
        workdir: Optional[str] = None,
    ) -> subprocess.CompletedProcess:
        """Execute command in running container."""
        cmd = self._compose_cmd("exec")
        
        if user:
            cmd.extend(["-u", user])
        if workdir:
            cmd.extend(["-w", workdir])
        
        cmd.append(service)
        cmd.extend(command)
        
        return self._run(cmd, capture=False)
    
    def restart(self, services: Optional[List[str]] = None) -> bool:
        """Restart services."""
        cmd = self._compose_cmd("restart")
        if services:
            cmd.extend(services)
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    def pull(self, services: Optional[List[str]] = None) -> bool:
        """Pull latest images."""
        cmd = self._compose_cmd("pull")
        if services:
            cmd.extend(services)
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    # ========================================
    # BUILD OPERATIONS
    # ========================================
    
    def build(
        self,
        services: Optional[List[str]] = None,
        no_cache: bool = False,
        pull: bool = True,
        build_args: Optional[Dict[str, str]] = None,
    ) -> bool:
        """Build Docker images."""
        cmd = self._compose_cmd("build")
        
        if no_cache:
            cmd.append("--no-cache")
        if pull:
            cmd.append("--pull")
        if build_args:
            for k, v in build_args.items():
                cmd.extend(["--build-arg", f"{k}={v}"])
        
        if services:
            cmd.extend(services)
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    def build_image(
        self,
        dockerfile: str,
        tag: str,
        context: str = ".",
        no_cache: bool = False,
        build_args: Optional[Dict[str, str]] = None,
        target: Optional[str] = None,
    ) -> bool:
        """Build a single Docker image."""
        cmd = ["build", "-f", dockerfile, "-t", tag, context]
        
        if no_cache:
            cmd.append("--no-cache")
        if target:
            cmd.extend(["--target", target])
        if build_args:
            for k, v in build_args.items():
                cmd.extend(["--build-arg", f"{k}={v}"])
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    # ========================================
    # REGISTRY OPERATIONS
    # ========================================
    
    def login(self, username: str, password: str, registry: Optional[str] = None) -> bool:
        """Login to Docker registry."""
        cmd = ["login"]
        if registry:
            cmd.append(registry)
        cmd.extend(["-u", username, "-p", password])
        
        result = self._run(cmd)
        return result.returncode == 0
    
    def push(self, tag: str) -> bool:
        """Push image to registry."""
        cmd = ["push", tag]
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    def tag(self, source: str, target: str) -> bool:
        """Tag an image."""
        cmd = ["tag", source, target]
        result = self._run(cmd)
        return result.returncode == 0
    
    # ========================================
    # HEALTH & STATUS
    # ========================================
    
    def health_check(self, service: str) -> Dict[str, Any]:
        """Check health of a service."""
        containers = self.ps([service])
        if not containers:
            return {"healthy": False, "status": "not_running"}
        
        container = containers[0]
        health = container.get("Health", {})
        status = health.get("Status", "unknown")
        
        return {
            "healthy": status == "healthy",
            "status": status,
            "container": container,
        }
    
    def wait_for_healthy(
        self,
        service: str,
        timeout: int = 120,
        interval: int = 5,
    ) -> bool:
        """Wait for service to become healthy."""
        import time
        
        start = time.time()
        while time.time() - start < timeout:
            health = self.health_check(service)
            if health["healthy"]:
                return True
            time.sleep(interval)
        
        return False
    
    def get_service_url(self, service: str, port: int) -> Optional[str]:
        """Get accessible URL for a service port."""
        containers = self.ps([service])
        if not containers:
            return None
        
        container = containers[0]
        ports = container.get("Ports", "")
        
        # Parse port mapping
        for mapping in ports.split(", "):
            if f"->{port}/tcp" in mapping:
                host_port = mapping.split("->")[0].split(":")[-1]
                return f"http://localhost:{host_port}"
        
        return None
    
    # ========================================
    # CLEANUP
    # ========================================
    
    def prune(self, volumes: bool = False, images: bool = False) -> bool:
        """Prune unused Docker resources."""
        cmd = ["system", "prune", "-f"]
        if volumes:
            cmd.append("--volumes")
        if images:
            cmd.append("-a")
        
        result = self._run(cmd, capture=False)
        return result.returncode == 0
    
    def remove_image(self, tag: str, force: bool = False) -> bool:
        """Remove a Docker image."""
        cmd = ["rmi"]
        if force:
            cmd.append("-f")
        cmd.append(tag)
        
        result = self._run(cmd)
        return result.returncode == 0
    
    # ========================================
    # UTILITY
    # ========================================
    
    def validate_compose(self) -> bool:
        """Validate docker-compose file."""
        cmd = self._compose_cmd("config", "--quiet")
        result = self._run(cmd)
        return result.returncode == 0
    
    def get_config(self) -> Dict[str, Any]:
        """Get resolved compose config."""
        cmd = self._compose_cmd("config", "--format", "json")
        result = self._run(cmd)
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {}
    
    def list_images(self, filter_: Optional[str] = None) -> List[Dict[str, Any]]:
        """List Docker images."""
        cmd = ["images", "--format", "json"]
        if filter_:
            cmd.extend(["-f", filter_])
        
        result = self._run(cmd)
        images = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    images.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return images


# Convenience functions
def get_docker_manager() -> DockerManager:
    """Get Docker manager instance."""
    return DockerManager()


def start_infrastructure() -> bool:
    """Start core infrastructure (Agent Brain, DB, etc)."""
    mgr = get_docker_manager()
    return mgr.up(
        services=["agent-brain", "postgres", "redis"],
        detach=True,
    )


def start_agents() -> bool:
    """Start agent runners."""
    mgr = get_docker_manager()
    return mgr.up(
        services=["claude-code-runner", "codex-runner"],
        profiles=["agents"],
        detach=True,
    )


def start_workers() -> bool:
    """Start 3D/video generation workers."""
    mgr = get_docker_manager()
    return mgr.up(
        services=["meshy-worker", "minimax-worker"],
        profiles=["workers"],
        detach=True,
    )


if __name__ == "__main__":
    mgr = DockerManager()
    
    # Validate
    if mgr.validate_compose():
        print("✅ docker-compose.yml is valid")
    else:
        print("❌ docker-compose.yml has errors")
    
    # Show config
    config = mgr.get_config()
    print(f"Services: {list(config.get('services', {}).keys())}")
"""
Meshy AI Client for MAXX Project
Handles 3D asset generation via Meshy API.
"""

import os
import time
import httpx
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from loguru import logger


class MeshyTaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class MeshyArtStyle(str, Enum):
    REALISTIC = "realistic"
    STYLIZED = "stylized"
    VOXEL = "voxel"
    LOW_POLY = "low_poly"
    SCULPTURE = "sculpture"


class MeshyTopology(str, Enum):
    QUAD = "quad"
    TRIANGLE = "triangle"


@dataclass
class MeshyConfig:
    api_key: str = ""
    base_url: str = "https://api.meshy.ai/v1"
    timeout: float = 300.0
    rate_limit_rpm: int = 30
    max_concurrent: int = 5
    
    @classmethod
    def from_env(cls) -> "MeshyConfig":
        return cls(
            api_key=os.getenv("MESHY_API_KEY", ""),
            base_url=os.getenv("MESHY_BASE_URL", "https://api.meshy.ai/v1"),
        )


@dataclass
class MeshyTask:
    task_id: str
    status: MeshyTaskStatus
    progress: int = 0
    model_urls: Dict[str, str] = None
    thumbnail_url: str = ""
    error: str = ""
    created_at: str = ""
    completed_at: str = ""
    
    def __post_init__(self):
        if self.model_urls is None:
            self.model_urls = {}


class MeshyClient:
    """Client for Meshy AI 3D generation API."""
    
    def __init__(self, config: Optional[MeshyConfig] = None):
        self.config = config or MeshyConfig.from_env()
        if not self.config.api_key:
            raise ValueError("MESHY_API_KEY is required")
        
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            timeout=self.config.timeout,
        )
        self.sync_client = httpx.Client(
            base_url=self.config.base_url,
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            timeout=self.config.timeout,
        )
    
    def close(self):
        self.client.close()
        self.sync_client.close()
    
    # ========================================
    # TEXT TO 3D
    # ========================================
    
    def create_text_to_3d(
        self,
        prompt: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
        topology: MeshyTopology = MeshyTopology.QUAD,
        target_polycount: int = 30000,
        should_remesh: bool = True,
        symmetrize: bool = True,
        negative_prompt: str = "",
    ) -> str:
        """Create text-to-3D generation task. Returns task ID."""
        payload = {
            "mode": "preview",
            "prompt": prompt,
            "art_style": art_style.value,
            "topology": topology.value,
            "target_polycount": target_polycount,
            "should_remesh": should_remesh,
            "symmetrize": symmetrize,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        response = self.sync_client.post("/text-to-3d", json=payload)
        response.raise_for_status()
        return response.json()["result"]
    
    async def acreate_text_to_3d(
        self,
        prompt: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
        topology: MeshyTopology = MeshyTopology.QUAD,
        target_polycount: int = 30000,
        should_remesh: bool = True,
        symmetrize: bool = True,
        negative_prompt: str = "",
    ) -> str:
        """Async create text-to-3D generation task."""
        payload = {
            "mode": "preview",
            "prompt": prompt,
            "art_style": art_style.value,
            "topology": topology.value,
            "target_polycount": target_polycount,
            "should_remesh": should_remesh,
            "symmetrize": symmetrize,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        response = await self.client.post("/text-to-3d", json=payload)
        response.raise_for_status()
        return response.json()["result"]
    
    # ========================================
    # IMAGE TO 3D
    # ========================================
    
    def create_image_to_3d(
        self,
        image_url: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
        topology: MeshyTopology = MeshyTopology.QUAD,
        target_polycount: int = 30000,
        should_remesh: bool = True,
        enable_pbr: bool = True,
    ) -> str:
        """Create image-to-3D generation task. Returns task ID."""
        payload = {
            "mode": "preview",
            "image_url": image_url,
            "art_style": art_style.value,
            "topology": topology.value,
            "target_polycount": target_polycount,
            "should_remesh": should_remesh,
            "enable_pbr": enable_pbr,
        }
        
        response = self.sync_client.post("/image-to-3d", json=payload)
        response.raise_for_status()
        return response.json()["result"]
    
    # ========================================
    # VIDEO TO 3D
    # ========================================
    
    def create_video_to_3d(
        self,
        video_url: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
        target_polycount: int = 30000,
    ) -> str:
        """Create video-to-3D generation task. Returns task ID."""
        payload = {
            "mode": "preview",
            "video_url": video_url,
            "art_style": art_style.value,
            "target_polycount": target_polycount,
        }
        
        response = self.sync_client.post("/video-to-3d", json=payload)
        response.raise_for_status()
        return response.json()["result"]
    
    # ========================================
    # TEXT TO TEXTURE
    # ========================================
    
    def create_text_to_texture(
        self,
        prompt: str,
        model_url: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
    ) -> str:
        """Create text-to-texture task for existing model. Returns task ID."""
        payload = {
            "mode": "preview",
            "prompt": prompt,
            "model_url": model_url,
            "art_style": art_style.value,
        }
        
        response = self.sync_client.post("/text-to-texture", json=payload)
        response.raise_for_status()
        return response.json()["result"]
    
    # ========================================
    # TASK STATUS
    # ========================================
    
    def get_task_status(self, task_id: str) -> MeshyTask:
        """Get task status."""
        response = self.sync_client.get(f"/tasks/{task_id}")
        response.raise_for_status()
        data = response.json()
        
        return MeshyTask(
            task_id=data["id"],
            status=MeshyTaskStatus(data["status"]),
            progress=data.get("progress", 0),
            model_urls=data.get("model_urls", {}),
            thumbnail_url=data.get("thumbnail_url", ""),
            error=data.get("error", ""),
            created_at=data.get("created_at", ""),
            completed_at=data.get("completed_at", ""),
        )
    
    async def aget_task_status(self, task_id: str) -> MeshyTask:
        """Async get task status."""
        response = await self.client.get(f"/tasks/{task_id}")
        response.raise_for_status()
        data = response.json()
        
        return MeshyTask(
            task_id=data["id"],
            status=MeshyTaskStatus(data["status"]),
            progress=data.get("progress", 0),
            model_urls=data.get("model_urls", {}),
            thumbnail_url=data.get("thumbnail_url", ""),
            error=data.get("error", ""),
            created_at=data.get("created_at", ""),
            completed_at=data.get("completed_at", ""),
        )
    
    def wait_for_task(
        self,
        task_id: str,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> MeshyTask:
        """Wait for task to complete."""
        start = time.time()
        
        while time.time() - start < timeout:
            task = self.get_task_status(task_id)
            
            if task.status == MeshyTaskStatus.SUCCEEDED:
                logger.info(f"Task {task_id} completed successfully")
                return task
            
            if task.status == MeshyTaskStatus.FAILED:
                logger.error(f"Task {task_id} failed: {task.error}")
                return task
            
            logger.info(f"Task {task_id}: {task.status.value} ({task.progress}%)")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Task {task_id} timed out after {timeout}s")
    
    # ========================================
    # DOWNLOAD
    # ========================================
    
    def download_model(
        self,
        task_id: str,
        output_dir: str,
        format: str = "glb",
    ) -> List[str]:
        """Download generated model files."""
        task = self.get_task_status(task_id)
        
        if task.status != MeshyTaskStatus.SUCCEEDED:
            raise ValueError(f"Task {task_id} not completed: {task.status}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        downloaded = []
        
        # Download main model
        model_url = task.model_urls.get(format)
        if model_url:
            filepath = output_path / f"{task_id}.{format}"
            self._download_file(model_url, filepath)
            downloaded.append(str(filepath))
        
        # Download thumbnail
        if task.thumbnail_url:
            thumb_path = output_path / f"{task_id}_thumb.jpg"
            self._download_file(task.thumbnail_url, thumb_path)
            downloaded.append(str(thumb_path))
        
        logger.info(f"Downloaded {len(downloaded)} files to {output_dir}")
        return downloaded
    
    def _download_file(self, url: str, filepath: Path):
        """Download a file."""
        with self.sync_client.stream("GET", url) as response:
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
    
    # ========================================
    # HIGH-LEVEL WORKFLOWS
    # ========================================
    
    def generate_asset(
        self,
        prompt: str,
        output_dir: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
        **kwargs
    ) -> MeshyTask:
        """Complete workflow: generate and download asset."""
        logger.info(f"Generating 3D asset: {prompt}")
        
        # Create task
        task_id = self.create_text_to_3d(prompt, art_style=art_style, **kwargs)
        logger.info(f"Created task: {task_id}")
        
        # Wait for completion
        task = self.wait_for_task(task_id)
        
        if task.status == MeshyTaskStatus.SUCCEEDED:
            # Download
            self.download_model(task_id, output_dir)
        
        return task
    
    def generate_asset_async(
        self,
        prompt: str,
        output_dir: str,
        art_style: MeshyArtStyle = MeshyArtStyle.REALISTIC,
        callback: Optional[callable] = None,
        **kwargs
    ) -> str:
        """Start async generation workflow. Returns task ID."""
        import asyncio
        
        async def _workflow():
            task_id = await self.acreate_text_to_3d(prompt, art_style=art_style, **kwargs)
            
            while True:
                task = await self.aget_task_status(task_id)
                if callback:
                    callback(task)
                
                if task.status in (MeshyTaskStatus.SUCCEEDED, MeshyTaskStatus.FAILED):
                    if task.status == MeshyTaskStatus.SUCCEEDED:
                        self.download_model(task_id, output_dir)
                    break
                
                await asyncio.sleep(5)
            
            return task
        
        # Start in background
        loop = asyncio.get_event_loop()
        loop.create_task(_workflow())
        return task_id


if __name__ == "__main__":
    # Test
    client = MeshyClient()
    print(f"Meshy client ready: {client.config.base_url}")
    client.close()
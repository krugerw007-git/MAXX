"""
Minimax AI Client for MAXX Project
Handles video, audio, and music generation via Minimax API.
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


class MinimaxTaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class MinimaxVideoModel(str, Enum):
    VIDEO_01 = "video-01"


class MinimaxAudioModel(str, Enum):
    SPEECH_01 = "speech-01"
    SPEECH_02 = "speech-02"
    TTS_01 = "tts-01"


class MinimaxVoice(str, Enum):
    MALE_QN_QINGSE = "male-qn-qingse"
    FEMALE_QN_QINGSE = "female-qn-qingse"
    MALE_QN_JINGSHEN = "male-qn-jingshen"
    FEMALE_QN_JINGSHEN = "female-qn-jingshen"
    MALE_QN_BIAODIAN = "male-qn-biaodian"
    FEMALE_QN_BIAODIAN = "female-qn-biaodian"


@dataclass
class MinimaxConfig:
    api_key: str = ""
    base_url: str = "https://api.minimax.chat/v1"
    timeout: float = 300.0
    group_id: str = ""
    
    @classmethod
    def from_env(cls) -> "MinimaxConfig":
        return cls(
            api_key=os.getenv("MINIMAX_API_KEY", ""),
            base_url=os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1"),
            group_id=os.getenv("MINIMAX_GROUP_ID", ""),
        )


@dataclass
class MinimaxTask:
    task_id: str
    status: MinimaxTaskStatus
    file_url: str = ""
    error: str = ""
    created_at: str = ""
    completed_at: str = ""


class MinimaxClient:
    """Client for Minimax AI generation APIs."""
    
    def __init__(self, config: Optional[MinimaxConfig] = None):
        self.config = config or MinimaxConfig.from_env()
        if not self.config.api_key:
            raise ValueError("MINIMAX_API_KEY is required")
        if not self.config.group_id:
            logger.warning("MINIMAX_GROUP_ID not set - some endpoints may fail")
        
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=self.config.timeout,
        )
        self.sync_client = httpx.Client(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=self.config.timeout,
        )
    
    def close(self):
        self.client.close()
        self.sync_client.close()
    
    def _get_group_id(self) -> str:
        """Get group_id for requests."""
        return self.config.group_id or "default"
    
    # ========================================
    # VIDEO GENERATION
    # ========================================
    
    def create_video_generation(
        self,
        prompt: str,
        model: MinimaxVideoModel = MinimaxVideoModel.VIDEO_01,
        duration: int = 6,
        resolution: str = "1280x720",
        fps: int = 24,
    ) -> str:
        """Create video generation task. Returns task ID."""
        payload = {
            "model": model.value,
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "fps": fps,
        }
        
        response = self.sync_client.post(
            f"/video/generation?GroupId={self._get_group_id()}",
            json=payload,
        )
        response.raise_for_status()
        return response.json()["task_id"]
    
    async def acreate_video_generation(
        self,
        prompt: str,
        model: MinimaxVideoModel = MinimaxVideoModel.VIDEO_01,
        duration: int = 6,
        resolution: str = "1280x720",
        fps: int = 24,
    ) -> str:
        """Async create video generation task."""
        payload = {
            "model": model.value,
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "fps": fps,
        }
        
        response = await self.client.post(
            f"/video/generation?GroupId={self._get_group_id()}",
            json=payload,
        )
        response.raise_for_status()
        return response.json()["task_id"]
    
    # ========================================
    # AUDIO GENERATION (TTS)
    # ========================================
    
    def create_audio_generation(
        self,
        text: str,
        model: MinimaxAudioModel = MinimaxAudioModel.SPEECH_01,
        voice: MinimaxVoice = MinimaxVoice.MALE_QN_QINGSE,
        speed: float = 1.0,
        pitch: int = 0,
        volume: float = 1.0,
        emotion: str = "neutral",
    ) -> str:
        """Create audio/speech generation task. Returns task ID."""
        payload = {
            "model": model.value,
            "text": text,
            "voice": voice.value,
            "speed": speed,
            "pitch": pitch,
            "volume": volume,
            "emotion": emotion,
        }
        
        response = self.sync_client.post(
            f"/audio/generation?GroupId={self._get_group_id()}",
            json=payload,
        )
        response.raise_for_status()
        return response.json()["task_id"]
    
    # ========================================
    # MUSIC GENERATION
    # ========================================
    
    def create_music_generation(
        self,
        prompt: str,
        duration: int = 30,
        style: str = "ambient",
        mood: str = "calm",
    ) -> str:
        """Create music generation task. Returns task ID."""
        payload = {
            "prompt": prompt,
            "duration": duration,
            "style": style,
            "mood": mood,
        }
        
        response = self.sync_client.post(
            f"/music/generation?GroupId={self._get_group_id()}",
            json=payload,
        )
        response.raise_for_status()
        return response.json()["task_id"]
    
    # ========================================
    # VOICE CLONING
    # ========================================
    
    def create_voice_clone(
        self,
        audio_url: str,
        name: str,
        text: str = "",
    ) -> str:
        """Create voice cloning task. Returns task ID."""
        payload = {
            "audio_url": audio_url,
            "name": name,
        }
        if text:
            payload["text"] = text
        
        response = self.sync_client.post(
            f"/voice/clone?GroupId={self._get_group_id()}",
            json=payload,
        )
        response.raise_for_status()
        return response.json()["task_id"]
    
    # ========================================
    # TASK STATUS
    # ========================================
    
    def get_task_status(self, task_id: str) -> MinimaxTask:
        """Get task status."""
        response = self.sync_client.get(
            f"/tasks/{task_id}?GroupId={self._get_group_id()}"
        )
        response.raise_for_status()
        data = response.json()
        
        return MinimaxTask(
            task_id=data["task_id"],
            status=MinimaxTaskStatus(data["status"]),
            file_url=data.get("file_url", ""),
            error=data.get("error", ""),
            created_at=data.get("created_at", ""),
            completed_at=data.get("completed_at", ""),
        )
    
    async def aget_task_status(self, task_id: str) -> MinimaxTask:
        """Async get task status."""
        response = await self.client.get(
            f"/tasks/{task_id}?GroupId={self._get_group_id()}"
        )
        response.raise_for_status()
        data = response.json()
        
        return MinimaxTask(
            task_id=data["task_id"],
            status=MinimaxTaskStatus(data["status"]),
            file_url=data.get("file_url", ""),
            error=data.get("error", ""),
            created_at=data.get("created_at", ""),
            completed_at=data.get("completed_at", ""),
        )
    
    def wait_for_task(
        self,
        task_id: str,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
    ) -> MinimaxTask:
        """Wait for task to complete."""
        start = time.time()
        
        while time.time() - start < timeout:
            task = self.get_task_status(task_id)
            
            if task.status == MinimaxTaskStatus.SUCCEEDED:
                logger.info(f"Task {task_id} completed successfully")
                return task
            
            if task.status == MinimaxTaskStatus.FAILED:
                logger.error(f"Task {task_id} failed: {task.error}")
                return task
            
            logger.info(f"Task {task_id}: {task.status.value}")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Task {task_id} timed out after {timeout}s")
    
    # ========================================
    # DOWNLOAD
    # ========================================
    
    def download_result(
        self,
        task_id: str,
        output_dir: str,
        filename: Optional[str] = None,
    ) -> str:
        """Download generated file."""
        task = self.get_task_status(task_id)
        
        if task.status != MinimaxTaskStatus.SUCCEEDED:
            raise ValueError(f"Task {task_id} not completed: {task.status}")
        
        if not task.file_url:
            raise ValueError(f"No file URL for task {task_id}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if not filename:
            ext = Path(task.file_url).suffix or ".mp4"
            filename = f"{task_id}{ext}"
        
        filepath = output_path / filename
        
        with self.sync_client.stream("GET", task.file_url) as response:
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
        
        logger.info(f"Downloaded result to {filepath}")
        return str(filepath)
    
    # ========================================
    # HIGH-LEVEL WORKFLOWS
    # ========================================
    
    def generate_video(
        self,
        prompt: str,
        output_dir: str,
        **kwargs
    ) -> MinimaxTask:
        """Complete video generation workflow."""
        logger.info(f"Generating video: {prompt}")
        
        task_id = self.create_video_generation(prompt, **kwargs)
        task = self.wait_for_task(task_id)
        
        if task.status == MinimaxTaskStatus.SUCCEEDED:
            self.download_result(task_id, output_dir)
        
        return task
    
    def generate_audio(
        self,
        text: str,
        output_dir: str,
        voice: MinimaxVoice = MinimaxVoice.MALE_QN_QINGSE,
        **kwargs
    ) -> MinimaxTask:
        """Complete audio generation workflow."""
        logger.info(f"Generating audio: {text[:50]}...")
        
        task_id = self.create_audio_generation(text, voice=voice, **kwargs)
        task = self.wait_for_task(task_id)
        
        if task.status == MinimaxTaskStatus.SUCCEEDED:
            self.download_result(task_id, output_dir)
        
        return task
    
    def generate_music(
        self,
        prompt: str,
        output_dir: str,
        **kwargs
    ) -> MinimaxTask:
        """Complete music generation workflow."""
        logger.info(f"Generating music: {prompt}")
        
        task_id = self.create_music_generation(prompt, **kwargs)
        task = self.wait_for_task(task_id)
        
        if task.status == MinimaxTaskStatus.SUCCEEDED:
            self.download_result(task_id, output_dir)
        
        return task


if __name__ == "__main__":
    client = MinimaxClient()
    print(f"Minimax client ready: {client.config.base_url}")
    client.close()
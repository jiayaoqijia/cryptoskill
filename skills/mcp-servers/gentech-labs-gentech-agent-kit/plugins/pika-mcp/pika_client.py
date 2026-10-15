"""
Pika MCP Plugin — Fal.ai Pika API Client

Wraps the Pika API available through Fal.ai for programmatic video generation.
Requires FAL_KEY environment variable for authentication.
"""

import os
import json
import time
import logging
from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class VideoAspectRatio(str, Enum):
    """Supported aspect ratios for Pika video generation."""
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    SQUARE = "1:1"


class VideoModel(str, Enum):
    """Pika video models available via Fal.ai."""
    PIKA_2_5 = "fal-ai/pika/v2.5"
    PIKA_2_1 = "fal-ai/pika/v2.1"
    PIKA_2_0 = "fal-ai/pika/v2.0"


@dataclass
class PikaVideoResult:
    """Result from a Pika video generation request."""
    video_url: str
    duration_seconds: float
    request_id: str
    credits_used: int
    model_used: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class PikaClientError(Exception):
    """Base exception for Pika API client errors."""
    pass


class PikaAuthenticationError(PikaClientError):
    """Raised when FAL_KEY is missing or invalid."""
    pass


class PikaGenerationError(PikaClientError):
    """Raised when video generation fails."""
    pass


class PikaClient:
    """
    Client for Pika video generation via Fal.ai API.

    Requires FAL_KEY environment variable set to a valid Fal.ai API key.
    """

    BASE_URL = "https://fal.run"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FAL_KEY")
        if not self.api_key:
            raise PikaAuthenticationError(
                "FAL_KEY is not set. Set the FAL_KEY environment variable "
                "or pass api_key to PikaClient()."
            )
        self._session = None

    def _get_session(self):
        """Lazy-init requests session."""
        if self._session is not None:
            return self._session
        import requests
        sess = requests.Session()
        sess.headers.update({
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json",
        })
        self._session = sess
        return sess

    def text_to_video(
        self,
        prompt: str,
        model: VideoModel = VideoModel.PIKA_2_5,
        aspect_ratio: VideoAspectRatio = VideoAspectRatio.LANDSCAPE,
        duration_seconds: int = 5,
        negative_prompt: Optional[str] = None,
        guidance_scale: Optional[float] = None,
        seed: Optional[int] = None,
        **kwargs
    ) -> PikaVideoResult:
        """
        Generate a video from a text description.

        Args:
            prompt: Text description of the video to generate.
            model: Pika model version (default: PIKA_2_5).
            aspect_ratio: Video aspect ratio.
            duration_seconds: Length of video (5 or 10 seconds).
            negative_prompt: What to avoid in generation.
            guidance_scale: Prompt adherence (higher = stricter).
            seed: Random seed for reproducibility.
            **kwargs: Additional API parameters.

        Returns:
            PikaVideoResult with video URL and metadata.

        Raises:
            PikaGenerationError: If generation fails.
        """
        session = self._get_session()
        url = f"{self.BASE_URL}/{model.value}/text-to-video"

        payload: Dict[str, Any] = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio.value,
            "duration": duration_seconds,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if guidance_scale is not None:
            payload["guidance_scale"] = guidance_scale
        if seed is not None:
            payload["seed"] = seed
        payload.update(kwargs)

        try:
            response = session.post(url, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            raise PikaGenerationError(f"Pika API call failed: {e}") from e

        video_url = (
            result.get("video", {}).get("url",
            result.get("output", {}).get("video_url",
            result.get("video_url", "")))
        )

        return PikaVideoResult(
            video_url=video_url,
            duration_seconds=duration_seconds,
            request_id=result.get("request_id", result.get("id", "unknown")),
            credits_used=result.get("credits_used", 0),
            model_used=model.value,
            metadata={"raw_preview": str(result)[:300]},
        )

    def image_to_video(
        self,
        prompt: str,
        image_url: str,
        model: VideoModel = VideoModel.PIKA_2_5,
        aspect_ratio: VideoAspectRatio = VideoAspectRatio.LANDSCAPE,
        duration_seconds: int = 5,
        **kwargs
    ) -> PikaVideoResult:
        """
        Generate a video from an image with text guidance.

        Args:
            prompt: Text description of motion/animation.
            image_url: URL of source image.
            model: Pika model version.
            aspect_ratio: Video aspect ratio.
            duration_seconds: Length of video.
            **kwargs: Additional API parameters.

        Returns:
            PikaVideoResult with video URL.
        """
        session = self._get_session()
        url = f"{self.BASE_URL}/{model.value}/image-to-video"

        payload: Dict[str, Any] = {
            "prompt": prompt,
            "image_url": image_url,
            "aspect_ratio": aspect_ratio.value,
            "duration": duration_seconds,
        }
        payload.update(kwargs)

        try:
            response = session.post(url, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            raise PikaGenerationError(f"Pika image-to-video failed: {e}") from e

        video_url = result.get("video", {}).get("url", result.get("video_url", ""))
        return PikaVideoResult(
            video_url=video_url or "",
            duration_seconds=duration_seconds,
            request_id=result.get("request_id", "unknown"),
            credits_used=result.get("credits_used", 0),
            model_used=model.value,
        )

    def health_check(self) -> Dict[str, Any]:
        """Verify the client configuration."""
        return {
            "configured": bool(self.api_key),
            "key_preview": f"{self.api_key[:8]}...{self.api_key[-4:]}" if self.api_key and len(self.api_key) > 12 else "set",
            "models": [m.value for m in VideoModel],
            "aspect_ratios": [r.value for r in VideoAspectRatio],
        }

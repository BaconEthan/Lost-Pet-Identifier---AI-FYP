"""
BirdNET audio classification wrapper.

This module integrates BirdNET (via birdnetlib) into the main pipeline as an
optional modality. It converts audio -> species detections -> a compact text
string that can be embedded with CLIP, plus structured metadata for filtering
and display.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import os
import tempfile


@dataclass(frozen=True)
class BirdNetDetection:
    common_name: str
    confidence: float


class BirdNetClassifier:
    """
    Thin wrapper around birdnetlib's Analyzer/Recording.

    If birdnetlib isn't installed, the instance is still constructible, but
    calling `analyze()` raises a RuntimeError.
    """

    def __init__(self):
        try:
            from birdnetlib.analyzer import Analyzer  # type: ignore
        except Exception as e:  # pragma: no cover
            self._available = False
            self._init_error = e
            self._analyzer = None
            return

        self._available = True
        self._init_error = None
        self._analyzer = Analyzer()

    @property
    def available(self) -> bool:
        return bool(self._available)

    def analyze(
        self,
        audio_path: str,
        *,
        min_confidence: float = 0.1,
    ) -> List[BirdNetDetection]:
        if not self._available or self._analyzer is None:  # pragma: no cover
            raise RuntimeError(
                "BirdNET is not available. Install 'birdnetlib' and its dependencies."
            ) from self._init_error

        if not audio_path:
            return []

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        wav_path: Optional[str] = None
        tmp_to_cleanup: Optional[str] = None
        recording = None
        try:
            wav_path, tmp_to_cleanup = self._maybe_convert_to_wav(audio_path)

            from birdnetlib import Recording  # type: ignore

            recording = Recording(self._analyzer, wav_path, min_conf=min_confidence)
            recording.analyze()
        finally:
            if tmp_to_cleanup and os.path.exists(tmp_to_cleanup):
                try:
                    os.unlink(tmp_to_cleanup)
                except Exception:
                    pass

        detections: List[BirdNetDetection] = []
        for detection in getattr(recording, "detections", []) or []:
            common_name = str(detection.get("common_name", "")).strip()
            confidence = float(detection.get("confidence", 0.0))
            if common_name:
                detections.append(BirdNetDetection(common_name=common_name, confidence=confidence))

        detections.sort(key=lambda d: d.confidence, reverse=True)
        return detections

    def format_for_clip(
        self,
        detections: Sequence[BirdNetDetection],
        *,
        max_species: int = 3,
        species_confidence_threshold: float = 0.3,
    ) -> str:
        """
        Convert detections to a short natural-language string for CLIP text embedding.
        """
        if not detections:
            return "bird, unknown species"

        top = [
            d.common_name
            for d in detections[: max(1, max_species)]
            if d.confidence >= species_confidence_threshold
        ]
        if not top:
            return "bird, unknown species"

        if len(top) == 1:
            return f"bird, {top[0]}"
        if len(top) == 2:
            return f"bird, {top[0]} or {top[1]}"
        return f"bird, possibly {top[0]}, {top[1]}, or {top[2]}"

    def to_metadata(
        self,
        detections: Sequence[BirdNetDetection],
        *,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        top = list(detections[: max(0, top_k)])
        return {
            "birdnet_top_species": top[0].common_name if top else None,
            "birdnet_top_confidence": float(top[0].confidence) if top else None,
            "birdnet_detections": [
                {"common_name": d.common_name, "confidence": float(d.confidence)} for d in top
            ],
        }

    def _maybe_convert_to_wav(self, audio_path: str) -> Tuple[str, Optional[str]]:
        """
        Convert audio to WAV if needed.

        Returns:
            (wav_path, temp_wav_path_to_cleanup)
        """
        ext = os.path.splitext(audio_path)[1].lower().lstrip(".")
        if ext == "wav":
            return audio_path, None

        try:
            from pydub import AudioSegment  # type: ignore
        except Exception:
            # If pydub/ffmpeg aren't available, best-effort: pass through.
            return audio_path, None

        tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_wav.close()
        try:
            audio = AudioSegment.from_file(audio_path)
            audio.export(tmp_wav.name, format="wav")
            return tmp_wav.name, tmp_wav.name
        except Exception:
            try:
                os.unlink(tmp_wav.name)
            except Exception:
                pass
            raise


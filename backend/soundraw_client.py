"""
Soundraw API client for generating rap beats
"""
import httpx
import os
from typing import Dict, Optional, List
from enum import Enum


class Mood(Enum):
    """Beat moods for rap music"""
    AGGRESSIVE = "aggressive"
    CHILL = "chill"
    DARK = "dark"
    ENERGETIC = "energetic"
    HAPPY = "happy"
    INTENSE = "intense"
    MELANCHOLIC = "melancholic"
    PARTY = "party"
    RELAXED = "relaxed"
    SAD = "sad"


class Tempo(Enum):
    """Tempo ranges for beats"""
    SLOW = (60, 90)
    MEDIUM = (90, 120)
    FAST = (120, 160)
    VERY_FAST = (160, 200)


class SoundrawClient:
    """Client for interacting with Soundraw API"""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("SOUNDRAW_API_KEY")
        self.api_url = (api_url or os.getenv("SOUNDRAW_API_URL", "https://api.soundraw.io")).rstrip("/")
        
        if not self.api_key:
            raise ValueError("SOUNDRAW_API_KEY is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_beat(
        self,
        mood: str = "energetic",
        tempo: int = 120,
        genre: str = "hip-hop",
        length: int = 30,
        energy: Optional[str] = None,
        instruments: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate a rap beat using Soundraw API
        
        Args:
            mood: Mood of the beat (aggressive, chill, dark, energetic, etc.)
            tempo: BPM (beats per minute) - typically 60-200
            genre: Music genre (hip-hop, trap, etc.)
            length: Length in seconds (typically 15-60)
            energy: Energy level (low, medium, high)
            instruments: List of preferred instruments
        
        Returns:
            Dict with beat information including download URL
        """
        payload = {
            "mood": mood,
            "tempo": tempo,
            "genre": genre,
            "length": length
        }
        
        if energy:
            payload["energy"] = energy
        
        if instruments:
            payload["instruments"] = instruments
        
        async with httpx.AsyncClient() as client:
            try:
                # Note: Actual Soundraw API endpoint may vary
                # This is a template based on typical music generation APIs
                response = await client.post(
                    f"{self.api_url}/v1/music/generate",
                    json=payload,
                    headers=self.headers,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Soundraw API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                raise Exception(f"Failed to generate beat: {str(e)}")
    
    async def search_beats(
        self,
        mood: Optional[str] = None,
        genre: Optional[str] = None,
        tempo_min: Optional[int] = None,
        tempo_max: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search for existing beats
        
        Args:
            mood: Filter by mood
            genre: Filter by genre
            tempo_min: Minimum BPM
            tempo_max: Maximum BPM
            limit: Maximum results to return
        
        Returns:
            List of beat dictionaries
        """
        params = {"limit": limit}
        
        if mood:
            params["mood"] = mood
        if genre:
            params["genre"] = genre
        if tempo_min:
            params["tempo_min"] = tempo_min
        if tempo_max:
            params["tempo_max"] = tempo_max
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.api_url}/v1/music/search",
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json().get("results", [])
            except httpx.HTTPStatusError as e:
                raise Exception(f"Soundraw API error: {e.response.status_code}")
            except Exception as e:
                raise Exception(f"Failed to search beats: {str(e)}")
    
    def parse_user_preferences(self, user_input: str) -> Dict:
        """
        Parse user's spoken preferences into beat parameters
        This is a helper method - in production, use NLP/AI to extract this
        
        Args:
            user_input: User's spoken description of desired beat
        
        Returns:
            Dict with parsed preferences
        """
        user_lower = user_input.lower()
        
        # Extract mood
        mood = "energetic"  # default
        for m in Mood:
            if m.value in user_lower:
                mood = m.value
                break
        
        # Extract tempo hints
        tempo = 120  # default
        if "slow" in user_lower or "chill" in user_lower:
            tempo = 80
        elif "fast" in user_lower or "upbeat" in user_lower:
            tempo = 140
        elif "medium" in user_lower:
            tempo = 110
        
        # Extract genre hints
        genre = "hip-hop"
        if "trap" in user_lower:
            genre = "trap"
        elif "drill" in user_lower:
            genre = "drill"
        
        return {
            "mood": mood,
            "tempo": tempo,
            "genre": genre
        }


"""
AI Agent for conversational beat creation
"""
import os
from typing import Dict, List, Optional
from openai import OpenAI


class BeatCreationAgent:
    """AI agent that guides users through creating rap beats via voice"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        self.system_prompt = """You are a friendly and creative AI assistant that helps rappers create the perfect beats for their music using Soundraw.

Your role:
1. Greet users warmly and understand what kind of rap beat they want
2. Ask about their preferences: mood, tempo, energy level, style
3. Guide them through the beat creation process conversationally
4. Extract key information: mood (aggressive, chill, dark, energetic, happy, intense, melancholic, party, relaxed, sad), tempo (BPM), genre (hip-hop, trap, drill, etc.)
5. Confirm their choices before generating
6. Be enthusiastic about rap music and help them express their creative vision

Keep responses:
- Short and conversational (for voice calls)
- Clear and easy to understand
- Encouraging and creative
- Focused on extracting beat preferences

When you have enough information, summarize what you'll create and ask for confirmation."""
    
    def __init_conversation(self, user_id: str) -> List[Dict]:
        """Initialize conversation history for a user"""
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "assistant", "content": "Hey! I'm your beat creation assistant. I'm here to help you create the perfect rap beat using Soundraw. What kind of vibe are you going for? Are you looking for something aggressive, chill, energetic, or something else?"}
        ]
    
    async def process_message(
        self,
        user_message: str,
        user_id: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Process user message and return AI response
        
        Args:
            user_message: User's spoken message
            user_id: Unique user identifier
            conversation_history: Previous conversation messages
        
        Returns:
            Dict with response and extracted preferences (if ready)
        """
        if conversation_history is None:
            conversation_history = self.__init_conversation(user_id)
        
        # Add user message
        conversation_history.append({"role": "user", "content": user_message})
        
        # Get AI response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation_history,
                temperature=0.8,
                max_tokens=200  # Keep responses short for voice
            )
            
            ai_response = response.choices[0].message.content
            
            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Check if we have enough info to generate (simple heuristic)
            ready_to_generate = self._check_if_ready(conversation_history)
            
            # Extract preferences if ready
            preferences = None
            if ready_to_generate:
                preferences = self._extract_preferences(conversation_history)
            
            return {
                "response": ai_response,
                "conversation_history": conversation_history,
                "ready_to_generate": ready_to_generate,
                "preferences": preferences
            }
        except Exception as e:
            return {
                "response": "Sorry, I'm having trouble right now. Could you try again?",
                "conversation_history": conversation_history,
                "ready_to_generate": False,
                "preferences": None,
                "error": str(e)
            }
    
    def _check_if_ready(self, conversation_history: List[Dict]) -> bool:
        """Check if we have enough information to generate a beat"""
        # Simple heuristic: check if mood and tempo are mentioned
        full_text = " ".join([msg["content"] for msg in conversation_history]).lower()
        
        moods = ["aggressive", "chill", "dark", "energetic", "happy", "intense", 
                 "melancholic", "party", "relaxed", "sad"]
        mood_mentioned = any(mood in full_text for mood in moods)
        
        tempo_indicators = ["tempo", "bpm", "slow", "fast", "speed", "pace"]
        tempo_mentioned = any(indicator in full_text for indicator in tempo_indicators)
        
        # Also check for confirmation phrases
        confirmation_phrases = ["yes", "sounds good", "that's right", "correct", "generate", "create", "make it"]
        confirmed = any(phrase in full_text for phrase in confirmation_phrases)
        
        return (mood_mentioned and tempo_mentioned) or confirmed
    
    def _extract_preferences(self, conversation_history: List[Dict]) -> Dict:
        """Extract beat preferences from conversation"""
        full_text = " ".join([msg["content"] for msg in conversation_history]).lower()
        
        # Extract mood
        mood = "energetic"  # default
        moods = {
            "aggressive": "aggressive",
            "chill": "chill",
            "dark": "dark",
            "energetic": "energetic",
            "happy": "happy",
            "intense": "intense",
            "melancholic": "melancholic",
            "party": "party",
            "relaxed": "relaxed",
            "sad": "sad"
        }
        for key, value in moods.items():
            if key in full_text:
                mood = value
                break
        
        # Extract tempo
        tempo = 120  # default
        if "slow" in full_text or "chill" in full_text:
            tempo = 80
        elif "fast" in full_text or "upbeat" in full_text:
            tempo = 140
        elif "medium" in full_text:
            tempo = 110
        
        # Extract genre
        genre = "hip-hop"
        if "trap" in full_text:
            genre = "trap"
        elif "drill" in full_text:
            genre = "drill"
        
        return {
            "mood": mood,
            "tempo": tempo,
            "genre": genre,
            "length": 30  # default 30 seconds
        }


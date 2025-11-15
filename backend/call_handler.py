"""
Twilio voice call handlers for inbound and outbound calls
"""
import os
from twilio.twiml.voice_response import VoiceResponse, Gather
from typing import Dict, Optional
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioException


class CallHandler:
    """Handles Twilio voice calls for beat creation"""
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        if self.account_sid and self.auth_token:
            self.twilio_client = TwilioClient(self.account_sid, self.auth_token)
        else:
            self.twilio_client = None
    
    def handle_inbound_call(self, from_number: str, call_sid: str) -> str:
        """
        Handle inbound call - user calling the bot
        
        Args:
            from_number: Caller's phone number
            call_sid: Twilio call SID
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Greet the caller
        response.say(
            "Hey! Welcome to the Rap Beat Creator. I'm here to help you create the perfect beat for your rap music using Soundraw. Let's get started!",
            voice="alice",
            language="en-US"
        )
        
        # Gather user input
        gather = Gather(
            input="speech",
            action=f"/api/voice/process-speech?call_sid={call_sid}&from={from_number}",
            method="POST",
            speech_timeout="auto",
            language="en-US",
            hints="aggressive, chill, dark, energetic, happy, intense, melancholic, party, relaxed, sad, slow, fast, tempo, BPM, trap, drill, hip-hop"
        )
        gather.say(
            "Tell me what kind of beat you're looking for. What's the mood? How fast should it be?",
            voice="alice"
        )
        response.append(gather)
        
        # Fallback if no input
        response.say(
            "I didn't catch that. Please call back and tell me about the beat you want to create.",
            voice="alice"
        )
        response.hangup()
        
        return str(response)
    
    def handle_speech_input(
        self,
        speech_result: str,
        call_sid: str,
        from_number: str,
        conversation_state: Optional[Dict] = None
    ) -> str:
        """
        Process speech input from user
        
        Args:
            speech_result: Transcribed speech from user
            call_sid: Twilio call SID
            from_number: Caller's phone number
            conversation_state: Current conversation state
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # This will be processed by the main API endpoint
        # For now, we'll use a simple response
        response.say(
            f"I heard you say: {speech_result}. Let me process that and help you create your beat.",
            voice="alice"
        )
        
        # Redirect to continue conversation
        gather = Gather(
            input="speech",
            action=f"/api/voice/process-speech?call_sid={call_sid}&from={from_number}",
            method="POST",
            speech_timeout="auto",
            language="en-US"
        )
        gather.say(
            "Tell me more about what you want, or say 'generate' when you're ready to create the beat.",
            voice="alice"
        )
        response.append(gather)
        
        return str(response)
    
    def make_outbound_call(
        self,
        to_number: str,
        webhook_url: str,
        message: Optional[str] = None
    ) -> Dict:
        """
        Make an outbound call to a user
        
        Args:
            to_number: Phone number to call (E.164 format)
            webhook_url: URL to handle the call
            message: Optional message to play
        
        Returns:
            Dict with call information
        """
        if not self.twilio_client:
            raise Exception("Twilio client not initialized. Check credentials.")
        
        try:
            call = self.twilio_client.calls.create(
                to=to_number,
                from_=self.phone_number,
                url=webhook_url,
                method="POST"
            )
            
            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "to": to_number
            }
        except TwilioException as e:
            return {
                "success": False,
                "error": str(e),
                "to": to_number
            }
    
    def generate_beat_ready_response(self, beat_url: Optional[str] = None) -> str:
        """
        Generate TwiML response when beat is ready
        
        Args:
            beat_url: URL to download the beat (optional)
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        if beat_url:
            response.say(
                "Great news! Your beat is ready. I'll send you a link to download it via text message. Thanks for using the Rap Beat Creator!",
                voice="alice"
            )
        else:
            response.say(
                "Your beat is being generated. You'll receive a text message with the download link shortly. Thanks for using the Rap Beat Creator!",
                voice="alice"
            )
        
        response.hangup()
        return str(response)
    
    def send_sms(self, to_number: str, message: str) -> Dict:
        """
        Send SMS message (e.g., with beat download link)
        
        Args:
            to_number: Phone number to send to (E.164 format)
            message: Message content
        
        Returns:
            Dict with message information
        """
        if not self.twilio_client:
            raise Exception("Twilio client not initialized. Check credentials.")
        
        try:
            message = self.twilio_client.messages.create(
                to=to_number,
                from_=self.phone_number,
                body=message
            )
            
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
        except TwilioException as e:
            return {
                "success": False,
                "error": str(e)
            }


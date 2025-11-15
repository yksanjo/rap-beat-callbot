"""
FastAPI backend for Rap Beat Call Bot
Handles inbound/outbound calls and beat generation via Soundraw
"""
from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import os
import uuid
from datetime import datetime
from twilio.twiml.voice_response import VoiceResponse, Gather

from call_handler import CallHandler
from ai_agent import BeatCreationAgent
from soundraw_client import SoundrawClient

app = FastAPI(title="Rap Beat Call Bot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
call_handler = CallHandler()
ai_agent = BeatCreationAgent()
soundraw_client = SoundrawClient()

# In-memory storage for conversation states (use Redis/DB in production)
conversation_states: Dict[str, Dict] = {}


class OutboundCallRequest(BaseModel):
    phone_number: str
    message: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "Rap Beat Call Bot API",
        "status": "running",
        "endpoints": {
            "inbound_call": "/api/voice/inbound",
            "outbound_call": "/api/calls/outbound",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "twilio": call_handler.twilio_client is not None,
            "openai": ai_agent.client is not None,
            "soundraw": soundraw_client.api_key is not None
        }
    }


@app.post("/api/voice/inbound")
async def handle_inbound_call(request: Request):
    """
    Handle inbound call from Twilio
    Twilio will POST to this endpoint when a call comes in
    """
    form_data = await request.form()
    from_number = form_data.get("From", "")
    call_sid = form_data.get("CallSid", "")
    
    # Initialize conversation state
    if call_sid not in conversation_states:
        conversation_states[call_sid] = {
            "call_sid": call_sid,
            "from_number": from_number,
            "conversation_history": None,
            "preferences": None,
            "beat_generated": False,
            "created_at": datetime.now().isoformat()
        }
    
    # Generate TwiML response
    twiml = call_handler.handle_inbound_call(from_number, call_sid)
    return Response(content=twiml, media_type="application/xml")


@app.post("/api/voice/process-speech")
async def process_speech(request: Request):
    """
    Process speech input from user during call
    """
    form_data = await request.form()
    speech_result = form_data.get("SpeechResult", "")
    call_sid = form_data.get("call_sid", form_data.get("CallSid", ""))
    from_number = form_data.get("from", form_data.get("From", ""))
    
    if not call_sid:
        return Response(
            content='<?xml version="1.0" encoding="UTF-8"?><Response><Say>Error: No call ID</Say><Hangup/></Response>',
            media_type="application/xml"
        )
    
    # Get or create conversation state
    if call_sid not in conversation_states:
        conversation_states[call_sid] = {
            "call_sid": call_sid,
            "from_number": from_number,
            "conversation_history": None,
            "preferences": None,
            "beat_generated": False,
            "created_at": datetime.now().isoformat()
        }
    
    state = conversation_states[call_sid]
    
    # Process with AI agent
    try:
        result = await ai_agent.process_message(
            user_message=speech_result,
            user_id=call_sid,
            conversation_history=state["conversation_history"]
        )
        
        # Update conversation state
        state["conversation_history"] = result["conversation_history"]
        
        # Check if ready to generate beat
        if result["ready_to_generate"] and result["preferences"]:
            state["preferences"] = result["preferences"]
            
            # Generate beat
            try:
                beat_result = await soundraw_client.generate_beat(**result["preferences"])
                state["beat_generated"] = True
                state["beat_url"] = beat_result.get("url", "")
                state["beat_id"] = beat_result.get("id", "")
                
                # Send SMS with download link
                if state["beat_url"]:
                    sms_message = f"Your rap beat is ready! Download it here: {state['beat_url']}"
                    call_handler.send_sms(from_number, sms_message)
                
                # Return success response
                twiml = call_handler.generate_beat_ready_response(state["beat_url"])
                return Response(content=twiml, media_type="application/xml")
            except Exception as e:
                # Beat generation failed
                response = VoiceResponse()
                response.say(
                    f"Sorry, I had trouble generating your beat. Error: {str(e)}. Let's try again.",
                    voice="alice"
                )
                gather = Gather(
                    input="speech",
                    action=f"/api/voice/process-speech?call_sid={call_sid}&from={from_number}",
                    method="POST",
                    speech_timeout="auto"
                )
                gather.say("Tell me about your beat again.", voice="alice")
                response.append(gather)
                return Response(content=str(response), media_type="application/xml")
        
        # Continue conversation
        ai_response = result["response"]
        response = VoiceResponse()
        response.say(ai_response, voice="alice")
        
        gather = Gather(
            input="speech",
            action=f"/api/voice/process-speech?call_sid={call_sid}&from={from_number}",
            method="POST",
            speech_timeout="auto",
            language="en-US"
        )
        gather.say("What else would you like to tell me?", voice="alice")
        response.append(gather)
        
        return Response(content=str(response), media_type="application/xml")
    
    except Exception as e:
        # Error handling
        response = VoiceResponse()
        response.say(
            "Sorry, I'm having trouble understanding. Could you repeat that?",
            voice="alice"
        )
        gather = Gather(
            input="speech",
            action=f"/api/voice/process-speech?call_sid={call_sid}&from={from_number}",
            method="POST",
            speech_timeout="auto"
        )
        response.append(gather)
        return Response(content=str(response), media_type="application/xml")


@app.post("/api/calls/outbound")
async def make_outbound_call(request: OutboundCallRequest):
    """
    Initiate an outbound call to a user
    """
    webhook_url = os.getenv("WEBHOOK_URL", "http://localhost:8000/api/voice/inbound")
    
    result = call_handler.make_outbound_call(
        to_number=request.phone_number,
        webhook_url=webhook_url,
        message=request.message
    )
    
    if result["success"]:
        return {
            "success": True,
            "call_sid": result["call_sid"],
            "status": result["status"],
            "message": "Call initiated successfully"
        }
    else:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to make call"))


@app.get("/api/conversations/{call_sid}")
async def get_conversation_state(call_sid: str):
    """Get conversation state for a call"""
    if call_sid not in conversation_states:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation_states[call_sid]


@app.get("/api/conversations")
async def list_conversations():
    """List all active conversations"""
    return {
        "conversations": list(conversation_states.keys()),
        "count": len(conversation_states)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


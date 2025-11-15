# Rap Beat Call Bot - Project Summary

## Overview

A complete voice-enabled AI call bot system that helps rappers create custom beats using Soundraw API. The bot supports both inbound (users call in) and outbound (bot calls users) calling scenarios.

## Project Structure

```
rap-beat-callbot/
├── backend/
│   ├── main.py              # FastAPI server with all endpoints
│   ├── call_handler.py      # Twilio voice call handling
│   ├── ai_agent.py          # OpenAI-powered conversational agent
│   └── soundraw_client.py   # Soundraw API integration
├── config/                  # Configuration files (if needed)
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick start guide
├── test_outbound.py        # Test script for outbound calls
├── test_api.py             # API endpoint tests
└── .gitignore             # Git ignore rules
```

## Key Components

### 1. Call Handler (`backend/call_handler.py`)
- Handles Twilio voice calls (inbound/outbound)
- Generates TwiML responses
- Manages call flow and speech input
- Sends SMS notifications

### 2. AI Agent (`backend/ai_agent.py`)
- Uses OpenAI GPT models for natural conversation
- Extracts user preferences (mood, tempo, genre)
- Guides users through beat creation process
- Determines when enough info is collected

### 3. Soundraw Client (`backend/soundraw_client.py`)
- Integrates with Soundraw API for beat generation
- Supports various moods, tempos, and genres
- Handles API requests and responses
- Parses user preferences into API parameters

### 4. Main API (`backend/main.py`)
- FastAPI server with all endpoints
- Handles webhooks from Twilio
- Manages conversation states
- Orchestrates beat generation flow

## Features

✅ **Inbound Calls**: Users can call a phone number to create beats
✅ **Outbound Calls**: Bot can proactively call users
✅ **Voice Recognition**: Uses Twilio's speech recognition
✅ **AI Conversation**: Natural language understanding via OpenAI
✅ **Beat Generation**: Creates custom beats via Soundraw API
✅ **SMS Delivery**: Sends download links via text message
✅ **Conversation Tracking**: Maintains state during calls

## Technology Stack

- **Backend**: FastAPI (Python)
- **Voice**: Twilio Voice API
- **AI**: OpenAI GPT models
- **Music**: Soundraw API
- **Deployment**: Docker, Railway, Render compatible

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/api/voice/inbound` | POST | Twilio inbound call webhook |
| `/api/voice/process-speech` | POST | Process user speech input |
| `/api/calls/outbound` | POST | Initiate outbound call |
| `/api/conversations` | GET | List all conversations |
| `/api/conversations/{call_sid}` | GET | Get conversation state |

## Conversation Flow

1. **Call Initiated** (inbound or outbound)
2. **Bot Greeting** - Welcomes user and explains service
3. **Preference Collection** - Asks about mood, tempo, style
4. **Confirmation** - Summarizes preferences
5. **Beat Generation** - Calls Soundraw API
6. **Delivery** - Sends SMS with download link
7. **Call End** - Thanks user and hangs up

## Configuration Required

1. **Twilio Account**
   - Account SID
   - Auth Token
   - Phone number with voice capabilities

2. **OpenAI Account**
   - API Key
   - Model selection (default: gpt-4o-mini)

3. **Soundraw Account**
   - API Key
   - API endpoint URL

## Important Notes

⚠️ **Soundraw API**: The actual Soundraw API endpoints and authentication method may vary. You may need to:
- Check Soundraw's official API documentation
- Adjust endpoints in `soundraw_client.py`
- Verify authentication method
- Test API integration

⚠️ **Production Considerations**:
- Replace in-memory conversation storage with Redis/PostgreSQL
- Add proper error handling and retries
- Implement rate limiting
- Add logging and monitoring
- Set up proper security measures

## Testing

```bash
# Test API endpoints
python test_api.py

# Test outbound call
python test_outbound.py +1234567890

# Test health
curl http://localhost:8000/health
```

## Deployment

The project is ready for deployment on:
- **Railway**: Use `railway up`
- **Render**: Configure as web service
- **Docker**: Use provided Dockerfile
- **Any Python hosting**: Standard FastAPI deployment

## Next Steps

1. Get API keys (Twilio, OpenAI, Soundraw)
2. Configure `.env` file
3. Test locally with ngrok
4. Deploy to production
5. Customize AI prompts and beat options
6. Add database for conversation storage
7. Implement additional features (beat preview, favorites, etc.)

## License

MIT


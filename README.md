# Rap Beat Call Bot 🎵📞

A voice-enabled AI call bot that helps rappers create custom beats using Soundraw API. Supports both **inbound** (users call in) and **outbound** (bot calls users) calling.

## Features

- 🎤 **Voice Interaction**: Natural conversation via phone calls
- 🎵 **Beat Generation**: Creates custom rap beats using Soundraw API
- 📞 **Inbound Calls**: Users can call a number to create beats
- 📲 **Outbound Calls**: Bot can proactively call users
- 🤖 **AI Agent**: GPT-powered conversational assistant
- 📱 **SMS Delivery**: Sends beat download links via text message

## Architecture

```
User Phone Call
    ↓
Twilio Voice API
    ↓
FastAPI Backend
    ├── AI Agent (OpenAI) → Understands user preferences
    ├── Soundraw Client → Generates beats
    └── Call Handler → Manages call flow
    ↓
Beat Generated → SMS with Download Link
```

## Prerequisites

1. **Twilio Account**
   - Sign up at https://www.twilio.com
   - Get a phone number with voice capabilities
   - Get Account SID and Auth Token

2. **OpenAI API Key**
   - Sign up at https://platform.openai.com
   - Get an API key

3. **Soundraw API Key**
   - Sign up at https://soundraw.io
   - Get API access (check their documentation for API availability)

4. **Python 3.9+**

## Installation

1. **Clone and navigate to the project:**
```bash
cd rap-beat-callbot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Configure `.env` file:**
```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Soundraw API Configuration
SOUNDRAW_API_KEY=your_soundraw_api_key
SOUNDRAW_API_URL=https://api.soundraw.io

# Server Configuration
SERVER_URL=http://localhost:8000
WEBHOOK_URL=https://your-domain.com  # Use ngrok for local testing
```

## Running Locally

1. **Start the server:**
```bash
cd backend
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Expose your local server (for Twilio webhooks):**
```bash
# Install ngrok: https://ngrok.com
ngrok http 8000
```

3. **Update Twilio webhook:**
   - Go to Twilio Console → Phone Numbers → Manage → Active Numbers
   - Select your phone number
   - Set Voice webhook URL to: `https://your-ngrok-url.ngrok.io/api/voice/inbound`
   - Save

## Usage

### Inbound Calls (User Calls Bot)

1. Call your Twilio phone number
2. Bot greets you and asks about your beat preferences
3. Describe what you want:
   - Mood: "aggressive", "chill", "energetic", etc.
   - Tempo: "slow", "fast", "medium", or specific BPM
   - Style: "trap", "drill", "hip-hop", etc.
4. Bot confirms and generates your beat
5. Receive SMS with download link

### Outbound Calls (Bot Calls User)

Make a POST request to initiate a call:

```bash
curl -X POST http://localhost:8000/api/calls/outbound \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890"
  }'
```

Or use Python:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/calls/outbound",
    json={"phone_number": "+1234567890"}
)
print(response.json())
```

## API Endpoints

### Health Check
```
GET /health
```

### Inbound Call Webhook (Twilio)
```
POST /api/voice/inbound
```

### Process Speech Input
```
POST /api/voice/process-speech
```

### Make Outbound Call
```
POST /api/calls/outbound
Body: {"phone_number": "+1234567890"}
```

### Get Conversation State
```
GET /api/conversations/{call_sid}
```

### List All Conversations
```
GET /api/conversations
```

## Example Conversation Flow

**Bot:** "Hey! Welcome to the Rap Beat Creator. I'm here to help you create the perfect beat for your rap music using Soundraw. Let's get started! Tell me what kind of beat you're looking for. What's the mood? How fast should it be?"

**User:** "I want something aggressive and fast, like trap music"

**Bot:** "Got it! So you want an aggressive trap beat with a fast tempo. What BPM are you thinking? Around 140-150?"

**User:** "Yeah, around 140"

**Bot:** "Perfect! I'll create an aggressive trap beat at 140 BPM. Should I generate it now?"

**User:** "Yes, generate it"

**Bot:** "Great news! Your beat is ready. I'll send you a link to download it via text message. Thanks for using the Rap Beat Creator!"

*[SMS sent with download link]*

## Configuration

### Beat Generation Options

The bot supports these parameters:

- **Moods**: aggressive, chill, dark, energetic, happy, intense, melancholic, party, relaxed, sad
- **Tempo**: 60-200 BPM (beats per minute)
- **Genres**: hip-hop, trap, drill
- **Length**: 15-60 seconds (default: 30)

### AI Agent Customization

Edit `backend/ai_agent.py` to customize:
- System prompt
- Response style
- Preference extraction logic

## Deployment

### Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Add environment variables in Railway dashboard
5. Deploy: `railway up`

### Render

1. Create new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Production Considerations

1. **Database**: Replace in-memory `conversation_states` with Redis or PostgreSQL
2. **Error Handling**: Add retry logic and better error messages
3. **Rate Limiting**: Implement rate limits for API calls
4. **Logging**: Add structured logging (e.g., with Loguru)
5. **Monitoring**: Set up monitoring and alerts
6. **Security**: Validate phone numbers, sanitize inputs
7. **Soundraw API**: Verify actual API endpoints and authentication method

## Troubleshooting

### Twilio Webhook Not Working
- Ensure ngrok is running and URL is accessible
- Check Twilio webhook URL is set correctly
- Verify webhook URL is HTTPS (required by Twilio)

### Soundraw API Errors
- Verify API key is correct
- Check Soundraw API documentation for actual endpoints
- Ensure API key has proper permissions

### OpenAI API Errors
- Verify API key is valid
- Check API quota/limits
- Ensure model name is correct

## License

MIT

## Contributing

Contributions welcome! Please open an issue or pull request.

## Support

For issues or questions:
- Check Twilio documentation: https://www.twilio.com/docs
- Check Soundraw API docs: https://soundraw.io (check for API documentation)
- Check OpenAI docs: https://platform.openai.com/docs


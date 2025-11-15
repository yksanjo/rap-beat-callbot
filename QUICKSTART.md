# Quick Start Guide 🚀

Get your Rap Beat Call Bot running in 5 minutes!

## Step 1: Get API Keys (5 min)

1. **Twilio** (Free trial with $15.50 credit):
   - Sign up: https://www.twilio.com/try-twilio
   - Get phone number: Console → Phone Numbers → Buy a Number
   - Copy Account SID and Auth Token from dashboard

2. **OpenAI** (Pay as you go):
   - Sign up: https://platform.openai.com
   - Create API key: API Keys → Create new secret key
   - Copy the key (starts with `sk-`)

3. **Soundraw** (Check their website):
   - Visit: https://soundraw.io
   - Sign up and check for API access
   - Get API key if available
   - **Note**: If Soundraw API is not publicly available, you may need to contact them or use an alternative music generation API

## Step 2: Install & Configure (2 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your keys
nano .env  # or use your favorite editor
```

Fill in your `.env`:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
SOUNDRAW_API_KEY=your_soundraw_key
```

## Step 3: Run Server (1 min)

```bash
cd backend
python main.py
```

Server runs on `http://localhost:8000`

## Step 4: Expose with ngrok (2 min)

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

## Step 5: Configure Twilio Webhook (2 min)

1. Go to Twilio Console → Phone Numbers → Manage → Active Numbers
2. Click your phone number
3. Under "Voice & Fax", set:
   - **A CALL COMES IN**: `https://abc123.ngrok.io/api/voice/inbound`
   - Method: `HTTP POST`
4. Save

## Step 6: Test! 🎉

**Test Inbound Call:**
1. Call your Twilio phone number
2. Say: "I want an aggressive trap beat, fast tempo"
3. Follow the conversation
4. Check your phone for SMS with download link

**Test Outbound Call:**
```bash
curl -X POST http://localhost:8000/api/calls/outbound \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

## Troubleshooting

**"Twilio webhook error"**
- Make sure ngrok is running
- Use HTTPS URL (not HTTP)
- Check webhook URL in Twilio console

**"OpenAI API error"**
- Verify API key is correct
- Check you have credits/quota

**"Soundraw API error"**
- Verify API key
- Check if Soundraw API is available
- May need to adjust API endpoint in `soundraw_client.py`

## Next Steps

- Customize the AI agent prompts in `backend/ai_agent.py`
- Add more beat generation options
- Deploy to production (Railway, Render, etc.)
- Add database for conversation storage

Happy beat making! 🎵


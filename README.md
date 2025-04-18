# Telegram Bot with Streamlit Dashboard

A Telegram bot powered by Mistral AI, with a Streamlit dashboard for monitoring.

## Deployment Steps

1. Fork this repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy this app
5. Add your secrets in Streamlit Cloud:
   - TELEGRAM_BOT_TOKEN

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a .env file with:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

3. Run locally:
```bash
streamlit run streamlit_app.py
```

## Features

- Natural language conversation using GPT
- Maintains conversation context
- Handles various message types

## Usage

1. Start a chat with your bot on Telegram
2. Send any message to start a conversation
3. The bot will respond using GPT's capabilities 

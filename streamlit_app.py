import streamlit as st
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
from threading import Thread
import sys

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="Telegram Bot Status", page_icon="🤖")

# Initialize session state
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False

st.title("Telegram Bot Status Dashboard")

# Function to run the bot
async def run_telegram_bot():
    try:
        from bot import main
        await main()
    except Exception as e:
        st.error(f"Bot Error: {str(e)}")
        st.session_state.bot_running = False

def start_bot_thread():
    asyncio.run(run_telegram_bot())

# Add control buttons
col1, col2 = st.columns([1, 3])
with col1:
    if not st.session_state.bot_running:
        if st.button("Start Bot"):
            try:
                st.session_state.bot_running = True
                thread = Thread(target=start_bot_thread)
                thread.start()
                st.success("Starting bot...")
            except Exception as e:
                st.error(f"Failed to start bot: {str(e)}")
                st.session_state.bot_running = False
    else:
        st.success("Bot is running! 🚀")

# Display bot information
st.markdown("""
### Bot Information
- Platform: Streamlit Cloud
- Status: Active
- Framework: python-telegram-bot
""")

# Display bot token status (safely)
token = os.getenv('TELEGRAM_BOT_TOKEN')
if token:
    st.sidebar.success("✅ Bot Token configured")
else:
    st.sidebar.error("❌ Bot Token missing")

# Add usage instructions
st.markdown("""
### Usage Instructions
1. Click 'Start Bot' to activate the bot
2. Open Telegram and search for your bot
3. Start chatting!

### Monitor
- Check the status above to ensure the bot is running
- View any errors or issues in the sidebar
""")

# Display activity log
st.sidebar.markdown("### Activity Log")
if st.session_state.bot_running:
    st.sidebar.info("Bot is active and responding to messages") 

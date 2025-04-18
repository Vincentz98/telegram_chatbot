import streamlit as st
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import threading

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="Telegram Bot Status", page_icon="🤖")

# Initialize session state
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
    st.session_state.bot_thread = None

def run_bot():
    """Run the bot in a separate thread"""
    async def start_bot():
        try:
            from bot import main
            await main()
        except Exception as e:
            st.error(f"Bot Error: {str(e)}")

    asyncio.run(start_bot())

st.title("Telegram Bot Status Dashboard")

# Add control buttons
if not st.session_state.bot_running:
    if st.button("Start Bot"):
        st.session_state.bot_running = True
        st.session_state.bot_thread = threading.Thread(target=run_bot)
        st.session_state.bot_thread.start()
        st.experimental_rerun()
else:
    st.success("Bot is running! 🚀")
    if st.button("Stop Bot"):
        st.session_state.bot_running = False
        if st.session_state.bot_thread:
            # Note: This is a simple stop implementation
            st.session_state.bot_thread = None
        st.experimental_rerun()

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
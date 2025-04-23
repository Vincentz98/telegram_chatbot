import streamlit as st
import os
from threading import Thread
import asyncio
from bot import main  # assuming main() in bot.py is your async bot function

st.set_page_config(page_title="Telegram Bot Status", page_icon="🤖")
st.title("Telegram Bot Status Dashboard")

status_file = "bot_status.txt"
if os.path.exists(status_file):
    with open(status_file, "r") as f:
        status = f.read().strip()
else:
    status = "unknown"

# Display current status
if status == "running":
    st.success("✅ Bot is running!")
elif status == "stopped":
    st.error("❌ Bot is stopped.")
else:
    st.warning("❓ Bot status unknown.")

# Start bot from Streamlit
def start_bot_thread():
    asyncio.run(main())  # run the Telegram bot async main

if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

if st.button("Start Bot") and not st.session_state.bot_running:
    st.session_state.bot_running = True
    Thread(target=start_bot_thread).start()
    st.success("🚀 Starting bot... Refresh to check status.")

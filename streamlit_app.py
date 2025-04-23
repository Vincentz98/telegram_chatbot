import streamlit as st
import os

st.set_page_config(page_title="Telegram Bot Status", page_icon="🤖")
st.title("Telegram Bot Status Dashboard")

# Check status from file
status_file = "bot_status.txt"
if os.path.exists(status_file):
    with open(status_file, "r") as f:
        status = f.read().strip()
else:
    status = "unknown"

if status == "running":
    st.success("✅ Bot is running!")
elif status == "stopped":
    st.error("❌ Bot is stopped.")
else:
    st.warning("❓ Bot status unknown.")

st.markdown("""
### Instructions
- Start your bot using `python bot.py` in a separate terminal.
- Refresh this dashboard to see its current status.
""")

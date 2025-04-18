import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary to store conversation history
conversation_history = {}

OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Default Ollama API endpoint

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        f"I'm your AI chat companion powered by Ollama. I can help you with:\n"
        f"• Questions and explanations\n"
        f"• Writing and analysis\n"
        f"• General conversation\n\n"
        f"Feel free to ask me anything!"
    )
    # Initialize conversation history for new users
    conversation_history[user.id] = []

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
Here's how to use me:
• Just send any message to start chatting
• Use /start to restart our conversation
• Use /clear to clear chat history
• Use /help to see this message again

I can help with:
• Answering questions
• Explaining concepts
• Writing assistance
• General conversation
    """
    await update.message.reply_text(help_text)

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the conversation history for the user."""
    user = update.effective_user
    conversation_history[user.id] = []
    await update.message.reply_text("Conversation history has been cleared! 🧹")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and generate responses using Ollama."""
    user = update.effective_user
    message_text = update.message.text

    # Initialize conversation history for new users
    if user.id not in conversation_history:
        conversation_history[user.id] = []

    try:
        # Prepare the messages format for Ollama
        messages = [
            {"role": "system", "content": """You are a helpful and knowledgeable AI assistant. 
            When explaining complex topics:
            1. Break them down into simple, understandable parts
            2. Use concrete examples when possible
            3. Be thorough but clear
            4. If relevant, provide practical applications or next steps
            5. If you're not certain about something, acknowledge it"""}
        ]
        
        # Add conversation history
        for msg in conversation_history[user.id][-5:]:  # Last 5 messages for context
            messages.append({
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({"role": "user", "content": message_text})

        # Make request to Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "mistral",
                "messages": messages,
                "stream": False
            }
        )
        
        response.raise_for_status()  # Raise exception for bad status codes
        ai_response = response.json()["message"]["content"]

        # Send the response
        await update.message.reply_text(ai_response)

        # Update conversation history
        conversation_history[user.id].extend([
            {"role": "user", "content": message_text},
            {"role": "assistant", "content": ai_response}
        ])

        # Limit conversation history
        if len(conversation_history[user.id]) > 10:
            conversation_history[user.id] = conversation_history[user.id][-10:]

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        await update.message.reply_text(
            "I apologize, but I encountered an error. Please try again or use /start to restart our conversation."
        )

async def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_history))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 

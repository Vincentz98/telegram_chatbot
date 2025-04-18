import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests  # For Ollama API calls

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
        f"Hi {user.mention_html()}! I'm your AI chat companion powered by Ollama. I provide detailed, accurate responses to your questions. Feel free to start a conversation!"
    )
    conversation_history[user.id] = []

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
I can help you with:
- Detailed explanations of complex topics
- Programming and technical questions
- General knowledge queries
- Writing and analysis

Commands:
/start - Start a new conversation
/help - Show this help message
/clear - Clear conversation history
    """
    await update.message.reply_text(help_text)

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the conversation history for the user."""
    user = update.effective_user
    conversation_history[user.id] = []
    await update.message.reply_text("Conversation history has been cleared!")

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
                "model": "mistral",  # You can change this to other models like "llama2" or "deepseek-coder"
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

        # Limit conversation history to last 10 messages (5 exchanges)
        if len(conversation_history[user.id]) > 10:
            conversation_history[user.id] = conversation_history[user.id][-10:]

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        await update.message.reply_text(
            "I apologize, but I encountered an error while processing your message. Please try again."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_history))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
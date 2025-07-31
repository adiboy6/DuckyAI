import os
import traceback
from typing import List, Dict, AsyncGenerator, Tuple
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def converse_sync(prompt: str, messages: List[Dict[str, str]],
    max_tokens: int = 1600,
    model=None) -> Tuple[str, List[Dict[str, str]]]:
    """
    Synchronous conversation using Gemini API
    """
    # Add the user's message to the list of messages
    if messages is None:
        messages = []

    messages.append({"role": "user", "content": prompt})

    try:
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            if msg["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [msg["content"]]})
            elif msg["role"] == "system":
                # Add system message as user message at the beginning
                gemini_messages.insert(0, {"role": "user", "parts": [f"System: {msg['content']}"]})

        # Create chat session
        chat = gemini_model.start_chat(history=gemini_messages[:-1] if len(gemini_messages) > 1 else [])
        
        # Get response
        response = chat.send_message(prompt)
        response_text = response.text

        # Add the assistant's message to the list of messages
        messages.append({"role": "assistant", "content": response_text})

        return response_text, messages

    except Exception as e:
        print(f"❌ GEMINI ERROR: {str(e)}")
        error_msg = f"GEMINI_EXCEPTION {str(e)}"
        messages.append({"role": "assistant", "content": error_msg})
        return error_msg, messages

async def converse(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Asynchronous conversation using Gemini API
    """
    try:
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            if msg["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [msg["content"]]})
            elif msg["role"] == "system":
                # Add system message as user message at the beginning
                gemini_messages.insert(0, {"role": "user", "parts": [f"System: {msg['content']}"]})

        # Create chat session
        chat = gemini_model.start_chat(history=gemini_messages)
        
        # Get the last user message
        last_user_message = None
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        if last_user_message:
            # Get response
            response = chat.send_message(last_user_message)
            response_text = response.text
            
            # Yield response in chunks (simulate streaming)
            words = response_text.split()
            for word in words:
                yield word + " "
        else:
            yield "No user message found"

    except Exception as e:
        print(f"❌ GEMINI ERROR: {str(e)}")
        yield f"GEMINI_EXCEPTION {str(e)}"

def create_conversation_starter(user_prompt: str) -> List[Dict[str, str]]:
    """
    Given a user prompt, create a conversation history with the following format:
    `[ { "role": "user", "content": user_prompt } ]`

    :param user_prompt: a user prompt string
    :return: a conversation history
    """
    return [{"role": "user", "content": user_prompt}] 
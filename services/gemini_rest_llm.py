import os
import json
import requests
import traceback
from typing import List, Dict, AsyncGenerator, Tuple
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gemini REST API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def converse_sync(prompt: str, messages: List[Dict[str, str]],
    max_tokens: int = 1600,
    model=None) -> Tuple[str, List[Dict[str, str]]]:
    """
    Synchronous conversation using Gemini REST API
    """
    # Add the user's message to the list of messages
    if messages is None:
        messages = []

    messages.append({"role": "user", "content": prompt})

    try:
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # Make the API call
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': GEMINI_API_KEY
        }

        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            
            # Add the assistant's message to the list of messages
            messages.append({"role": "assistant", "content": response_text})
            
            return response_text, messages
        else:
            error_msg = f"GEMINI_REST_ERROR: HTTP {response.status_code} - {response.text}"
            messages.append({"role": "assistant", "content": error_msg})
            return error_msg, messages

    except Exception as e:
        print(f"❌ GEMINI REST ERROR: {str(e)}")
        error_msg = f"GEMINI_REST_EXCEPTION {str(e)}"
        messages.append({"role": "assistant", "content": error_msg})
        return error_msg, messages

async def converse(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Asynchronous conversation using Gemini REST API
    """
    try:
        # Get the last user message
        last_user_message = None
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        if not last_user_message:
            yield "No user message found"
            return

        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": last_user_message
                        }
                    ]
                }
            ]
        }

        # Make the API call
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': GEMINI_API_KEY
        }

        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            
            # Yield response in chunks (simulate streaming)
            words = response_text.split()
            for word in words:
                yield word + " "
        else:
            error_msg = f"GEMINI_REST_ERROR: HTTP {response.status_code} - {response.text}"
            yield error_msg

    except Exception as e:
        print(f"❌ GEMINI REST ERROR: {str(e)}")
        yield f"GEMINI_REST_EXCEPTION {str(e)}"

def create_conversation_starter(user_prompt: str) -> List[Dict[str, str]]:
    """
    Given a user prompt, create a conversation history with the following format:
    `[ { "role": "user", "content": user_prompt } ]`

    :param user_prompt: a user prompt string
    :return: a conversation history
    """
    return [{"role": "user", "content": user_prompt}] 
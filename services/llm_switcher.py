import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check which service to use
USE_GEMINI = os.getenv('USE_GEMINI', 'false').lower() == 'true'

if USE_GEMINI:
    try:
        from services.gemini_llm import converse_sync, converse, create_conversation_starter
        print("🔧 Using Gemini API")
    except ImportError:
        print("❌ Gemini service not available, falling back to OpenAI")
        from services.llm import converse_sync, converse, create_conversation_starter
else:
    from services.llm import converse_sync, converse, create_conversation_starter
    print("�� Using OpenAI API") 
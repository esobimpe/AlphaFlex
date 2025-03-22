import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()


ENCODED_API_KEY = "OFF3S0xiNFhyVWYyZlBMQWQ1OHBDeUhIT0t1QjNoVFg="
BASE_URL = "https://financialmodelingprep.com/api/v3"

def decode_api_key(encoded_key):
    """Decode the encoded API key."""
    try:
        return base64.b64decode(encoded_key).decode('utf-8')
    except Exception:
        return None

def get_api_key():
    """
    Get the API key with the following priority:
    1. Environment variable if set by user
    2. Built-in encoded API key as fallback
    """
    # First try to get from environment
    env_key = os.getenv('ALPHAFLEX_API_KEY')
    if env_key and env_key != "your_api_key_here":
        return env_key
    
    # Fallback to built-in encoded key
    decoded_key = decode_api_key(ENCODED_API_KEY)
    if decoded_key:
        return decoded_key
        
    raise ValueError(
        "Could not initialize API key. If you want to use your own API key, "
        "please set it in the ALPHAFLEX_API_KEY environment variable or in a .env file."
    ) 
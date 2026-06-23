import logging
import requests
import time
from app.core.config import settings

logger = logging.getLogger(__name__)

# Sequenced list of models to try. We prioritize models that have verified success on the user's API key.
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash"
]

def generate_content_with_fallback(prompt: str, temperature: float = 0.0) -> str:
    """
    Queries Gemini API using a sequenced fallback pool of models.
    Implements a brief retry loop for transient status codes (429 rate limiting, 503 service unavailable).
    """
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured in settings.")
        
    last_error_msg = ""
    
    # Try each model in our pool sequentially
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature
            }
        }
        
        # Retry up to 2 times per model if hitting transient issues
        for attempt in range(2):
            try:
                logger.info(f"Attempting Gemini generation using model {model} (attempt {attempt + 1})...")
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    res_json = response.json()
                    try:
                        text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                        logger.info(f"Successfully generated content using model {model}.")
                        return text
                    except (KeyError, IndexError) as parse_err:
                        logger.error(f"Failed to parse response structure for model {model}: {parse_err}")
                        last_error_msg = f"Malformed JSON structure from model {model}."
                        break # Not transient, try next model
                        
                elif response.status_code in (429, 503):
                    last_error_msg = f"Model {model} returned status code {response.status_code}: {response.text}"
                    logger.warning(f"Transient error from model {model} (status code {response.status_code}). Retrying in 1s...")
                    time.sleep(1.0)
                    continue
                else:
                    last_error_msg = f"Model {model} returned status code {response.status_code}: {response.text}"
                    logger.warning(f"Error from model {model} (status code {response.status_code}). Trying next model...")
                    break # Not transient, try next model
                    
            except Exception as e:
                last_error_msg = f"Request to model {model} failed: {str(e)}"
                logger.error(f"Exception during request to model {model}: {e}")
                time.sleep(0.5)
                continue
                
    raise RuntimeError(f"All Gemini models in the fallback pool failed. Last error: {last_error_msg}")

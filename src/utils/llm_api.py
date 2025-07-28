
import requests
from tqdm import tqdm

def call_llm(prompt: str, temperature: float, top_p: float, max_tokens: int, api_url: str, lora_name: str = None) -> str:
    """Sends a prompt to the LLM API and returns the content of the response."""
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
    if lora_name:
        payload['lora_name'] = lora_name
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["message"]['content'].strip()
    except requests.exceptions.RequestException as e:
        tqdm.write(f"API call failed: {e}")
        return "" 
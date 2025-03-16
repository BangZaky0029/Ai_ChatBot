import requests
import json
from ..config.ai_config import API_KEY, API_URL

def get_ai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "google/gemma-3-4b-it:free",  # Updated model name
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 150
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 401:
            return "Error: Invalid API key. Please check your OpenRouter API configuration."
        
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "No response generated from AI"
            
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to AI service: {str(e)}"
    except Exception as e:
        return f"Error processing AI response: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    response = get_ai_response(prompt)
    print("AI Response:", response)
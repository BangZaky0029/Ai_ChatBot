import requests
import json

def get_ai_response(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek/deepseek-r1-zero:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )
        
        response.raise_for_status()  # Raise exception for bad status codes
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "No response from AI"
            
    except requests.exceptions.RequestException as e:
        return f"Error making request: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error parsing response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    response = get_ai_response(prompt)
    print("AI Response:", response)
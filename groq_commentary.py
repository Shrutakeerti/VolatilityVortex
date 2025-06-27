import requests

def get_groq_commentary(prompt, api_key): # func to get commentary 
    url = "https://api.groq.com/openai/v1/chat/completions" # Groq API endpoint 
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7 # adjusted this temp
    }

    try: # Made the API call
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]: # choices if exist
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Unexpected GROQ API response: {result}")
            return "No valid response from GROQ."

    except requests.exceptions.RequestException as e: # handle the request
        print(f"GROQ API call failed: {e}")
        return "GROQ API call failed."

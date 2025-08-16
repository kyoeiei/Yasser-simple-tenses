from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Get the Chutes.ai API key from environment variables
CHUTES_API_KEY = os.getenv('CHUTES_API_KEY')
CHUTES_API_URL = "https://llm.chutes.ai/v1/chat/completions"

# Thai AI configuration
THAI_AI_CONFIGS = {
    "present_simple": {
        "name": "Present Simple Tense Checker (Thai)",
        "description": "Check and improve Present Simple tense usage in Thai",
        "system_prompt": """คุณเป็นผู้ช่วยสอนภาษาอังกฤษที่พูดภาษาไทย คุณจะตอบกลับเป็นภาษาไทย คุณจะให้คำแนะนำเพื่อปรับปรุงแต่ไม่ให้คำตอบที่ถูกต้องโดยตรง จะตรวจ Present Simple tense เท่านั้น คุณจะไฮไลท์คำที่ผิดโดยใช้ **คำที่ผิด** และไม่ให้คำตอบโดยตรงให้แค่ให้แนะนำ จงตอบกลับเป็นภาษาไทยเท่านั้นเสมอ ไม่ให้ตัวอย่างด้วย"""
    },
    "past_simple": {
        "name": "Past Simple Tense Checker (Thai)",
        "description": "Check and improve Past Simple tense usage in Thai",
        "system_prompt": """คุณเป็นผู้ช่วยสอนภาษาอังกฤษที่พูดภาษาไทย คุณจะตอบกลับเป็นภาษาไทย คุณจะให้คำแนะนำเพื่อปรับปรุงแต่ไม่ให้คำตอบที่ถูกต้องโดยตรง จะตรวจ Past Simple tense เท่านั้น คุณจะไฮไลท์คำที่ผิดโดยใช้ **คำที่ผิด** และไม่ให้คำตอบโดยตรงให้แค่ให้แนะนำ จงตอบกลับเป็นภาษาไทยเท่านั้นเสมอ ไม่ให้ตัวอย่างด้วย"""
    },
    "future_simple": {
        "name": "Future Simple Tense Checker (Thai)",
        "description": "Check and improve Future Simple tense usage in Thai",
        "system_prompt": """คุณเป็นผู้ช่วยสอนภาษาอังกฤษที่พูดภาษาไทย คุณจะตอบกลับเป็นภาษาไทย คุณจะให้คำแนะนำเพื่อปรับปรุงแต่ไม่ให้คำตอบที่ถูกต้องโดยตรง จะตรวจ Future Simple tense เท่านั้น คุณจะไฮไลท์คำที่ผิดโดยใช้ **คำที่ผิด** และไม่ให้คำตอบโดยตรงให้แค่ให้แนะนำ จงตอบกลับเป็นภาษาไทยเท่านั้นเสมอ ไม่ให้ตัวอย่างด้วย"""
    }
}

# Define the 3 different AIs with their system prompts for simple tenses
AI_CONFIGS = {
    "present_simple": {
        "name": "Present Simple Tense Checker",
        "description": "Check and improve Present Simple tense usage",
        "system_prompt": """[system note: "You are an assistant that analyzes user text for correct use of the Present Simple tense.

If the text is correct, confirm it.

If there are mistakes, highlight them in bold (e.g., wrong_word) and give only hints about the issue (e.g., 'Consider checking the verb form.').

Do NOT provide the correct answer or rewrite their text.

Do NOT give examples.

Your role is to guide, not solve: point out errors, suggest what to think about, and encourage the user to find the fix on their own."]"""
    },
    "past_simple": {
        "name": "Past Simple Tense Checker",
        "description": "Check and improve Past Simple tense usage",
        "system_prompt": """[system note: You are a helpful assistant checking Past Simple tense inside user text. Do not give direct answers unless asked. Communicate with the user, review their text, and return grammar suggestions only. Highlight mistakes in bold using double asterisks (e.g., wrong_word). Give hints, not exact corrections (e.g., "Consider a more accurate verb. Hint:"). Your goal is to help the user think, not solve for them. You focus on Past Simple grammar and vocabulary.if they already correct then tell them that.don't give example]"""
    },
    "future_simple": {
        "name": "Future Simple Tense Checker",
        "description": "Check and improve Future Simple tense usage",
        "system_prompt": """[system note: You are a helpful assistant checking Future Simple tense inside user text. Do not give direct answers unless asked. Communicate with the user, review their text, and return grammar suggestions only. Highlight mistakes in bold using double asterisks (e.g., wrong_word). Give hints, not exact corrections (e.g., "Consider a more accurate verb. Hint:").Your goal is to help the user think, not solve for them. You focus on Future Simple grammar and vocabulary.if they already correct then tell them that.don't give example]"""
    }
}

app = Flask(__name__)

def call_chutes_api(message, ai_type="present_simple"):
    """
    Make a call to the Chutes.ai chat completions API using DeepSeek-V3-0324
    """
    if not CHUTES_API_KEY:
        return "Error: Chutes.ai API key not found. Please set it in your .env file."

    # Get the system prompt for the selected AI
    ai_config = AI_CONFIGS.get(ai_type, AI_CONFIGS["present_simple"])
    system_prompt = ai_config["system_prompt"]

    headers = {
        "Authorization": f"Bearer {CHUTES_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        payload = {
            "model": "deepseek-ai/DeepSeek-R1-0528",
            "messages": messages,
            "stream": False,
            "max_tokens": 0,
            "temperature": 0.7
        }

        print("Sending request with payload:", payload)  # Debug print
        response = requests.post(
            CHUTES_API_URL,
            headers=headers,
            json=payload
        )
        print("Response status:", response.status_code)  # Debug print
        print("Response content:", response.text)  # Debug print

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('choices') and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            return "No response content from API"
        else:
            error_message = f"Error: API returned status code {response.status_code}"
            try:
                error_detail = response.json()
                error_message += f"\nDetails: {error_detail}"
            except:
                pass
            print("Error response:", error_message)  # Debug print
            return error_message

    except requests.exceptions.RequestException as e:
        return f"Error connecting to Chutes.ai API: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html', ai_configs=AI_CONFIGS)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    ai_type = data.get('aiType', 'present_simple')  # Get selected AI type

    # Call the Chutes.ai API with the selected AI type
    response = call_chutes_api(user_message, ai_type)
    
    return jsonify({'response': response})

@app.route('/ai-configs', methods=['GET'])
def get_ai_configs():
    """Return the AI configurations for the frontend"""
    return jsonify(AI_CONFIGS)

@app.route('/translate', methods=['POST'])
def generate_thai_response():
    """Generate a new Thai response using the same user message and Thai AI system prompt"""
    data = request.json
    user_message = data.get('text', '')
    ai_type = data.get('aiType', 'present_simple')
    
    if not user_message:
        return jsonify({'error': 'No text provided'}), 400
    
    if not CHUTES_API_KEY:
        return jsonify({'error': 'Chutes.ai API key not found. Please set it in your .env file.'}), 500
    
    try:
        headers = {
            "Authorization": f"Bearer {CHUTES_API_KEY}",
            "Content-Type": "application/json"
        }

        # Get the Thai AI system prompt for the selected AI type
        thai_ai_config = THAI_AI_CONFIGS.get(ai_type, THAI_AI_CONFIGS["present_simple"])
        thai_system_prompt = thai_ai_config["system_prompt"]

        messages = [
            {"role": "system", "content": thai_system_prompt},
            {"role": "user", "content": user_message}
        ]

        payload = {
            "model": "deepseek-ai/DeepSeek-V3-0324",
            "messages": messages,
            "stream": False,
            "max_tokens": 0,
            "temperature": 0.7
        }

        response = requests.post(
            CHUTES_API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('choices') and len(response_data['choices']) > 0:
                thai_response = response_data['choices'][0]['message']['content']
                return jsonify({'translated_text': thai_response})
            else:
                return jsonify({'error': 'Thai response generation failed - no response content'}), 500
        else:
            error_message = f"Thai AI API error: {response.status_code}"
            try:
                error_detail = response.json()
                error_message += f"\nDetails: {error_detail}"
            except:
                pass
            return jsonify({'error': error_message}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Thai AI request failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)





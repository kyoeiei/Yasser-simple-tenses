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
        "system_prompt": """"You are a helpful assistant with purpose of to check the grammar (Present simple tense) of the text provided by the user and YOU WILL NOT GIVE THEM DIRECT ANSWER unless being asked by the user. you WILL and ALWAYS speak in THAI and not English or any other language, your speciality is that you will speaks and replying to user in THAI but you can understand english. you can communicate with the user. You will be given a text and you will need to check the grammar (Present simple tense) of the text and return the text with the grammar errors SUGGESTIONS. You will give the user of what they could maybe change into but do not give them the word/sentence that can change (example:  "Consider using a more precise phrase. Hint:") . YOU WILL NOT GIVE DIRECT CORRECT ANSWER BUT GIVE THE USER A HINT INSTEAD AND YOUR PURPOSE IS TO HELP USER THINK BUT YOU CAN ALSO GIVE THE USER HINTS WHEN THEY ASK FOR SPECIFIC WORDS IN THE TEXT AND ONLY GIVE THE USER HINTS ONLY HINTS IF YOU ARE GIVING THE USER HINTS DO NOT GIVE THE REAL ANSWERS BUT GIVE THE USER HINTS TO THE REAL ANSWER INSTEAD.When highlighting incorrect words, you should put them in bold using double asterisks (e.g., incorrect_word). You will give out words in the text that are not correct and not giving direct answer and give hint instead, with the hint sentence are being bold text. The system will have the knowledge of writing and will able to help the user with the vocabulary and grammar.You will be honest with the user responds. You will tell the user that they are correct IF they are correct."""
    },
    "past_simple": {
        "name": "Past Simple Tense Checker (Thai)",
        "description": "Check and improve Past Simple tense usage in Thai",
        "system_prompt": """คุณเป็นผู้ช่วยที่เป็นประโยชน์ในการตรวจสอบ Past Simple tense ในข้อความของผู้ใช้ คุณจะพูด เฉพาะภาษาไทยเท่านั้น และจะตอบกลับเป็นภาษาไทยเสมอ อย่าให้คำตอบโดยตรง เว้นแต่ถูกถาม จงสื่อสารกับผู้ใช้ ตรวจสอบข้อความของพวกเขา และให้คำแนะนำด้านไวยากรณ์เท่านั้น เน้นจุดผิดพลาดด้วยการทำตัวหนาโดยใช้ดอกจันคู่ (เช่น wrong_word) ให้คำใบ้ ไม่ใช่คำแก้ที่ถูกต้องตรงๆ (เช่น "ลองใช้คำกริยาที่ถูกต้องมากขึ้น คำใบ้:") เป้าหมายของคุณคือช่วยให้ผู้ใช้คิดเอง ไม่ใช่แก้แทน คุณมุ่งเน้นไปที่ไวยากรณ์และคำศัพท์ของ Past Simple หากถูกต้องแล้วให้บอกว่าถูกต้องแล้ว อย่าให้ตัวอย่าง"""
    },
    "future_simple": {
        "name": "Future Simple Tense Checker (Thai)",
        "description": "Check and improve Future Simple tense usage in Thai",
        "system_prompt": """คุณเป็นผู้ช่วยที่เป็นประโยชน์ในการตรวจสอบ Future Simple tense ในข้อความของผู้ใช้ คุณจะพูด เฉพาะภาษาไทยเท่านั้น และจะตอบกลับเป็นภาษาไทยเสมอ อย่าให้คำตอบโดยตรง เว้นแต่ถูกถาม จงสื่อสารกับผู้ใช้ ตรวจสอบข้อความของพวกเขา และให้คำแนะนำด้านไวยากรณ์เท่านั้น เน้นจุดผิดพลาดด้วยการทำตัวหนาโดยใช้ดอกจันคู่ (เช่น wrong_word) ให้คำใบ้ ไม่ใช่คำแก้ที่ถูกต้องตรงๆ (เช่น "ลองใช้คำกริยาที่ถูกต้องมากขึ้น คำใบ้:") เป้าหมายของคุณคือช่วยให้ผู้ใช้คิดเอง ไม่ใช่แก้แทน คุณมุ่งเน้นไปที่ไวยากรณ์และคำศัพท์ของ Future Simple หากถูกต้องแล้วให้บอกว่าถูกต้องแล้ว อย่าให้ตัวอย่าง"""
    }
}

# Define the 3 different AIs with their system prompts for simple tenses
AI_CONFIGS = {
    "present_simple": {
        "name": "Present Simple Tense Checker",
        "description": "Check and improve Present Simple tense usage",
        "system_prompt": """[system note: "You are a helpful assistant with purpose of to check the grammar of Present simple tense of the text provided by the user and YOU WILL NOT GIVE THEM DIRECT ANSWER unless being asked by the user. you can communicate with the user. You will be given a text and you will need to check the grammar of Present simple tense of the text and return the text with the grammar errors SUGGESTIONS. You will give the user of what they could maybe change into but do not give them the word/sentence that can change (example:  "Consider using a more precise phrase. Hint:") . YOU WILL NOT GIVE DIRECT CORRECT ANSWER BUT GIVE THE USER A HINT INSTEAD AND YOUR PURPOSE IS TO HELP USER THINK BUT YOU CAN ALSO GIVE THE USER HINTS WHEN THEY ASK FOR SPECIFIC WORDS IN THE TEXT AND ONLY GIVE THE USER HINTS ONLY HINTS IF YOU ARE GIVING THE USER HINTS DO NOT GIVE THE REAL ANSWERS BUT GIVE THE USER HINTS TO THE REAL ANSWER INSTEAD.When highlighting incorrect words, you should put them in bold using double asterisks (e.g., incorrect_word). You will give out words in the text that are not correct and not giving direct answer and give hint instead, with the hint sentence are being bold text. The system will have the knowledge of writing and will able to help the user with the vocabulary and grammar.You will be honest with the user responds. You will tell the user that they are correct IF they are correct]"""
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
            "model": "tngtech/DeepSeek-TNG-R1T2-Chimera",
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
            "model": "tngtech/DeepSeek-TNG-R1T2-Chimera",
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





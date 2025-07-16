from flask import request, jsonify
from . import chat_bp
from sarvamai import SarvamAI
from app import csrf
from dotenv import load_dotenv
import os

load_dotenv()

client = SarvamAI(api_subscription_key=os.getenv('SARVAM_API_KEY'))

@csrf.exempt
@chat_bp.route('', methods=['POST'])
def ai_chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({'error': 'Empty message!'}), 400
    
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
        
        response = client.chat.completions(messages=messages)
        reply = response.choices[0].message.content
        
        return jsonify({'response': reply})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
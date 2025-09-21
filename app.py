# app.py
from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'chatbot-secret-key-123')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get conversation history from session
        if 'conversation' not in session:
            session['conversation'] = []
        
        # Add user message to conversation
        session['conversation'].append({"role": "user", "content": user_message})
        
        # Build conversation messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": """You are a senior project management consultant with expertise in all major methodologies. Your goal is to recommend the best project management approach based on specific project characteristics.

METHODOLOGIES TO CONSIDER:
- Agile/Scrum: Iterative, flexible, good for uncertain requirements
- Kanban: Continuous flow, visual workflow, good for maintenance
- Waterfall: Sequential, structured, good for fixed requirements
- Lean: Waste reduction, efficiency focus
- Hybrid: Combination approaches
- DevOps: Development and operations integration

GATHER INFORMATION ABOUT:
1. Team size and experience level
2. Project timeline and deadlines
3. Requirements clarity and change frequency
4. Stakeholder involvement level
5. Project complexity and risk
6. Industry/domain constraints

RESPONSE STYLE:
- Ask follow-up questions if you need more information
- Be specific in recommendations
- Explain WHY your recommendation fits
- Suggest implementation tips
- Keep responses conversational but professional
- If you have enough information, provide a detailed recommendation with reasoning"""
            }
        ]
        
        # Add conversation history
        messages.extend(session['conversation'])
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=600,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Add AI response to conversation
        session['conversation'].append({"role": "assistant", "content": ai_response})
        
        # Limit conversation history to last 10 exchanges
        if len(session['conversation']) > 20:
            session['conversation'] = session['conversation'][-20:]
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
    
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'error': 'I apologize, but I encountered an error. Please try again.',
            'status': 'error'
        }), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Conversation reset'})

if __name__ == '__main__':
    app.run(debug=True)
# app.py
from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'chatbot-secret-key-123')

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

@app.route('/')
def home():
    """Main chat interface"""
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with OpenAI API"""
    try:
        # Validate OpenAI client
        if not client:
            return jsonify({
                'error': 'OpenAI service is not available. Please check your API key.',
                'status': 'error'
            }), 500
        
        # Get and validate user message
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Please enter a message'}), 400
        
        if len(user_message) > 1000:
            return jsonify({'error': 'Message too long. Please keep under 1000 characters.'}), 400
        
        # Initialize conversation history
        if 'conversation' not in session:
            session['conversation'] = []
        
        # Add user message to conversation
        session['conversation'].append({"role": "user", "content": user_message})
        
        # Build system prompt and conversation
        system_prompt = """You are a senior project management consultant with expertise in all major methodologies. Your goal is to recommend the best project management approach based on specific project characteristics.

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

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(session['conversation'])
        
        # Call OpenAI API with timeout and error handling
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=600,
            temperature=0.7,
            timeout=30
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Validate response
        if not ai_response:
            return jsonify({
                'error': 'Received empty response. Please try again.',
                'status': 'error'
            }), 500
        
        # Add AI response to conversation
        session['conversation'].append({"role": "assistant", "content": ai_response})
        
        # Limit conversation history to prevent token overflow
        if len(session['conversation']) > 20:
            session['conversation'] = session['conversation'][-20:]
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        
        # Different error messages for different types of errors
        if "rate limit" in str(e).lower():
            error_msg = "Too many requests. Please wait a moment and try again."
        elif "api key" in str(e).lower():
            error_msg = "API key issue. Please contact support."
        elif "timeout" in str(e).lower():
            error_msg = "Request timed out. Please try again."
        else:
            error_msg = "I apologize, but I encountered an error. Please try again."
        
        return jsonify({
            'error': error_msg,
            'status': 'error'
        }), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    try:
        session.clear()
        return jsonify({'status': 'success', 'message': 'Conversation reset'})
    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to reset'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'openai_available': client is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Note: The following function/code snippet/lines was/were generated with the assistance of AI tools.
# I have thoroughly reviewed the code and confirm that I understand its logic, can explain its behaviour, and am capable of modifying it as needed.
# app.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Basic route to test if Flask is working
@app.route('/')
def home():
    return "<h1>Chatbot Project Setup Complete!</h1><p>Flask is running successfully!</p>"

# Test route to check if environment variables are loaded
@app.route('/test')
def test():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return f"<h2>Environment setup working!</h2><p>API key loaded: {api_key[:10]}...</p>"
    else:
        return "<h2>Environment setup issue!</h2><p>API key not found</p>"

# Chat endpoint that communicates with OpenAI
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user message from request
        user_message = request.json.get('message', '')
        
        # Validate input
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Call OpenAI API using new client format
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that recommends project management methodologies based on project characteristics. Keep responses concise and practical."
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the AI response
        ai_response = response.choices[0].message.content.strip()
        
        # Return JSON response
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
    
    except Exception as e:
        # Handle errors 
        app.logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
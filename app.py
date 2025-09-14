# app.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
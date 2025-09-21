# Project Methodology Advisor Chatbot

AI-powered chatbot that recommends project management methodologies based on project characteristics using OpenAI GPT-3.5.

## Features

- Interactive chat interface
- Conversation memory
- Smart methodology recommendations
- Error handling and validation
- Responsive design
- Reset conversation functionality

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chatbot-methodology-advisor.git
cd chatbot-methodology-advisor
```

2. Create virtual environment:
```bash
python -m venv chatbot_env
chatbot_env\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
```

5. Run the application:
```bash
python app.py
```
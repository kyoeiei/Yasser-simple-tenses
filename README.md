# Web-based Chatbot

A simple web-based chatbot built with Flask, ready for chutes.ai API integration.

## Setup Instructions

1. Make sure you have Python 3.7+ installed on your system.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory (optional, for API keys):
```
CHUTES_API_KEY=your_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Features

- Modern web interface with real-time chat functionality
- Ready for chutes.ai API integration
- Responsive design
- Support for both click and Enter key message sending
- **Translation to Thai**: Click the "แปลเป็นไทย" button on any AI response to translate it to Thai
- Multiple AI models for different English tenses (Present Simple, Past Simple, Future Simple)

## Adding chutes.ai Integration

To integrate with chutes.ai API:
1. Add your API key to the `.env` file
2. Modify the `/chat` route in `app.py` to make API calls to chutes.ai
3. Update the response handling as needed

## Thai Response Generation Feature

The application includes a feature that generates new AI responses in Thai using specialized Thai AI models for each tense type.

### Thai AI Setup
The Thai response generation uses the same Chutes.ai API key as the main application. No additional setup is required if you already have the `CHUTES_API_KEY` configured.

### How Thai Response Generation Works
1. Uses specialized Thai AI models with Thai system prompts for each tense type
2. Generates completely new responses in Thai based on the user's original message
3. Maintains the same educational approach and grammar checking functionality
4. Provides natural, fluent Thai responses with proper Thai grammar and vocabulary
5. Preserves formatting like bold text (**text**) for highlighting errors

### How to Use Thai Response Generation
1. Send a message to any of the AI models (Present Simple, Past Simple, Future Simple)
2. When you receive an English response, click the "แปลเป็นไทย" (Generate Thai Response) button
3. A new Thai response will be generated and displayed below the original English response
4. The Thai response will provide the same grammar checking and suggestions in Thai

## Project Structure

- `app.py` - Main Flask application
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file) 
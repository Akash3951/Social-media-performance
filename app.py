from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configuration constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def run_flow(message: str) -> dict:
    """Run a flow with a given message"""
    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat"
        }
        headers = {
            "Authorization": f"Bearer {APPLICATION_TOKEN}",
            "Content-Type": "application/json"
        }

        # Send POST request to LangFlow API
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during LangFlow API request: {e}")
        return {"error": "Failed to connect to LangFlow API"}

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle incoming questions and get responses from LangFlow"""
    try:
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({"error": "No question provided"}), 400
        # handle case
        if question.lower() == 'hi':
            return jsonify({"message": "Hello, how can I assist you!"})

        # Get response from LangFlow
        response = run_flow(message=question)

        # Debug log
        logging.debug(f"LangFlow Response: {response}")

        # Extract 'message' field from the response
        message = (
            response.get('outputs', [{}])[0]
            .get('outputs', [{}])[0]
            .get('results', {})
            .get('message', {})
            .get('text', 'Sorry, Something went wrong Please try again later !.')
        )

        return jsonify({"message": message})
    except Exception as e:
        logging.error(f"Error in /ask route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

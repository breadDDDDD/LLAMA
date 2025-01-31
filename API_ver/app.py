from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)  

url = os.getenv("url_req")
headers = {
    'Content-Type': 'application/json',
}

@app.route('/chat', methods=['POST'])
    
def chat():

    data = request.get_json()
    prompt = data.get("message", "")
    
    def generate_response(prompt):
        conversation_history = []
        conversation_history.append(prompt)

        full_prompt = "\n".join(conversation_history)

        data = {
            "model": "sharkboo",
            "stream": False,
            "prompt": full_prompt,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            conversation_history.append(actual_response)
            return actual_response
        else:
            print("Error:", response.status_code, response.text)
            return None
    return jsonify({"response" : generate_response(prompt)})


if __name__ == '__main__':
    app.run(debug=True)
    
    

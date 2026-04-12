from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({"answer": "Hello! This is a test response from chat endpoint."}), 200

@app.route('/api/test', methods=['POST'])
def test():
    return jsonify({"answer": "Hello! This is a test response from test endpoint."}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
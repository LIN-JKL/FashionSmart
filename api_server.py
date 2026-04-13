from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Hello World"})

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query', '')
        return jsonify({"answer": f"收到：{query}"})
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
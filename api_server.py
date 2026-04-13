from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "FashionSmart API", "status": "running"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if data and 'query' in data:
            return jsonify({"answer": f"收到：{data['query']}"})
        return jsonify({"error": "需要query参数"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
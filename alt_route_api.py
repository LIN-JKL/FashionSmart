from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 启用CORS

@app.route('/api/message', methods=['POST'])
def message():
    try:
        logger.info('Received POST request to /api/message')
        return jsonify({"answer": "Hello from alternate route API!"})
    except Exception as e:
        logger.error(f'Error: {e}')
        return jsonify({"answer": "Error occurred"}), 500

@app.route('/api/health', methods=['GET'])
def health():
    try:
        logger.info('Received GET request to /api/health')
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f'Error: {e}')
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f'Starting server on port {port}')
    app.run(host='0.0.0.0', port=port, debug=True)
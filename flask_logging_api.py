from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 启用CORS

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        logger.info('Received POST request to /api/chat')
        logger.info(f'Headers: {dict(request.headers)}')
        
        # 尝试读取请求体
        if request.is_json:
            data = request.get_json()
            logger.info(f'Request data: {data}')
        else:
            logger.info('Request is not JSON')
            data = request.get_data()
            logger.info(f'Request data: {data}')
        
        logger.info('Sending response')
        return jsonify({"answer": "Hello from Flask logging API!"})
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
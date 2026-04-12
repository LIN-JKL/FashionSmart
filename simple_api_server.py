from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        app.logger.info('Health check endpoint called')
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        app.logger.error(f'Error in health_check: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        app.logger.info('Chat endpoint called')
        # 检查请求方法
        app.logger.info(f'Request method: {request.method}')
        # 检查请求头
        app.logger.info(f'Request headers: {dict(request.headers)}')
        # 检查请求数据
        app.logger.info(f'Request data: {request.data}')
        
        data = request.get_json()
        app.logger.info(f'Parsed JSON: {data}')
        
        if not data or 'query' not in data:
            app.logger.error('Missing query parameter')
            return jsonify({"error": "Missing query parameter"}), 400
        
        query = data['query']
        app.logger.info(f'Processing query: {query}')
        
        response = jsonify({"answer": f"Hello! You asked: {query}"})
        app.logger.info(f'Response: {response.get_json()}')
        return response, 200
    except Exception as e:
        app.logger.error(f'Error in chat endpoint: {str(e)}')
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
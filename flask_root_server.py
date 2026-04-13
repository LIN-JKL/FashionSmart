from flask import Flask, request, jsonify
import sys
import os

# 打印Python版本和环境信息
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables: {dict(os.environ)}")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    print(f"Request method: {request.method}")
    print(f"Request path: {request.path}")
    print(f"Request headers: {dict(request.headers)}")
    
    if request.method == 'POST':
        print(f"Request data: {request.data}")
        return jsonify({"message": "POST request received"})
    else:
        return jsonify({"message": "GET request received"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
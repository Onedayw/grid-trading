import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Access environment variables
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

@app.route('/')
def hello_world():
    return f"Hello, Azure! Running in {app.config['ENV']} mode."

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return '<p>Hello, World!<p>'

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable CORS for all routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, POST')
    return response

@app.route('/process_data', methods=['OPTIONS', 'POST'])
def process_data():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    received_data = data.get('data', [])
    for item in received_data:
        print(item)
    # Process data
    updated_data = [7, 8, 9]

    return jsonify({'message': 'Data processed successfully', 'updatedData': updated_data})

if __name__ == '__main__':
    app.run(debug=True)
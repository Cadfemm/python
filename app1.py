from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/print_number', methods=['POST'])
def print_number():
    try:
        # Get the number from the JSON payload
        data = request.json
        number = data.get('number')

        # Print the number on the server
        print(f"Received number from React.js: {number}")

        return jsonify({'message': 'Number received successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)

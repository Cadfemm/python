from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)

@app.route('/print_data ', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        received_data = data.get('data', [])

        # Convert received data to DataFrame
        df = pd.DataFrame({'Column1': received_data})

        # Process df as needed
        print(f"Received number from React.js: {2}")
        return jsonify({'message': 'Data received successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
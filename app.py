from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import numpy as np
import warnings

app = Flask(__name__)
CORS(app)

# Suppress warnings for version mismatches
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Function to load model safely
def load_model(file_path):
    try:
        with open(file_path, 'rb') as file:
            model_metadata = pickle.load(file)
        if not isinstance(model_metadata, dict):
            raise ValueError("The loaded model is not in the expected dictionary format.")
        return model_metadata
    except ValueError as ve:
        print(f"ValueError while loading model from {file_path}: {str(ve)}")
        raise RuntimeError(
            f"Model {file_path} is incompatible with the current scikit-learn version. "
            f"Consider upgrading scikit-learn to match the model version or retrain the model."
        )
    except Exception as e:
        print(f"Error loading model from {file_path}: {str(e)}")
        raise

# Load model5 with metadata
try:
    model_metadata = load_model('model/Right_Lower_Limb_Model (5).pkl')
    pipeline = model_metadata['pipeline']  # Trained model pipeline
    bins = model_metadata['bins']  # Age bins for bucketing
    labels = model_metadata['labels']  # Corresponding labels for Age bins
    columns = model_metadata['columns']  # Expected column structure
except Exception as e:
    print(f"Unexpected error during model loading: {e}")
    raise

# Function to preprocess input data
def preprocess_input_data(input_data):
    """
    Preprocess the input data according to the model requirements.
    """
    try:
        # Convert input data to a DataFrame
        input_df = pd.DataFrame([input_data])
# Ensure numeric fields are converted to proper data types
        numeric_fields = ['Age', 'Days of treatment', 
                          'Initial Right Lower Limb Hip Flexion', 
                          'Initial Right Lower Limb Hip Extension',
                          'Initial Right Lower Limb Hip Abduction', 
                          'Initial Right Lower Limb Hip Adduction',
                          'Initial Right Lower Limb Knee Flexion', 
                          'Initial Right Lower Limb Knee Extension',
                          'Initial Right Lower Limb Ankle Dorsiflexion', 
                          'Initial Right Lower Limb Ankle Plantarflexion']
        
        for field in numeric_fields:
            if field in input_df:
                input_df[field] = pd.to_numeric(input_df[field], errors='coerce')

        # Preprocess: Label encode `Gender` and one-hot encode `Age`
        input_df['Gender'] = input_df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
        input_df['Age Group'] = pd.cut(
            input_df['Age'], bins=bins, labels=labels, right=False
        )
        input_df = pd.get_dummies(input_df, columns=["Age Group"], drop_first=True)

        # Align input DataFrame with training columns
        for col in columns:
            if col not in input_df:
                input_df[col] = 0  # Add missing columns with default value 0

        input_df = input_df[columns]  # Ensure column order matches training data
        return input_df
    except Exception as e:
        print(f"Error in preprocessing: {str(e)}")
        raise

# Flask API for model5 prediction
@app.route('/predict_model5', methods=['POST'])
def predict_model5():
    try:
        data = request.json  # Parse incoming JSON data
        print("Received data for model 5:", data)

        if not data or 'inputs' not in data:
            return jsonify({"error": "No data or invalid data format provided"}), 400

        model5_data = data['inputs']  # Extract inputs for model 5

        # Preprocess input data
        processed_df = preprocess_input_data(model5_data)

        # Debugging information
        print("Processed DataFrame columns:", processed_df.columns.tolist())
        print("Processed DataFrame:\n", processed_df)

        # Make prediction
        prediction = pipeline.predict(processed_df)
        print("Prediction result for model 5:", prediction)

        # Convert predictions to a Python list
        prediction_list = prediction.tolist()

        # Format predictions: Each prediction in a separate line
        formatted_predictions = [f"Prediction {i+1}: {pred}" for i, pred in enumerate(prediction)]

        # Return formatted predictions
        return jsonify({"result5": prediction_list})

    except Exception as e:
        print(f"Error in predict_model5: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

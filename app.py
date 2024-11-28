from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import shutil

app = Flask(__name__)
CORS(app)

# Load the pre-trained models
pickle_file_path_model1 = r'C:\python\model\best_random_forest_model.pkl'
pickle_file_path_model2 = r'C:\python\model\10M.pkl'
pickle_file_path_model3 = r'C:\python\model\TugRight.pkl'
pickle_file_path_model4 = r'C:\python\model\10Right.pkl'

with open(pickle_file_path_model1, 'rb') as file1:
    model1 = pickle.load(file1)

with open(pickle_file_path_model2, 'rb') as file2:
    model2 = pickle.load(file2)

with open(pickle_file_path_model3, 'rb') as file3:
    model3 = pickle.load(file3)

with open(pickle_file_path_model4, 'rb') as file4:
    model4 = pickle.load(file4)

# LabelEncoder for Gender column
label_encoder = LabelEncoder()

# Function to update SCONE integration_accuracy
def update_integration_accuracy(file_path, new_accuracy, new_file_name):
    try:
        # Read the SCONE file content
        with open(file_path, 'r') as file:
            content = file.readlines()

        # Update the 'integration_accuracy' parameter
        updated_content = []
        for line in content:
            if 'integration_accuracy' in line:
                line = f'integration_accuracy = {new_accuracy}\n'
            updated_content.append(line)

        # Construct new file path for saving the updated file
        directory = r"C:\python\configs\Tutorials2"
        new_file_path = f"{directory}\\{new_file_name}"

        # Write the updated content to the new file
        with open(new_file_path, 'w') as file:
            file.writelines(updated_content)

        print(f"Updated 'integration_accuracy' to {new_accuracy} and saved as {new_file_name} in {directory}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# SCONE configuration file path
scone_file_path = r"C:\python\configs\Tutorials2\Tutorial 4a - Gait - OpenSim.scone"
new_file_name = "changed-gate.scone"  # Set the new file name

# Model 1 Prediction
@app.route('/predict_model1', methods=['POST'])
def predict_model1():
    try:
        data = request.json
        print("Received data for model 1:", data)

        model1_data = data.get("model1_inputs")
        
        if model1_data:
            model1_df = pd.DataFrame([model1_data])
            model1_df.rename(columns={"DaysOfTreatment": "Days Of Treatment"}, inplace=True)
            model1_df['Gender'] = label_encoder.fit_transform(model1_df['Gender'])
            model1_prediction = model1.predict(model1_df)[0]

            # Set integration_accuracy based on prediction value
            if model1_prediction < 0:
                integration_accuracy_value = 0.0013
            else:
                integration_accuracy_value = model1_prediction

            # Update the integration_accuracy in the SCONE configuration file
            update_integration_accuracy(scone_file_path, integration_accuracy_value, new_file_name)
        else:
            model1_prediction = None

        return jsonify({
            "result1": model1_prediction
        })

    except Exception as e:
        print("Error:", e)  # Log the error for debugging
        return jsonify({"error": str(e)}), 400

# Model 2 Prediction
@app.route('/predict_model2', methods=['POST'])
def predict_model2():
    try:
        data = request.json
        print("Received data for model 2:", data)

        model2_data = data.get("model2_inputs")
        
        if model2_data:
            model2_df = pd.DataFrame([model2_data])
            model2_df.rename(columns={"DaysOfTreatment": "Days Of Treatment"}, inplace=True)
            model2_df['Gender'] = label_encoder.fit_transform(model2_df['Gender'])
            model2_prediction = model2.predict(model2_df)[0]
        else:
            model2_prediction = None

        return jsonify({
            "result2": model2_prediction
        })

    except Exception as e:
        print("Error:", e)  # Log the error for debugging
        return jsonify({"error": str(e)}), 400

# Model 3 Prediction
@app.route('/predict_model3', methods=['POST'])
def predict_model3():
    try:
        data = request.json
        print("Received data for model 3:", data)

        model3_data = data.get("model3_inputs")
        
        if model3_data:
            model3_df = pd.DataFrame([model3_data])
            model3_df.rename(columns={"DaysOfTreatment": "Days Of Treatment"}, inplace=True)
            model3_df['Gender'] = label_encoder.fit_transform(model3_df['Gender'])
            model3_prediction = model3.predict(model3_df)[0]
        else:
            model3_prediction = None

        return jsonify({
            "result3": model3_prediction
        })

    except Exception as e:
        print("Error:", e)  # Log the error for debugging
        return jsonify({"error": str(e)}), 400

# Model 4 Prediction
@app.route('/predict_model4', methods=['POST'])
def predict_model4():
    try:
        data = request.json
        print("Received data for model 4:", data)

        model4_data = data.get("model4_inputs")
        
        if model4_data:
            model4_df = pd.DataFrame([model4_data])
            model4_df.rename(columns={"DaysOfTreatment": "Days Of Treatment"}, inplace=True)
            model4_df['Gender'] = label_encoder.fit_transform(model4_df['Gender'])
            model4_prediction = model4.predict(model4_df)[0]
        else:
            model4_prediction = None

        return jsonify({
            "result4": model4_prediction
        })

    except Exception as e:
        print("Error:", e)  # Log the error for debugging
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

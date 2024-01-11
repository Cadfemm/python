from flask import Flask, request, jsonify
import pandas as pd
import pickle

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
    
    try:
        data = request.get_json()
        received_data = data.get('data', [])
        df_t = pd.DataFrame(received_data, index=[0])
        print(df_t)
    # Process data
        updated_data = [7, 8, 9]

    # Load the training data
        datafile_train = "C:/IBS Project details/Model_Test.csv"
        bd = pd.read_csv(datafile_train)
        df = pd.DataFrame(bd)

    # One-hot encoding
        columns_to_encode = df.columns[0:7]
        one_hot_encoded_columns = pd.get_dummies(df[columns_to_encode], prefix=columns_to_encode)

    # Impute NaN values with mode
        for column in df.columns:
            mode_value = df[column].mode().iloc[0]
            df[column] = df[column].fillna(mode_value)
        df.drop(columns=columns_to_encode, axis=1, inplace=True)

    # Concatenate one-hot encoded columns at the beginning
        df = pd.concat([one_hot_encoded_columns, df], axis=1)

    
        x_train = df.drop(df.loc[:, 'Initial deviation from ideal swing right':], axis=1)

    # Specify the path to the trained model
        model_path = "C:/IBS Project details/trained_model.pkl"

    # Load the trained model using pickle
        with open(model_path, 'rb') as model_file:
            loaded_model = pickle.load(model_file)

        
    

    # One-hot encoding
        columns_to_encode = df_t.columns[0:7]
        one_hot_encoded_columns = pd.get_dummies(df_t[columns_to_encode], prefix=columns_to_encode)

    # Convert boolean values to integers (0 and 1)

    # Concatenate one-hot encoded columns at the beginning
        df_t = pd.concat([one_hot_encoded_columns, df_t], axis=1)
        for col in x_train.columns:
        # If the column is not present in df2, add it with values filled as False
        # print(col)
            if col not in df_t.columns:
                df_t[col] = False

    # Reorder columns in df2 to match the order of df1
        df_t = df_t[x_train.columns]
        print(df_t)
        updated_datapanda = loaded_model.predict(df_t)
        updated_data = updated_datapanda.tolist()[0]

        return jsonify({'message': 'Data processed successfully', 'updatedData': updated_data})
    except Exception as e:
        return jsonify({'error':str(e)})

if __name__ == '__main__':
    app.run(debug=True)
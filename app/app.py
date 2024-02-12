from flask import Flask, render_template, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
import pandas as pd
from io import BytesIO
import pickle
import mlflow
import mlflow.sklearn
import os
import time


app = Flask(__name__)
auth = HTTPBasicAuth()

model = pickle.load(open('fraud_detection_model.sav', 'rb'))

# Set MLflow tracking URI
mlflow_tracking_uri = 'frauddetectionmodel.azurewebsites.net'
mlflow.set_tracking_uri(mlflow_tracking_uri)

# Define experiment name
experiment_name = "fraud_detection"
mlflow.set_experiment(experiment_name)
log_file = 'user_data.csv'

# Check if the log file exists, if not, create it with headers
if not os.path.isfile(log_file):
    with open(log_file, 'w') as f:
        f.write("Time,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,"
                "V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27"
                ",V28,Amount, Class\n")

# Define username and password for basic authentication
USERNAME = 'admin'
PASSWORD = 'admin'


@auth.verify_password
def verify_password(username, password):
    return username == USERNAME and password == PASSWORD


@app.route('/')
@auth.login_required
def home():
    return render_template('index.html')


def predict_data(features):
    start_time = time.time()  # Capture start time
    prediction = model.predict([features])
    end_time = time.time()  # Capture end time
    response_time = end_time - start_time
    prediction_text = 'Potentially Fraudulent Activity Detected' if prediction[0] == 1 else 'Transaction Appears Normal'
    return prediction_text, response_time, prediction[0]


def predict_file(file):
    df = pd.read_csv(file)
    start_time = time.time()  # Capture start time
    df = df.iloc[1:, :].reset_index(drop=True)  # Exclude the first row(Columns names) and reset the index
    predictions = model.predict(df.values)
    end_time = time.time()  # Capture end time
    response_time = end_time - start_time
    df['Class'] = predictions
    prediction_texts = ['Potentially Fraudulent Activity Detected' if p == 1 else 'Transaction Appears Normal' for p in
                        predictions]
    return prediction_texts, response_time, df


@app.route('/predict', methods=['POST'])
@auth.login_required
def predict():
    try:
        if request.is_json:
            data = request.get_json()
            features = [data[f'V{i}'] for i in range(1, 29)]
            features = [float(data['Time'])] + [float(v) for v in features] + [float(data['Amount'])]
            prediction_text, response_time, prediction = predict_data(features)
            log_mlflow(features, response_time, prediction)
            return jsonify(
                {'prediction': prediction_text, 'response_time': response_time, 'prediction_value': prediction})
        else:
            time_val = float(request.form['time'])
            features = [float(request.form[f'v{i}']) for i in range(1, 29)]
            amount = float(request.form['amount'])
            features = [time_val] + features + [amount]
            prediction_text, response_time, prediction = predict_data(features)
            log_mlflow(features, response_time, prediction)
            return render_template('index.html', prediction=prediction_text, response_time=response_time,
                                   prediction_value=prediction)

    except Exception as e:
        if request.is_json:
            return jsonify({'error': str(e)}), 400
        else:
            return render_template('index.html', error=str(e))


@app.route('/predict-file', methods=['POST'])
@auth.login_required
def predict_file_route():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        prediction_texts, response_time, df = predict_file(file)

        # Save the DataFrame with the 'Class' column
        output_file_path = 'file_with_predictions.csv'
        df.to_csv(output_file_path, index=False)

        # Log the data to MLflow
        log_mlflow(df.iloc[0, :].tolist(), response_time, df['Class'].tolist()[0])

        # Send the file as a downloadable attachment
        output_file = BytesIO()
        with open(output_file_path, 'rb') as f:
            output_file.write(f.read())
        output_file.seek(0)

        return send_file(output_file, as_attachment=True, download_name='file_with_predictions.csv',
                         mimetype='text/csv')

    except Exception as e:
        return jsonify({'error': str(e)}), 400


def log_mlflow(features, response_time, prediction_value):
    with mlflow.start_run():
        features_dict = {
            f'V{i}': feature for i, feature in enumerate(features[1:29], start=1)
        }
        features_dict['Time'] = features[0]
        features_dict['Amount'] = features[-1]

        # Ensure response_time and prediction_value are of numeric type
        response_time = float(response_time)
        prediction_value = float(prediction_value)

        mlflow.log_params(features_dict)
        mlflow.log_metric("response_time", response_time)
        mlflow.log_metric("prediction_value", prediction_value)

        # Append the data to the CSV file
        with open(log_file, 'a') as f:
            f.write(f"{','.join(map(str, features))},{prediction_value}\n")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

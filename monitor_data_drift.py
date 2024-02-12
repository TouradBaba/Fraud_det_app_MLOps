from train import *

url0 = 'https://raw.githubusercontent.com/TouradBaba/Fraud_det_model_MLOps/main/data/training_data.csv'
url1 = 'https://raw.githubusercontent.com/TouradBaba/Fraud_det_model_MLOps/main/data/datadrift_simulation.csv'

# Importing the data
df = pd.read_csv(url)


def calculate_drift(baseline, current):
    # Select features
    baseline_selected = baseline.drop(baseline.columns[-1], axis=1)
    current_selected = current

    baseline_mean = baseline_selected.mean()
    baseline_std = baseline_selected.std()

    current_mean = current_selected.mean()

    drift = (current_mean - baseline_mean) / baseline_std
    return drift


def main():

    baseline_data = pd.read_csv(url0)
    current_data = pd.read_csv(url1)

    # Set a threshold for data drift
    drift_threshold = 2.0
    drift = calculate_drift(baseline_data, current_data)

    if any(abs(drift) > drift_threshold):
        print("Data drift detected. Retraining the model...")
        X_train, X_test, Y_train, Y_test = preprocess_data(df)
        model = train_model(X_train, Y_train)
        evaluation_results = evaluate_model(model, X_test, Y_test)
        print("Evaluation Results:")
        print(evaluation_results)
        save_model(model)
    else:
        print("No significant data drift detected. Model remains unchanged.")


if __name__ == "__main__":
    main()

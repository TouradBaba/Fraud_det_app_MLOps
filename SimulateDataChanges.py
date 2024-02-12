import numpy as np
import pandas as pd

url = 'https://media.githubusercontent.com/media/TouradBaba/Fraud_det_model_MLOps/main/creditcard_2023.csv'


def simulate_monthly_changes(data):
    
    # Adding random noise to all features
    features = [col for col in data.columns]
    legit = data[data.Class == 0]
    fraudulent = data[data.Class == 1]
    fraudulent_sample = fraudulent.sample(n=10000)
    legit_sample = legit.sample(n=10000)
    data = pd.concat([legit_sample, fraudulent_sample], axis=0)
    data[features] += np.random.normal(2, 10, size=(len(data), len(features)))
    data = data.drop(data.columns[-1], axis=1)  # Drop the class column
  
    return data


if __name__ == "__main__":
    # Load baseline data
    df = pd.read_csv(url)

    # Simulate changes for the current month
    current_data = simulate_monthly_changes(df)

    # Save the modified data for the current month
    current_data.to_csv("datadrift_simulation.csv", index=False)

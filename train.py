import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score
import pickle


url = 'https://media.githubusercontent.com/media/TouradBaba/Fraud_det_app_MLOps/main/creditcard_2023.csv'


def load_data():
    df = pd.read_csv(url)
    return df


def preprocess_data(df):
    # Separating the data
    legit = df[df.Class == 0]
    fraudulent = df[df.Class == 1]

    """Under sampling the data, So we always have samples to retrain the model after a given time"""
    legit_sample = legit.sample(n=10000)
    fraudulent_sample = fraudulent.sample(n=10000)
    new_dataset = pd.concat([legit_sample, fraudulent_sample], axis=0)
    new_dataset.to_csv('training_data.csv')
    # Split the data into Training data and test data
    X = new_dataset.drop(columns='Class', axis=1)
    Y = new_dataset['Class']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
    return X_train, X_test, Y_train, Y_test

def train_model(X_train, Y_train):
    # Training the model
    model = LogisticRegression()
    model.fit(X_train, Y_train)
    return model

def evaluate_model(model, X_test, Y_test):
    # Evaluating the model
    Y_pred = model.predict(X_test)
    cm = confusion_matrix(Y_test, Y_pred)
    accuracy = accuracy_score(Y_test, Y_pred)
    precision = precision_score(Y_test, Y_pred)
    recall = recall_score(Y_test, Y_pred)
    f1 = f1_score(Y_test, Y_pred)
    roc_auc = roc_auc_score(Y_test, Y_pred)

    return {
        'Confusion Matrix': cm,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1,
        'ROC AUC Score': roc_auc
    }

def save_model(model):
    try:
        # Saving the model to a file
        filename = 'fraud_detection_model.sav'
        with open(filename, 'wb') as model_file:
            pickle.dump(model, model_file)
        print(f"Model saved successfully as {filename}")
    except Exception as e:
        print(f"Error saving the model: {str(e)}")


if __name__ == "__main__":
    data = load_data()
    X_train, X_test, Y_train, Y_test = preprocess_data(data)
    model = train_model(X_train, Y_train)
    evaluation_results = evaluate_model(model, X_test, Y_test)
    print("Evaluation Results:")
    print(evaluation_results)
    save_model(model)

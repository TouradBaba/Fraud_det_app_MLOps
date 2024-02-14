# Fraud Detection App - User Guide

Welcome to this Fraud Detection App! This application utilizes machine learning to predict potentially fraudulent activities in financial transactions. Whether you're accessing the app on the cloud or locally, follow this guide to seamlessly set up and make the most of its capabilities.

**Key Features:**

- **Predictive Power:** Leverage the app's machine learning algorithms to identify potential fraudulent activities in financial transactions.

- **Cloud Accessibility:** Access the app effortlessly through the cloud using the URL: [https://frauddetectionmodel.azurewebsites.net](https://frauddetectionmodel.azurewebsites.net).

- **Local Deployment:** If preferred, set up and use the app locally by following the installation and usage instructions provided in this guide.

**Enhancements and Continuous Improvement:**

- **CI/CD Integration:** Benefit from a robust Continuous Integration/Continuous Deployment (CI/CD) pipeline that ensures the app is always up-to-date with the latest enhancements and improvements.

- **Workflow for Data Drift Monitoring:** Experience a seamless workflow for monitoring data drift, which triggers model retraining and deployment in response to changes in the dataset, ensuring the app's accuracy over time.

- **Monthly Retraining:** The app undergoes monthly retraining, enhancing its predictive capabilities.

- **Cloud Deployment:** The app is efficiently deployed on the cloud, allowing for scalability, reliability, and continuous accessibility.

Follow the comprehensive guide below to navigate through the setup process and unleash the potential of this Fraud Detection App.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage on the Cloud](#usage-on-the-cloud)
4. [Usage Locally](#usage-locally)
5. [Endpoints](#endpoints)
6. [File Upload](#file-upload)
7. [Response](#response)

## Prerequisites

- Python 3.11
- Virtualenv (optional but recommended)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/TouradBaba/Fraud_det_model_MLOps.git
    ```

2. Navigate to the app directory:

    ```bash
    cd app
    ```

3. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate  # Windows
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Change the app port:
    In the `app.py` file, change the port from:

    ```bash
            app.run(host="0.0.0.0", port=8000)
    ```

    to:

    ```bash
            app.run(port=5001)
    ```

## Usage on the Cloud

1. Access the app through a web browser: [https://frauddetectionmodel.azurewebsites.net](https://frauddetectionmodel.azurewebsites.net)

2. Use the provided credentials for basic authentication:

    - Username: admin
    - Password: admin

## Usage Locally

1. Navigate to the app directory:

    ```bash
    cd app
    ```

2. Run the Flask app:

    ```bash
    python app.py
    ```

3. Access the app through a web browser: [http://localhost:5001/](http://localhost:5001/)

4. Use the provided credentials for basic authentication:

    - Username: admin
    - Password: admin

## Endpoints

- `/`: Home page with a form for making predictions.
- `/predict`: Endpoint for making predictions with JSON data.
- `/predict-file`: Endpoint for making predictions with a CSV file upload.

## File Upload

To make predictions using a CSV file, upload a CSV file containing transaction data. An Example file is provided in the repository called `test.csv`.

## Response

- For files, the app will add a new column called `Class` and assign 1 or 0 for each row:
  - 1 --> Fraudulent
  - 0 --> Normal

- For inserted data, the response will be either:
  - "Potentially Fraudulent Activity Detected"
  - "Transaction Appears Normal"

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from pathlib import Path

def train_failure_model():
    # Get the absolute path to the CSV file
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / 'predictive_maintenance.csv'
    
    # Read the dataset
    df = pd.read_csv(data_file)
    
    # Prepare features and target
    feature_columns = ['Air temperature [K]', 'Process temperature [K]', 
                      'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
    X = df[feature_columns]
    
    # Encode the Failure Type as target
    le = LabelEncoder()
    y = le.fit_transform(df['Failure Type'])
    
    # Create models directory
    models_dir = base_dir / 'models'
    models_dir.mkdir(exist_ok=True)
    
    # Save the label encoder for later use
    joblib.dump(le, models_dir / 'failure_type_encoder.joblib')
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    joblib.dump(scaler, models_dir / 'failure_scaler.joblib')
    
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Save the model
    joblib.dump(model, models_dir / 'failure_predictor.joblib')
    
    # Calculate and print accuracy
    train_accuracy = model.score(X_train_scaled, y_train)
    test_accuracy = model.score(X_test_scaled, y_test)
    
    print(f"Train Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Print unique failure types
    failure_types = le.classes_
    print("\nFailure Types:")
    for i, failure_type in enumerate(failure_types):
        print(f"{i}: {failure_type}")
    
    return model, scaler, le

if __name__ == "__main__":
    # Train and save the model
    model, scaler, le = train_failure_model()
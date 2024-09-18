import pandas as pd
import joblib

# Load the trained model, scaler, and encoder
model = joblib.load("house_price_model.pkl")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")

# Function to preprocess new input data
def preprocess_input(data):
    # Encode categorical columns
    categorical_columns = [
        "mainroad", "guestroom", "basement", "hotwaterheating", 
        "airconditioning", "prefarea", "furnishingstatus"
    ]
    encoded_data = encoder.transform(data[categorical_columns])
    encoded_df = pd.DataFrame(
        encoded_data, columns=encoder.get_feature_names_out(categorical_columns)
    )
    
    # Scale numerical columns
    numerical_columns = ["area", "bedrooms", "bathrooms", "stories", "parking"]
    scaled_data = scaler.transform(data[numerical_columns])
    scaled_df = pd.DataFrame(scaled_data, columns=numerical_columns)
    
    # Combine processed data
    processed_data = pd.concat([scaled_df, encoded_df], axis=1)
    return processed_data

# Example new input for prediction
new_data = pd.DataFrame({
    'area': [3000],
    'bedrooms': [2],
    'bathrooms': [3],
    'stories': [2],
    'parking': [2],
    'mainroad': ['yes'],
    'guestroom': ['no'],
    'basement': ['no'],
    'hotwaterheating': ['no'],
    'airconditioning': ['yes'],
    'prefarea': ['no'],
    'furnishingstatus': ['furnished']
})

# Preprocess input
preprocessed_data = preprocess_input(new_data)

# Make a prediction
prediction = model.predict(preprocessed_data)
print(f"Predicted house price: {prediction[0]}")

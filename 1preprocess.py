#preprocess , training and and saving the model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
file_path = "data.csv"  # Update with your correct file path
df = pd.read_csv(file_path)

# Rename columns (fix currency symbols if needed)
df.rename(columns={
    "Travel Cost (?)": "Travel Cost",
    "Accommodation Cost (?)": "Accommodation Cost",
    "Food Cost (?)": "Food Cost",
    "Total Budget (?)": "Total Budget"
}, inplace=True)

# Drop ID column
df.drop(columns=["ID"], inplace=True)

# Encode categorical variables
label_encoders = {}
for col in ["Destination", "Travel Mode"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoders for later use

# Split features and target
X = df.drop(columns=["Total Budget"])
y = df["Total Budget"]

# Train-test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers # type: ignore

# Define model
model = keras.Sequential([
    layers.Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(1)  # Output layer for budget prediction
])

# Compile model
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Train model
history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=512, validation_data=(X_test_scaled, y_test), verbose=1)
model.save("travel_budget_model.h5")  # Save in .h5 format for deployment

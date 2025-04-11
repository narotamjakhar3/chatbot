from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
import pandas as pd
from sklearn.preprocessing import StandardScaler

    # Define custom loss function explicitly
custom_objects = {"mse": tf.keras.losses.MeanSquaredError()}

    # Load trained model with custom objects
model = load_model("travel_budget_model.h5", custom_objects=custom_objects)

    # Dummy scaler (Replace with actual scaler used in training)
scaler = StandardScaler()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = pd.DataFrame([data])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        return jsonify({"predicted_budget": float(prediction[0][0])})
    except Exception as e:
        return jsonify({"error": str(e)})
if __name__ == "__main__":
    app.run(debug=True)

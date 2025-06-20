from flask import Flask, render_template, request
import joblib
import numpy as np
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the trained machine learning model
try:
    model = joblib.load('house_price_model.pkl')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None


@app.route('/', methods=['GET', 'POST'])
def predict():
    """
    Handles house price prediction via a POST form.
    """
    prediction = None

    if request.method == 'POST':
        if model is None:
            prediction = "Model not loaded. Please contact administrator."
            return render_template("index.html", prediction=prediction)

        try:
            # Get input values from the form - make sure these names match your form input 'name' attributes
            feature1 = float(request.form.get('OverallQual', 0))    # Overall Quality
            feature2 = float(request.form.get('GrLivArea', 0))      # Living Area
            feature3 = float(request.form.get('GarageCars', 0))     # Garage Capacity
            feature4 = float(request.form.get('TotalBsmtSF', 0))    # Basement Area

            logging.info(f"Received inputs: OverallQual={feature1}, GrLivArea={feature2}, GarageCars={feature3}, TotalBsmtSF={feature4}")

            input_data = np.array([[feature1, feature2, feature3, feature4]])

            # Predict price
            result = model.predict(input_data)[0]
            prediction = round(result, 2)

            logging.info(f"Prediction result: {prediction}")

        except ValueError:
            prediction = "Invalid input. Please enter numeric values only."
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            prediction = "An error occurred during prediction."

    return render_template("index.html", prediction=prediction)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

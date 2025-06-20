from flask import Flask, render_template, request
import joblib
import numpy as np
import logging

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
            # Get input values and validate
            feature1 = float(request.form.get('feature1', 0))  # OverallQual
            feature2 = float(request.form.get('feature2', 0))  # GrLivArea
            feature3 = float(request.form.get('feature3', 0))  # GarageCars
            feature4 = float(request.form.get('feature4', 0))  # TotalBsmtSF

            input_data = np.array([[feature1, feature2, feature3, feature4]])

            # Predict and round result
            result = model.predict(input_data)[0]
            prediction = round(result, 2)

        except ValueError:
            prediction = "Invalid input. Please enter numeric values only."
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            prediction = "An error occurred during prediction."

    return render_template("index.html", prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)

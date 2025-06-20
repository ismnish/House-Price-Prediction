<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>House Price Prediction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #f5f5f5;
        }

        .app-container {
            background-image: url("../static/houses_prices.jpg");
            background-size: cover;
            background-position: center;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .form-container {
            background: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
        }

        .form-container h1 {
            margin-bottom: 30px;
            font-size: 26px;
            text-align: center;
            color: #333;
        }

        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
            color: #333;
        }

        input[type="number"],
        select {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 16px;
        }

        select {
            background-color: white;
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
        }

        small {
            display: block;
            margin-top: 3px;
            color: #666;
            font-size: 13px;
        }

        .button {
            background-color: #007bff;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            padding: 12px;
            margin-top: 20px;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s ease;
        }

        .button:hover:not(:disabled) {
            background-color: #0056b3;
        }

        .button:disabled {
            background-color: #999;
            cursor: not-allowed;
        }

        .result {
            margin-top: 25px;
            font-size: 18px;
            color: green;
            text-align: center;
        }
    </style>
</head>

<body>
    <div class="app-container">
        <div class="form-container">
            <h1>🏠 House Price Prediction</h1>
            <form method="POST" novalidate>
                <!-- Overall Quality -->
                <label for="OverallQual">Overall Quality (1–10):</label>
                <input type="number" id="OverallQual" name="OverallQual" min="1" max="10" step="1" required
                    placeholder="e.g. 7" title="1 = Poor quality, 10 = Excellent quality" />
                <small>Material and finish quality (1 = Poor, 10 = Excellent)</small>

                <!-- Living Area -->
                <label for="GrLivArea">Above Ground Living Area (sq ft):</label>
                <input type="number" id="GrLivArea" name="GrLivArea" min="100" max="15000" step="any" required
                    placeholder="e.g. 1710" title="Total finished living space above ground in square feet" />
                <small>Example: 1710 sq ft</small>

                <!-- Garage Cars -->
                <label for="GarageCars">Garage Capacity (number of cars):</label>
                <input type="number" id="GarageCars" name="GarageCars" min="0" max="4" step="1" required
                    placeholder="e.g. 2" />
                <small>Cars that can fit in the garage</small>

                <!-- Basement Area -->
                <label for="TotalBsmtSF">Total Basement Area (sq ft):</label>
                <input type="number" id="TotalBsmtSF" name="TotalBsmtSF" min="0" max="6000" step="any" required
                    placeholder="e.g. 856" />
                <small>Finished and unfinished basement area combined</small>

                <!-- Year Built -->
                <label for="YearBuilt">Year Built:</label>
                <input type="number" id="YearBuilt" name="YearBuilt" min="1800" max="2025" required
                    placeholder="e.g. 2003" />
                <small>Year the house was built</small>

                <!-- Full Bathrooms -->
                <label for="FullBath">Number of Full Bathrooms:</label>
                <input type="number" id="FullBath" name="FullBath" min="0" max="5" step="1" required
                    placeholder="e.g. 2" />
                <small>Full bathrooms (with shower or bathtub)</small>

                <!-- Bedrooms -->
                <label for="BedroomAbvGr">Bedrooms (Above Ground):</label>
                <input type="number" id="BedroomAbvGr" name="BedroomAbvGr" min="0" max="10" step="1" required
                    placeholder="e.g. 3" />
                <small>Number of bedrooms above ground level</small>

                <!-- Fireplaces -->
                <label for="Fireplaces">Number of Fireplaces:</label>
                <input type="number" id="Fireplaces" name="Fireplaces" min="0" max="3" step="1" required
                    placeholder="e.g. 1" />
                <small>Number of fireplaces in the house</small>

                <!-- Kitchen Quality -->
                <label for="KitchenQual">Kitchen Quality:</label>
                <select id="KitchenQual" name="KitchenQual" required>
                    <option value="">-- Select Quality --</option>
                    <option value="Ex">Excellent</option>
                    <option value="Gd">Good</option>
                    <option value="TA">Typical</option>
                    <option value="Fa">Fair</option>
                </select>
                <small>Rate kitchen condition</small>

                <!-- Neighborhood -->
                <label for="Neighborhood">Neighborhood:</label>
                <select id="Neighborhood" name="Neighborhood" required>
                    <option value="">-- Select Neighborhood --</option>
                    <option value="CollgCr">College Creek</option>
                    <option value="Veenker">Veenker</option>
                    <option value="Crawfor">Crawford</option>
                    <!-- Add more neighborhoods from your dataset as needed -->
                </select>
                <small>Neighborhood where the house is located</small>

                <!-- Submit Button -->
                <input class="button" type="submit" value="Predict Price" />
            </form>

            {% if prediction %}
            <div class="result">
               Predicted House Price: <strong>₹{{ prediction }}</strong>
            </div>
            {% endif %}
        </div>
    </div>
<footer style="
  text-align: center; 
  margin-top: 40px; 
  padding: 15px 0; 
  font-size: small; 
  color: #ffffff; 
  background-color: #333333;
  border-top: 1px solid #444444;
">
  &copy; {{ current_year }} Manish. All rights reserved.
</footer>


    <script>
        const form = document.querySelector('form');
        const submitButton = document.querySelector('.button');

        form.addEventListener('submit', function () {
            // Disable the button to prevent multiple submissions
            submitButton.disabled = true;
            submitButton.value = "Calculating...";

            // Clear previous result or create a new div to show calculating text
            let resultDiv = document.querySelector('.result');
            if (!resultDiv) {
                resultDiv = document.createElement('div');
                resultDiv.classList.add('result');
                form.parentNode.appendChild(resultDiv);
            }
            resultDiv.textContent = "Calculating...";
        });
    </script>
</body>

</html>

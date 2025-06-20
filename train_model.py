# train_model.py

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Step 1: Load dataset
data_path = 'train.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset not found at '{data_path}'")

df = pd.read_csv(data_path)

# Step 2: Select and clean relevant features
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'SalePrice']
df = df[features].dropna()

# Step 3: Prepare input and target variables
X = df.drop('SalePrice', axis=1)
y = df['SalePrice']

# Step 4: Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 5: Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
print(f"\nModel evaluation:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

# Optional: Display feature importances
print("\nFeature importances:")
for feature, importance in zip(X.columns, model.feature_importances_):
    print(f"{feature}: {importance:.4f}")

# Step 7: Save model
model_path = 'house_price_model.pkl'
joblib.dump(model, model_path)
print(f"\nModel saved to '{model_path}'")

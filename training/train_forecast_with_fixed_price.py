import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time

## Load dataset
df = pd.read_csv("D:\OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED\Desktop\EMS R&D\Cheese_Craft_EMS\data\historical_sales_enriched_final_ready.csv")

# Encode categorical columns
df = pd.get_dummies(df, columns=['product', 'season'])

# Drop null values
df = df.dropna()

print("Dataset Shape (rows, columns):", df.shape)
print("Descriptive Statistics Before Training:")
print(df.describe())

# Outlier detection (IQR Method)
outlier_bounds = {}
for col in ["sales", "revenue", "profit", "inventory"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outlier_bounds[col] = {"lower": round(lower, 2), "upper": round(upper, 2)}
    print(f"• {col}: Lower Bound = {lower:.2f}, Upper Bound = {upper:.2f}")

# Save outlier thresholds to Knowledge Base
os.makedirs("kb", exist_ok=True)
with open("kb/outlier_thresholds.md", "w") as f:
    f.write("# Outlier Thresholds for Forecast Monitoring (IQR-based)\n\n")
    for metric, bounds in outlier_bounds.items():
        f.write(f"- **{metric.capitalize()}**:\n")
        f.write(f"  - Lower Bound: {bounds['lower']}\n")
        f.write(f"  - Upper Bound: {bounds['upper']}\n\n")

# Save distribution plots for target columns
os.makedirs("plots", exist_ok=True)
target_columns = ["sales", "revenue", "profit", "inventory"]
for target in target_columns:
    plt.figure(figsize=(6, 4))
    sns.histplot(df[target], kde=True, bins=30, color="lightgreen")
    plt.title(f"Distribution of {target}")
    plt.xlabel(target)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"plots/distribution_{target}.png")
    plt.close()

# Define feature columns (excluding target variables like sales, revenue, profit, inventory)
feature_cols = [col for col in df.columns if col not in ["sales", "revenue", "profit", "inventory"]]

# Save model directory
os.makedirs("app/models", exist_ok=True)

# Evaluation function
def evaluate_model(X_test, y_test, y_pred, target):
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Manual RMSE
    r2 = r2_score(y_test, y_pred)

    print(f"\nEvaluation for model_{target}.pkl")
    print(f"  - MAE  : {mae:.2f}")
    print(f"  - RMSE : {rmse:.2f}")
    print(f"  - R²   : {r2:.2f}")

# Training + evaluation function with dynamic model saving using a counter
def train_and_save_model(target, counter):
    X = df[feature_cols]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    evaluate_model(X_test, y_test, y_pred, target)

    # Save the model with a counter (sales or revenue)
    model_filename = f"app/models/model_{target}_{counter}.pkl"
    joblib.dump(model, model_filename)
    print(f"XGBoost model saved: {model_filename}")

# Initialize counters for sales and revenue models
counter_sales = 1
counter_revenue = 1

# Train and save the sales and revenue models with dynamic counters
train_and_save_model("sales", counter_sales)
train_and_save_model("revenue", counter_revenue)

# Increment counters for the next models if needed
counter_sales += 1
counter_revenue += 1

# Now, during forecast prediction, we'll set the price as constant for the revenue calculation

def forecast_with_constant_price(model, X_test, constant_price=7.5):
    """
    Use the trained model to predict sales and calculate revenue with a fixed price per unit.
    """
    # Predict sales volume from the model
    predicted_sales = model.predict(X_test)
    
    # Revenue is simply sales * constant price per unit (e.g., $7.5)
    predicted_revenue = predicted_sales * constant_price
    
    return predicted_sales, predicted_revenue

# Example: Using the trained model to predict sales and revenue with constant price
sales_model = joblib.load("app/models/model_sales_1.pkl")  # Assuming you've trained the sales model
revenue_model = joblib.load("app/models/model_revenue_1.pkl")  # Assuming you also have a revenue model

# Get the test data (you can use the X_test from earlier)
X_test = df[feature_cols]  # Or use a separate test dataset

# Call the forecasting function with a constant price per unit (e.g., $7.5)
predicted_sales, predicted_revenue = forecast_with_constant_price(sales_model, X_test, constant_price=7.5)

# Display the first few predictions
print(f"Predicted Sales (first 5): {predicted_sales[:5]}")
print(f"Predicted Revenue (first 5, with constant price): {predicted_revenue[:5]}")

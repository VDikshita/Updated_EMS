################################################ With flatuating unit price*********************

# import pandas as pd
# import numpy as np
# import os
# from sklearn.model_selection import train_test_split
# from xgboost import XGBRegressor
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os

# import joblib

# ## load dataset
# df=pd.read_csv("data\historical_sales_enriched_final_ready.csv")

# #encode categorical cloumn
# df=pd.get_dummies(df, columns=['product','season'])

# # drop null values
# df=df.dropna()

# print(" Dataset Shape (rows, columns):", df.shape)

# print(" Descriptive Statistics Before Training:")
# print(df.describe())

# print("\n Outlier Thresholds (IQR Method):")
# outlier_bounds = {}

# for col in ["sales", "revenue", "profit", "inventory"]:
#     Q1 = df[col].quantile(0.25)
#     Q3 = df[col].quantile(0.75)
#     IQR = Q3 - Q1
#     lower = Q1 - 1.5 * IQR
#     upper = Q3 + 1.5 * IQR
#     outlier_bounds[col] = {"lower": round(lower, 2), "upper": round(upper, 2)}
#     print(f"• {col}: Lower Bound = {lower:.2f}, Upper Bound = {upper:.2f}")

#     # Save to KB
# os.makedirs("kb", exist_ok=True)
# with open("kb/outlier_thresholds.md", "w") as f:
#     f.write("# Outlier Thresholds for Forecast Monitoring (IQR-based)\n\n")
#     for metric, bounds in outlier_bounds.items():
#         f.write(f"- **{metric.capitalize()}**:\n")
#         f.write(f"  - Lower Bound: {bounds['lower']}\n")
#         f.write(f"  - Upper Bound: {bounds['upper']}\n\n")


# # Save plots for all target columns
# os.makedirs("plots", exist_ok=True)

# target_columns = ["sales", "revenue", "profit", "inventory"]
# for target in target_columns:
#     plt.figure(figsize=(6, 4))
#     sns.histplot(df[target], kde=True, bins=30, color="lightgreen")
#     plt.title(f"Distribution of {target}")
#     plt.xlabel(target)
#     plt.ylabel("Frequency")
#     plt.tight_layout()
#     plt.savefig(f"plots/distribution_{target}.png")
#     plt.close()

# ## define future
# feature_cols=[col for col in df.columns if col not in ["sales", "revenue", "profit", "inventory"]]
 
# # save dir.
# os.makedirs("app/models",exist_ok=True)


# #  Evaluation function
# def evaluate_model(X_test, y_test, y_pred, target):
#     mae = mean_absolute_error(y_test, y_pred)
#     rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Manual RMSE
#     r2 = r2_score(y_test, y_pred)

#     print(f"\n Evaluation for model_{target}.pkl")
#     print(f"  - MAE  : {mae:.2f}")
#     print(f"  - RMSE : {rmse:.2f}")
#     print(f"  - R²   : {r2:.2f}")

# # Training + evaluation
# def train_and_save_model(target):
#     X = df[feature_cols]
#     y = df[target]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#     model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
#     model.fit(X_train, y_train)

#     y_pred = model.predict(X_test)
#     evaluate_model(X_test, y_test, y_pred, target)

#     joblib.dump(model, f"app/models/model_{target}.pkl")
#     print(f"XGBoost model saved: model_{target}.pkl")

# #  Train all models
# for target in ["sales", "revenue", "profit", "inventory"]:
#     train_and_save_model(target)



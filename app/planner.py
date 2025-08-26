######
# import pandas as pd
# import os
# import joblib
# from datetime import datetime, timedelta

# # Constants matching your project structure
# MODELS_DIR = "D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED/Desktop/EMS R&D/Cheese_Craft_EMS/app/models"  # Absolute path to models
# DATA_DIR = "data"

# # Load XGBoost models (sales and revenue models)
# model_sales = joblib.load(os.path.join(MODELS_DIR, "model_sales_1.pkl"))
# model_revenue = joblib.load(os.path.join(MODELS_DIR, "model_revenue_1.pkl"))

# # Load historical data for reference (no 'date' column, use 'week' directly)
# df = pd.read_csv(os.path.join(DATA_DIR, "D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED\Desktop/EMS R&D/Cheese_Craft_EMS/data/historical_sales_enriched_final_ready.csv"))

# # Proceed with the logic using the 'week' column for forecasting without creating a date
# # The 'week' column will be used directly for forecasting
# df['week'] = df['week']  # This keeps the 'week' column as it is

# # Define the feature columns (excluding target variables like sales, revenue, profit, and inventory)
# feature_cols = [col for col in df.columns if col not in ["sales", "revenue", "profit", "inventory", "date"]]

# # Use the latest data point for forecasting
# X_test = df[feature_cols].iloc[-1:]  # Use the most recent row for prediction

# def generate_xgb_forecast(model, X_test):
#     """Generate forecast using XGBoost model"""
#     forecast = model.predict(X_test)
#     return [int(round(x)) for x in forecast]

# def generate_multiweek_plan(current_date, weeks_ahead=4):
#     """
#     Generate forecasts for sales and revenue using XGBoost models.
#     Args:
#         current_date: Datetime object or string (YYYY-MM-DD)
#         weeks_ahead: Number of weeks to forecast (default=4)
#     Returns:
#         List of forecast dictionaries with XGBoost predictions
#     """
#     if isinstance(current_date, str):
#         current_date = datetime.strptime(current_date, '%Y-%m-%d')
    
#     current_week = current_date.isocalendar().week

#     # Generate forecasts using the trained XGBoost models
#     sales_forecast = generate_xgb_forecast(model_sales, X_test)
#     revenue_forecast = generate_xgb_forecast(model_revenue, X_test)

#     forecasts = []
#     for i in range(weeks_ahead):
#         forecast_date = current_date + timedelta(weeks=i+1)
#         week = current_week + i + 1
        
#         forecasts.append({
#             'date': forecast_date.strftime('%Y-%m-%d'),
#             'week': week,
#             'sales': sales_forecast[i],
#             'revenue': revenue_forecast[i],
#             'forecast_type': 'XGBoost'
#         })
    
#     return forecasts

# # Example usage
# if __name__ == "__main__":
#     sample_forecasts = generate_multiweek_plan("2023-10-01")
#     print("XGBoost Forecasts:")
#     for f in sample_forecasts:
#         print(f"Week {f['week']} ({f['date']}): Sales={f['sales']}, Revenue={f['revenue']}")




#*********************************************************************************************************
# import pandas as pd
# import os
# import joblib

# # Load trained XGBoost models
# # model_sales = joblib.load("app/models/model_sales_1.pkl")
# # model_revenue = joblib.load("app/models/model_revenue_1.pkl")
# # model_profit = joblib.load("app/models/model_profit.pkl")
# # model_inventory = joblib.load("app/models/model_inventory.pkl")

# model_sales = joblib.load("models/model_sales_1.pkl")
# model_revenue = joblib.load("models/model_revenue_1.pkl")
# model_profit = joblib.load("models/model_profit.pkl")
# model_inventory = joblib.load("models/model_inventory.pkl")

# # Load historical data
# df = pd.read_csv("D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED/Desktop/EMS R&D/Cheese_Craft_EMS - Copy/data/historical_sales_enriched_final_ready.csv")

# def get_season_from_week(week: int) -> str:
#     """
#     Assigns a season based on the week number.
#     """
#     if 10 <= week <= 22:
#         return "spring"
#     elif 23 <= week <= 35:
#         return "summer"
#     elif 36 <= week <= 48:
#         return "fall"
#     else:
#         return "winter"

# def generate_multiweek_plan(product, current_week, actual_sales, weeks_ahead=4):
#     forecasts = []
#     unit_price = 7.5  # optional; not used in modeling directly

#     for i in range(1, weeks_ahead + 1):
#         week = current_week + i

#         # Lag features
#         lag_1 = forecasts[-1]["sales"] if forecasts else actual_sales

#         if len(forecasts) >= 2:
#             lag_2 = forecasts[-2]["sales"]
#         elif not df[df["week"] == current_week - 1].empty:
#             lag_2 = df[df["week"] == current_week - 1]["sales"].values[0]
#         else:
#             lag_2 = actual_sales

#         # Prepare input features
#         input_row = pd.DataFrame([{
#             "week": week,
#             "product": product,
#             "price": unit_price,
#             "promotion_flag": 0,
#             "season": get_season_from_week(week),
#             "month": ((week - 1) // 4 + 1),
#             "lag_1_sales": lag_1,
#             "lag_2_sales": lag_2
#         }])

#         # One-hot encode input
#         input_row_encoded = pd.get_dummies(input_row)
#         for model in [model_sales, model_revenue, model_profit, model_inventory]:
#             for col in model.feature_names_in_:
#                 if col not in input_row_encoded:
#                     input_row_encoded[col] = 0

#         input_row_encoded = input_row_encoded[model_sales.feature_names_in_]

#         # Predict all 4 metrics
#         sales = int(model_sales.predict(input_row_encoded)[0])
#         revenue = int(model_revenue.predict(input_row_encoded)[0])
#         profit = int(model_profit.predict(input_row_encoded)[0])
#         inventory = int(model_inventory.predict(input_row_encoded)[0])

#         forecasts.append({
#             "week": week,
#             "sales": sales,
#             "revenue": revenue,
#             "profit": profit,
#             "inventory": inventory
#         })

#     return forecasts



#############################################################################################
import pandas as pd
import os
import joblib

# Load trained XGBoost models
model_sales = joblib.load("app/models/model_sales_1.pkl")
model_revenue = joblib.load("app/models/model_revenue_1.pkl")  
model_profit = joblib.load("app/models/model_profit.pkl")
model_inventory = joblib.load("app/models/model_inventory.pkl")

# Load historical data
df = pd.read_csv("D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED/Desktop/EMS R&D/Cheese_Craft_EMS - Copy/data/historical_sales_enriched_final_ready.csv")

def get_season_from_week(week: int) -> str:
    """
    Assigns a season based on the week number.
    """
    if 10 <= week <= 22:
        return "spring"
    elif 23 <= week <= 35:
        return "summer"
    elif 36 <= week <= 48:
        return "fall"
    else:
        return "winter"

def generate_multiweek_plan(product, current_week, actual_sales, weeks_ahead=4):
    forecasts = []
    unit_price = 7.5  # Fixed unit price for forecasting

    for i in range(1, weeks_ahead + 1):
        week = current_week + i

        # Lag features
        lag_1 = forecasts[-1]["sales"] if forecasts else actual_sales

        if len(forecasts) >= 2:
            lag_2 = forecasts[-2]["sales"]
        elif not df[df["week"] == current_week - 1].empty:
            lag_2 = df[df["week"] == current_week - 1]["sales"].values[0]
        else:
            lag_2 = actual_sales

        # Prepare input features
        input_row = pd.DataFrame([{
            "week": week,
            "product": product,
            "price": unit_price,
            "promotion_flag": 0,
            "season": get_season_from_week(week),
            "month": ((week - 1) // 4 + 1),
            "lag_1_sales": lag_1,
            "lag_2_sales": lag_2
        }])

        # One-hot encode input
        input_row_encoded = pd.get_dummies(input_row)
        for model in [model_sales, model_profit, model_inventory]: 
            for col in model.feature_names_in_:
                if col not in input_row_encoded:
                    input_row_encoded[col] = 0

        input_row_encoded = input_row_encoded[model_sales.feature_names_in_]

        # Predict metrics
        sales = int(model_sales.predict(input_row_encoded)[0])
        revenue = int(sales * unit_price)  # Use fixed price
        profit = int(model_profit.predict(input_row_encoded)[0])
        inventory = int(model_inventory.predict(input_row_encoded)[0])

        forecasts.append({
            "week": week,
            "sales": sales,
            "revenue": revenue,
            "profit": profit,
            "inventory": inventory
        })

    return forecasts



# evaluation.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Connect to EMS log
def load_ems_log():
    conn = sqlite3.connect("memory/ems_log.db")
    df = pd.read_sql_query("SELECT * FROM ems_log", conn)
    conn.close()
    return df

# MAPE calculation
def calculate_mape(df):
    df = df[df["actual"] != 0]  # avoid division by zero
    return np.mean(np.abs((df["actual"] - df["forecast"]) / df["actual"])) * 100

# RMSE calculation
def calculate_rmse(df):
    return np.sqrt(np.mean((df["actual"] - df["forecast"])**2))

# Plot Actual vs Forecast
def plot_forecast_vs_actual(df):
    plt.figure(figsize=(10, 5))
    for product in df["product"].unique():
        prod_df = df[df["product"] == product]
        plt.plot(prod_df["week"], prod_df["actual"], label=f"{product} - Actual", linestyle="--")
        plt.plot(prod_df["week"], prod_df["forecast"], label=f"{product} - Forecast")
    plt.xlabel("Week")
    plt.ylabel("Sales")
    plt.title("Forecast vs Actual Sales")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df_log = load_ems_log()
    print("\n--- Forecast Accuracy Metrics ---")
    print(f"MAPE: {calculate_mape(df_log):.2f}%")
    print(f"RMSE: {calculate_rmse(df_log):.2f}")
    print("\nPlotting Forecast vs Actual...")
    plot_forecast_vs_actual(df_log)

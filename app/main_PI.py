import os
import certifi
import warnings
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import re

# Setup
os.environ["SSL_CERT_FILE"] = certifi.where()
warnings.filterwarnings("ignore", category=RuntimeWarning)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import planner, actor

# --- Streamlit Config ---
st.set_page_config(page_title="CheeseCraft EMS", layout="wide")
st.title(" CheeseCraft EMS")

# --- Sidebar Inputs ---
st.sidebar.title(" EMS Controls")
product = st.sidebar.selectbox("Select Cheese Type:", ["Mozzarella", "Brie", "Cheddar"])
week = st.sidebar.number_input("Current Week Number", min_value=2, max_value=52, value=10)
actual_sales = st.sidebar.number_input(f"Actual Sales for Week {week}", min_value=1, value=1000)
weeks_ahead = st.sidebar.slider("Forecast Horizon (Weeks Ahead)", 1, 6, 4)

# --- Forecast Trigger ---
if st.sidebar.button(" Run EMS Forecast"):
    print("START ====>")
    forecast_table = planner.generate_multiweek_plan(
        product=product,
        current_week=week,
        actual_sales=actual_sales,
        weeks_ahead=weeks_ahead
    )

    st.success(" Forecast complete!")
    st.markdown(f"###  Forecast from Week {week + 1} to Week {week + weeks_ahead}")

    df = pd.DataFrame(forecast_table)[["week", "sales", "revenue", "profit", "inventory"]]
    df.columns = [
        "Week",
        "Forecasted Sales (Units)",
        "Forecasted Revenue ($)",
        "Forecasted Profit ($)",
        "Forecasted Inventory (Units)"
    ]

    with st.expander(" Forecast Table"):
        st.dataframe(df, use_container_width=True, hide_index=True)


    # --- EMS Recommendation ---
    st.markdown("###  EMS Recommendation")
    recommendation = actor.recommend_action(product, forecast_table)
    print("recommendation from main ===>",recommendation)
    st.markdown(recommendation)
    
# --- EMS Recommendation Table ---
    st.markdown("###  EMS Recommended Data")
    try:
        print("recommendation ====>",recommendation)
        ems_json = actor.ems_recommended_data(recommendation, forecast_table)
    
        # Clean LLM JSON output
        ems_json_clean = re.sub(r"```json|```|json", "", ems_json, flags=re.IGNORECASE)
        ems_json_clean = re.sub(r"//.*", "", ems_json_clean)
        ems_json_clean = re.sub(r",\s*}", "}", ems_json_clean)
        ems_json_clean = re.sub(r",\s*]", "]", ems_json_clean)
        ems_json_clean = ems_json_clean.replace("“", '"').replace("”", '"').replace("'", '"')
    
        # Convert to DataFrame
        df_final = pd.DataFrame(json.loads(ems_json_clean))
    
        # Rename columns with units
        df_final.columns = [
            "Week",
            "Forecasted Sales (Units)", "EMS Generated Sales (Units)",
            "Forecasted Revenue ($)", "EMS Generated Revenue ($)",
            "Forecasted Profit ($)", "EMS Generated Profit ($)",
            "Forecasted Inventory (Units)", "EMS Generated Inventory (Units)"
        ]
    
        # Round EMS generated numerical values to whole numbers
        columns_to_round = [
            "EMS Generated Sales (Units)",
            "EMS Generated Revenue ($)",
            "EMS Generated Profit ($)",
            "EMS Generated Inventory (Units)"
        ]
        for col in columns_to_round:
            if col in df_final.columns:
                df_final[col] = df_final[col].round(0).astype(int)
    
        # Show table
        st.dataframe(df_final, use_container_width=True, hide_index=True)
    
        # ---  Forecast vs EMS Generated Comparison ---
        st.markdown("###  Forecasted vs EMS Generated Comparison")
    
        comparison_metrics = [
            ("Forecasted Sales (Units)", "EMS Generated Sales (Units)", "Sales (Units)"),
            ("Forecasted Revenue ($)", "EMS Generated Revenue ($)", "Revenue ($)"),
            ("Forecasted Profit ($)", "EMS Generated Profit ($)", "Profit ($)"),
            ("Forecasted Inventory (Units)", "EMS Generated Inventory (Units)", "Inventory (Units)")
        ]
    
        fig, axs = plt.subplots(4, 1, figsize=(10, 14), sharex=True)
    
        for i, (forecast_col, ems_col, ylabel) in enumerate(comparison_metrics):
            axs[i].plot(df_final["Week"], df_final[forecast_col], label=forecast_col, marker="o")
            axs[i].plot(df_final["Week"], df_final[ems_col], label=ems_col, marker="s")
            axs[i].set_ylabel(ylabel, fontsize=11)
            axs[i].legend()
            axs[i].grid(True)
    
        axs[-1].set_xlabel("Week", fontsize=11)
        plt.tight_layout()
        st.pyplot(fig)
    
    except json.JSONDecodeError as e:
        st.error(f" JSON Decode Error: {str(e)}")
    except Exception as e:
        st.error(f" Unexpected Error: {str(e)}")
 
    # --- Power BI Integration ---
    st.markdown("###  Power BI Business Dashboard")
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=d3ee3fed-6862-419a-a4db-0f23ef36a628&autoAuth=true&ctid=8254186e-51ca-4454-8e78-0eb06dce7272"
    st.components.v1.iframe(powerbi_url, width=1100, height=700, scrolling=True)
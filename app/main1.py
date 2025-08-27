# import os
# import certifi
# import warnings
# import sys
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import json

# # Setup
# os.environ["SSL_CERT_FILE"] = certifi.where()
# warnings.filterwarnings("ignore", category=RuntimeWarning)
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import planner, actor
# from impact_estimator import parse_weekly_recommendations, estimate_weekly_impact

# # --- Streamlit Config ---
# st.set_page_config(page_title="CheeseCraft EMS", layout="wide")
# st.title("CheeseCraft EMS")

# # --- Sidebar Inputs ---
# st.sidebar.title("EMS Controls")
# product = st.sidebar.selectbox("Select Cheese Type:", ["Mozzarella", "Brie", "Cheddar"])
# week = st.sidebar.number_input("Current Week Number", min_value=2, max_value=52, value=10)
# actual_sales = st.sidebar.number_input(f"Actual Sales for Week {week}", min_value=1, value=1000)
# weeks_ahead = st.sidebar.slider("Forecast Horizon (Weeks Ahead)", 1, 6, 4)

# # --- Forecast Trigger ---
# if st.sidebar.button("Run EMS Forecast"):
#     forecast_table = planner.generate_multiweek_plan(
#         product=product,
#         current_week=week,
#         actual_sales=actual_sales,
#         weeks_ahead=weeks_ahead
#     )

#     st.success("Forecast complete!")
#     st.markdown(f"### Forecast from Week {week + 1} to Week {week + weeks_ahead}")

#     df_forecast = pd.DataFrame(forecast_table)
#     df_forecast_display = df_forecast.rename(columns={
#         "week": "Week",
#         "sales": "Forecasted Sales (Units)",
#         "revenue": "Forecasted Revenue ($)",
#         "profit": "Forecasted Profit ($)",
#         "inventory": "Forecasted Inventory (Units)"
#     })

#     with st.expander("Forecast Table"):
#         st.dataframe(df_forecast_display, use_container_width=True, hide_index=True)

#     # --- EMS Recommendation ---
#     st.markdown("### EMS Recommendation")
#     recommendation = actor.recommend_action(product, forecast_table)
#     st.text_area("LLM Generated Recommendations", recommendation, height=300)

#     # --- Apply EMS Recommendations to Forecast ---
#     st.markdown("### EMS Generated Forecast with Impact")
#     try:
#         ems_data = actor.ems_recommended_data(recommendation, forecast_table)
#         updated = ems_data.get("updated_forecast", []) if isinstance(ems_data, dict) else ems_data

#         if not isinstance(updated, list) or not all(isinstance(row, dict) for row in updated):
#             st.error("Invalid EMS forecast format")
#             st.stop()

#         df_updated = pd.DataFrame(updated)

#         # Merge original forecast for delta calculations
#         df_merged = df_forecast.merge(df_updated, on="week", suffixes=("_orig", "_ems"))

#         # Compute % impact
#         for metric in ["sales", "revenue", "profit", "inventory"]:
#             df_merged[f"{metric}_impact_pct"] = (
#                 (df_merged[f"{metric}_ems"] - df_merged[f"{metric}_orig"]) / df_merged[f"{metric}_orig"]
#             ) * 100

#         # Round values
#         for col in df_merged.columns:
#             if "_impact_pct" in col:
#                 df_merged[col] = df_merged[col].round(0).astype(int)
#             elif col.endswith("_orig") or col.endswith("_ems"):
#                 df_merged[col] = df_merged[col].round(0).astype(int)

#         # Rename columns
#         df_final = df_merged.rename(columns={
#             "week": "Week",
#             "sales_orig": "Forecasted Sales (Units)",
#             "sales_ems": "EMS Generated Sales (Units)",
#             "sales_impact_pct": "% Impact on Sales",
#             "revenue_orig": "Forecasted Revenue ($)",
#             "revenue_ems": "EMS Generated Revenue ($)",
#             "revenue_impact_pct": "% Impact on Revenue",
#             "profit_orig": "Forecasted Profit ($)",
#             "profit_ems": "EMS Generated Profit ($)",
#             "profit_impact_pct": "% Impact on Profit",
#             "inventory_orig": "Forecasted Inventory (Units)",
#             "inventory_ems": "EMS Generated Inventory (Units)",
#             "inventory_impact_pct": "% Impact on Inventory"
#         })

#         # Reorder columns for display
#         df_final = df_final[
#             [
#                 "Week",
#                 "Forecasted Sales (Units)", "EMS Generated Sales (Units)", "% Impact on Sales",
#                 "Forecasted Revenue ($)", "EMS Generated Revenue ($)", "% Impact on Revenue",
#                 "Forecasted Profit ($)", "EMS Generated Profit ($)", "% Impact on Profit",
#                 "Forecasted Inventory (Units)", "EMS Generated Inventory (Units)", "% Impact on Inventory"
#             ]
#         ]

#         st.dataframe(df_final, use_container_width=True, hide_index=True)

#         # --- Plot EMS Adjusted Trends ---
#         st.markdown("### Forecasted vs EMS Generated Comparison")
#         fig, axs = plt.subplots(4, 1, figsize=(10, 14), sharex=True)
#         y_labels = [
#             ("Forecasted Sales (Units)", "EMS Generated Sales (Units)"),
#             ("Forecasted Revenue ($)", "EMS Generated Revenue ($)"),
#             ("Forecasted Profit ($)", "EMS Generated Profit ($)"),
#             ("Forecasted Inventory (Units)", "EMS Generated Inventory (Units)")
#         ]

#         for i, (base, ems) in enumerate(y_labels):
#             axs[i].plot(df_final["Week"], df_final[base], label=base, marker="o")
#             axs[i].plot(df_final["Week"], df_final[ems], label=ems, marker="s")
#             axs[i].set_ylabel(base.split("(")[0].strip(), fontsize=11)
#             axs[i].legend()
#             axs[i].grid(True)

#         axs[-1].set_xlabel("Week", fontsize=11)
#         plt.tight_layout()
#         st.pyplot(fig)

#     except json.JSONDecodeError as e:
#         st.error(f"JSON Decode Error: {str(e)}")
#     except Exception as e:
#         st.error(f"Unexpected Error: {str(e)}")

#******************** with colour code*************************

import os
import certifi
import warnings
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# Setup
os.environ["SSL_CERT_FILE"] = certifi.where()
warnings.filterwarnings("ignore", category=RuntimeWarning)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import planner, actor
from impact_estimator import parse_weekly_recommendations, estimate_weekly_impact

# --- Streamlit Config ---
st.set_page_config(page_title="CheeseCraft EMS", layout="wide")
st.title("CheeseCraft EMS")

# --- Sidebar Inputs ---
st.sidebar.title("EMS Controls")
product = st.sidebar.selectbox("Select Cheese Type:", ["Mozzarella", "Brie", "Cheddar"])
week = st.sidebar.number_input("Current Week Number", min_value=2, max_value=52, value=10)
actual_sales = st.sidebar.number_input(f"Actual Sales for Week {week}", min_value=1, value=1000)
weeks_ahead = st.sidebar.slider("Forecast Horizon (Weeks Ahead)", 1, 6, 4)

# --- Forecast Trigger ---
if st.sidebar.button("Run EMS Forecast"):
    forecast_table = planner.generate_multiweek_plan(
        product=product,
        current_week=week,
        actual_sales=actual_sales,
        weeks_ahead=weeks_ahead
    )

    st.success("Forecast complete!")
    st.markdown(f"### Forecast from Week {week + 1} to Week {week + weeks_ahead}")

    df_forecast = pd.DataFrame(forecast_table)
    df_forecast_display = df_forecast.rename(columns={
        "week": "Week",
        "sales": "Forecasted Sales (Units)",
        "revenue": "Forecasted Revenue ($)",
        "profit": "Forecasted Profit ($)",
        "inventory": "Forecasted Inventory (Units)"
    })

    with st.expander("Forecast Table"):
        st.dataframe(df_forecast_display, use_container_width=True, hide_index=True)

    # --- EMS Recommendation ---
    st.markdown("### EMS Recommendation")
    recommendation = actor.recommend_action(product, forecast_table)
    st.text_area("LLM Generated Recommendations", recommendation, height=300)

    # --- Apply EMS Recommendations to Forecast ---
    st.markdown("### EMS Generated Forecast with Impact")
    try:
        ems_data = actor.ems_recommended_data(recommendation, forecast_table)
        updated = ems_data.get("updated_forecast", []) if isinstance(ems_data, dict) else ems_data

        if not isinstance(updated, list) or not all(isinstance(row, dict) for row in updated):
            st.error("Invalid EMS forecast format")
            st.stop()

        df_updated = pd.DataFrame(updated)

        # Merge original forecast for delta calculations
        df_merged = df_forecast.merge(df_updated, on="week", suffixes=("_orig", "_ems"))

        # Compute % impact
        for metric in ["sales", "revenue", "profit", "inventory"]:
            df_merged[f"{metric}_impact_pct"] = (
                (df_merged[f"{metric}_ems"] - df_merged[f"{metric}_orig"]) / df_merged[f"{metric}_orig"]
            ) * 100

        # Round values
        for col in df_merged.columns:
            if "_impact_pct" in col:
                df_merged[col] = df_merged[col].round(0).astype(int)
            elif col.endswith("_orig") or col.endswith("_ems"):
                df_merged[col] = df_merged[col].round(0).astype(int)

        # Rename columns
        df_final = df_merged.rename(columns={
            "week": "Week",
            "sales_orig": "Forecasted Sales (Units)",
            "sales_ems": "EMS Generated Sales (Units)",
            "sales_impact_pct": "% Impact on Sales",
            "revenue_orig": "Forecasted Revenue ($)",
            "revenue_ems": "EMS Generated Revenue ($)",
            "revenue_impact_pct": "% Impact on Revenue",
            "profit_orig": "Forecasted Profit ($)",
            "profit_ems": "EMS Generated Profit ($)",
            "profit_impact_pct": "% Impact on Profit",
            "inventory_orig": "Forecasted Inventory (Units)",
            "inventory_ems": "EMS Generated Inventory (Units)",
            "inventory_impact_pct": "% Impact on Inventory"
        })

        # Reorder columns for display
        df_final = df_final[
            [
                "Week",
                "Forecasted Sales (Units)", "EMS Generated Sales (Units)", "% Impact on Sales",
                "Forecasted Revenue ($)", "EMS Generated Revenue ($)", "% Impact on Revenue",
                "Forecasted Profit ($)", "EMS Generated Profit ($)", "% Impact on Profit",
                "Forecasted Inventory (Units)", "EMS Generated Inventory (Units)", "% Impact on Inventory"
            ]
        ]

        # Style: color impact values
        def highlight_impact(val):
            try:
                if int(val) > 0:
                    return "color: green"
                elif int(val) < 0:
                    return "color: red"
                else:
                    return ""
            except:
                return ""

        impact_cols = [
            "% Impact on Sales", "% Impact on Revenue",
            "% Impact on Profit", "% Impact on Inventory"
        ]

        styled_df = df_final.style.applymap(highlight_impact, subset=impact_cols)

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

        # --- Plot EMS Adjusted Trends ---
        st.markdown("### Forecasted vs EMS Generated Comparison")
        fig, axs = plt.subplots(4, 1, figsize=(10, 14), sharex=True)
        y_labels = [
            ("Forecasted Sales (Units)", "EMS Generated Sales (Units)"),
            ("Forecasted Revenue ($)", "EMS Generated Revenue ($)"),
            ("Forecasted Profit ($)", "EMS Generated Profit ($)"),
            ("Forecasted Inventory (Units)", "EMS Generated Inventory (Units)")
        ]

        for i, (base, ems) in enumerate(y_labels):
            axs[i].plot(df_final["Week"], df_final[base], label=base, marker="o")
            axs[i].plot(df_final["Week"], df_final[ems], label=ems, marker="s")
            axs[i].set_ylabel(base.split("(")[0].strip(), fontsize=11)
            axs[i].legend()
            axs[i].grid(True)

        axs[-1].set_xlabel("Week", fontsize=11)
        plt.tight_layout()
        st.pyplot(fig)

    except json.JSONDecodeError as e:
        st.error(f"JSON Decode Error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")

    # --- Power BI Integration ---
    st.markdown("###  Power BI Business Dashboard")
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=c771a16f-92aa-4f14-92d6-ce9f5ff6df2c&autoAuth=true&ctid=8254186e-51ca-4454-8e78-0eb06dce7272"
    st.components.v1.iframe(powerbi_url, width=1100, height=700, scrolling=True) 

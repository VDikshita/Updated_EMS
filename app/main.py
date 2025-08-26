



############################ WITH IMPACT CHART WORDS ********************************************************************************
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

#     df = pd.DataFrame(forecast_table)[["week", "sales", "revenue", "profit", "inventory"]]
#     df.columns = [
#         "Week",
#         "Forecasted Sales (Units)",
#         "Forecasted Revenue ($)",
#         "Forecasted Profit ($)",
#         "Forecasted Inventory (Units)"
#     ]

#     with st.expander("Forecast Table"):
#         st.dataframe(df, use_container_width=True, hide_index=True)

#     # --- EMS Recommendation ---
#     st.markdown("### EMS Recommendation")
#     recommendation = actor.recommend_action(product, forecast_table)
#     st.text_area("LLM Generated Recommendations", recommendation, height=300)

#     # --- Estimate Dynamic Impact Before Applying Actions ---
#     st.markdown("### Estimated Recommendation Impact")
#     parsed = parse_weekly_recommendations(recommendation)
#     for row in forecast_table:
#         w = row["week"]
#         if w in parsed:
#             impact = estimate_weekly_impact(
#                 {"sales": row["sales"], "revenue": row["revenue"]},
#                 parsed[w]["sales"] + parsed[w]["revenue"]
#             )
#             st.markdown(f"** Week {w}**")
#             st.markdown("**🔹 Sales Recommendations:**")
#             for s in parsed[w]["sales"]:
#                 st.markdown(f"- {s}")
#             st.markdown("**🔹 Revenue Recommendations:**")
#             for r in parsed[w]["revenue"]:
#                 st.markdown(f"- {r}")
#             st.markdown(f"**Sales Impact**: {impact['original_sales']} → {impact['adjusted_sales']} (+{impact['sales_impact']}%)")
#             st.markdown(f"**Revenue Impact**: ${impact['original_revenue']} → ${impact['adjusted_revenue']} (+{impact['revenue_impact']}%)")
#             st.markdown("---")

#     # --- Apply EMS Recommendations to Forecast ---
#     st.markdown("### EMS Recommended Data")
#     try:
#         ems_data = actor.ems_recommended_data(recommendation, forecast_table)

#         if isinstance(ems_data, dict):
#             updated = ems_data.get("updated_forecast", [])
#         elif isinstance(ems_data, list):
#             updated = ems_data
#         else:
#             st.error("Invalid EMS data structure")
#             st.stop()

#         if not isinstance(updated, list) or not all(isinstance(row, dict) for row in updated):
#             st.error("Error: 'updated_forecast' format is invalid.")
#             st.stop()

#         df_final = pd.DataFrame(updated)

#         df_final.rename(columns={
#             "week": "Week",
#             "sales": "EMS Adjusted Sales (Units)",
#             "revenue": "EMS Adjusted Revenue ($)",
#             "profit": "EMS Adjusted Profit ($)",
#             "inventory": "EMS Adjusted Inventory (Units)"
#         }, inplace=True)

#         for col in df_final.columns:
#             if "Units" in col or "$" in col:
#                 df_final[col] = df_final[col].round(0).astype(int)

#         st.dataframe(df_final, use_container_width=True, hide_index=True)

#         # --- Plot EMS Adjusted Trends ---
#         st.markdown("### EMS Forecast Adjustment Chart")
#         fig, axs = plt.subplots(4, 1, figsize=(10, 14), sharex=True)

#         y_labels = [
#             "EMS Adjusted Sales (Units)",
#             "EMS Adjusted Revenue ($)",
#             "EMS Adjusted Profit ($)",
#             "EMS Adjusted Inventory (Units)"
#         ]

#         for i, ylabel in enumerate(y_labels):
#             axs[i].plot(df_final["Week"], df_final[ylabel], marker="o")
#             axs[i].set_ylabel(ylabel, fontsize=11)
#             axs[i].grid(True)

#         axs[-1].set_xlabel("Week", fontsize=11)
#         plt.tight_layout()
#         st.pyplot(fig)

#         # --- Impact Analysis ---
#         st.markdown("### Impact Analysis Report")
#         impact_agent = actor.ImpactAnalysisAgent(
#             forecast_table_data=df_final.rename(columns={
#                 "Week": "week",
#                 "EMS Adjusted Sales (Units)": "sales",
#                 "EMS Adjusted Revenue ($)": "revenue",
#                 "EMS Adjusted Profit ($)": "profit",
#                 "EMS Adjusted Inventory (Units)": "inventory"
#             }).to_dict("records"),
#             action=recommendation
#         )
#         impact_data = impact_agent.apply_impact()
#         report = impact_agent.generate_impact_report(impact_data)
#         st.text_area("LLM-based Business Impact Summary:", report, height=350)

#     except json.JSONDecodeError as e:
#         st.error(f"JSON Decode Error: {str(e)}")
#     except Exception as e:
#         st.error(f"Unexpected Error: {str(e)}")



####### V1 : WITH REMOVING IMPACT ANALYSIS REPORT AND EXPLAINANTION*********

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
#     st.markdown("### EMS Adjusted Forecast with Impact")
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

#         # Round & rename
#         df_final = df_merged.rename(columns={
#             "week": "Week",
#             "sales_orig": "Forecasted Sales (Units)",
#             "sales_ems": "EMS Generated Sales (Units)",
#             "revenue_orig": "Forecasted Revenue ($)",
#             "revenue_ems": "EMS Generated Revenue ($)",
#             "profit_orig": "Forecasted Profit ($)",
#             "profit_ems": "EMS Generated Profit ($)",
#             "inventory_orig": "Forecasted Inventory (Units)",
#             "inventory_ems": "EMS Generated Inventory (Units)",
#             "sales_impact_pct": "Sales Impact (%)",
#             "revenue_impact_pct": "Revenue Impact (%)",
#             "profit_impact_pct": "Profit Impact (%)",
#             "inventory_impact_pct": "Inventory Impact (%)"
#         })

#         # Round numerical columns
#         for col in df_final.columns:
#             if "Units" in col or "$" in col:
#                 df_final[col] = df_final[col].round(0).astype(int)
#             elif "Impact (%)" in col:
#                 df_final[col] = df_final[col].round(1)

#         st.dataframe(df_final, use_container_width=True, hide_index=True)

#         # --- Plot EMS Adjusted Trends ---
#         st.markdown("### EMS Forecast Adjustment Chart")
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



####################### REORDER THE COLOUMN NAME IN EMS and without % imapct**********

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

        # Round & rename
        df_final = df_merged.rename(columns={
            "week": "Week",
            "sales_orig": "Forecasted Sales (Units)",
            "sales_ems": "EMS Generated Sales (Units)",
            "revenue_orig": "Forecasted Revenue ($)",
            "revenue_ems": "EMS Generated Revenue ($)",
            "profit_orig": "Forecasted Profit ($)",
            "profit_ems": "EMS Generated Profit ($)",
            "inventory_orig": "Forecasted Inventory (Units)",
            "inventory_ems": "EMS Generated Inventory (Units)"
        })

        #  Reorder columns as required
        df_final = df_final[
            [
                "Week",
                "Forecasted Sales (Units)", "EMS Generated Sales (Units)",
                "Forecasted Revenue ($)", "EMS Generated Revenue ($)",
                "Forecasted Profit ($)", "EMS Generated Profit ($)",
                "Forecasted Inventory (Units)", "EMS Generated Inventory (Units)"
            ]
        ]

        # Round numerical columns
        for col in df_final.columns:
            if "Units" in col or "$" in col:
                df_final[col] = df_final[col].round(0).astype(int)

        st.dataframe(df_final, use_container_width=True, hide_index=True)

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
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=63e476d5-fe7f-476f-ba79-912e8b7637b5&autoAuth=true&ctid=8254186e-51ca-4454-8e78-0eb06dce7272"
    st.components.v1.iframe(powerbi_url, width=1100, height=700, scrolling=True)    

# from app.utils import groq_llm, get_kb_context
# import json

# # Impact Analysis Agent Class
# class ImpactAnalysisAgent:
#     def __init__(self, forecast_table_data: list[dict], action: str):
#         self.forecast_table_data = forecast_table_data
#         self.action = action
    
#     def apply_impact(self):
#         """
#         Applies EMS strategy actions to forecast data and returns updated forecast along with impact analysis.
#         """
#         forecast_summary = "\n".join(
#             f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
#             f"Profit={entry['profit']}, Inventory={entry['inventory']}"
#             for entry in self.forecast_table_data
#         )

#         # Constructing the prompt for Groq-based LLM to calculate impact
#         prompt = f"""
# You are the EMS impact analysis agent for CheeseCraft Co.

# Here is the weekly forecast data:
# {forecast_summary}

# Here are the recommended business actions to apply:
# {self.action}

# Your task:
# 1. Apply the recommended actions to adjust the forecast data where necessary.
# 2. Update only relevant fields: Sales, Revenue, Profit, and Inventory for each week.
# 3. Calculate the expected impact of each action (as percentage changes).
# 4. Return a JSON object with two parts:
#    - "updated_forecast": Array of weekly records with original and adjusted values
#    - "impact_analysis": Summary of total impact across all weeks
# 5. Follow the core business rules for sales, inventory changes, pricing adjustments, and marketing.

# Required JSON structure:
# {{
#     "updated_forecast": [
#         {{
#             "week": <week number>,
#             "forecasted_sales": <original>,
#             "ems_sales": <adjusted>,
#             "sales_impact": <% change>,
#             "forecasted_revenue": <original>,
#             "ems_revenue": <adjusted>,
#             "revenue_impact": <% change>,
#             "forecasted_profit": <original>,
#             "ems_profit": <adjusted>,
#             "profit_impact": <% change>,
#             "forecasted_inventory": <original>,
#             "ems_inventory": <adjusted>
#         }} ,
#         ...
#     ],
#     "impact_analysis": {{
#         "total_sales_impact": <% cumulative change>,
#         "total_revenue_impact": <% cumulative change>,
#         "total_profit_impact": <% cumulative change>        
#     }}
# }}

# Output only the JSON string. Do not include any explanation, markdown, or comments.
# """
#         response = groq_llm(prompt)

#         # Parsing the response as JSON
#         try:
#             return json.loads(response)
#         except json.JSONDecodeError:
#             print("Failed to parse LLM response as JSON")
#             return {
#                 "updated_forecast": self.forecast_table_data,
#                 "impact_analysis": {}
#             }

#     def generate_impact_report(self, ems_data: dict) -> str:
#         """
#         Generates a human-readable impact report from the EMS-generated data
#         """
#         if not ems_data or "impact_analysis" not in ems_data:
#             return "No impact analysis data available"
        
#         impact = ems_data["impact_analysis"]
#         report = ["\nEMS Recommendation Impact Analysis Report"]
#         report.append("="*50)
        
#         # Summary metrics
#         report.append(f"Total Sales Impact: {impact.get('total_sales_impact', 0):.1f}%")
#         report.append(f"Total Revenue Impact: {impact.get('total_revenue_impact', 0):.1f}%")
#         report.append(f"Total Profit Impact: {impact.get('total_profit_impact', 0):.1f}%")
        
#         # Weekly breakdown
#         report.append("\nWeekly Breakdown:")
#         for week in ems_data.get("updated_forecast", []):
#             report.append(
#                 f"Week {week['week']}: "
#                 f"Sales {week.get('sales_impact', 0):+.1f}%, "
#                 f"Revenue {week.get('revenue_impact', 0):+.1f}%, "
#                 f"Profit {week.get('profit_impact', 0):+.1f}%"
#             )
        
#         # Key improvements
#         if "key_improvements" in impact:
#             report.append("\nKey Improvements Achieved:")
#             for i, improvement in enumerate(impact["key_improvements"][:3], 1):
#                 report.append(f"{i}. {improvement}")
        
#         return "\n".join(report)


# # Recommendation generation
# def recommend_action(product, forecast_table: list[dict]) -> str:
#     """
#     Generate business recommendations using multi-week forecast + Mozzarella strategy KB + outlier thresholds.
#     Input: forecast_table = list of forecast dicts (week, sales, revenue, profit, inventory)
#     """
#     strategy_kb = get_kb_context("mozzarella strategy")
#     outlier_kb = get_kb_context("outlier thresholds")

#     forecast_summary = "\n".join(
#         f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
#         f"Profit={entry['profit']}, Inventory={entry['inventory']}"
#         for entry in forecast_table
#     )

#     prompt = f"""
# You are the EMS strategist for CheeseCraft Co.

# Product: {product}

# Weekly Forecast Summary:
# {forecast_summary}

# Mozzarella Strategy (from internal KB):
# {strategy_kb}

# Outlier Thresholds (for anomaly detection):
# {outlier_kb}

# Task:
# - Analyze the weekly forecast and identify unusual patterns or optimization opportunities.
# - Recommend 4 actions for Sales and 4 actions for Revenue (e.g., price change, inventory adjustment, marketing, rerouting).
# - Each recommendation must include a clear reason and explicitly cite the relevant KB section number and title.
# - Ensure that Sales and Revenue trends are always considered in every recommendation.
# - Detect and act upon forecast anomalies using outlier thresholds.
# - Avoid repeating identical actions unless the justification and KB reference differ.
# - Give the actions and reasoning for sales and revenue increase.
# - Give the reason in 2-3 lines

# Format strictly like this:
# Week <week> Recommendation:
# - Action for Sales: <Your recommendation>
# - Expected Sales Impact: <+X% or -X%>
# - Action for Revenue: <Your recommendation>
# - Expected Revenue Impact: <+X% or -X%>
# - Reason: <Clear explanation based on forecast + KB rule. Must mention KB section number and title>

# Return only the week-wise recommendations. Do not add summaries or explanations.
# """
#     response = groq_llm(prompt)
#     return response


# # Applying EMS recommendations to forecast data
# def ems_recommended_data(action: str, forecast_table_data: list[dict]) -> dict:
#     """
#     Applies EMS strategy actions to the forecast table and returns:
#     - Updated weekly metrics
#     - Impact analysis comparing forecasted vs EMS-generated values
#     """
#     forecast_summary = "\n".join(
#         f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
#         f"Profit={entry['profit']}, Inventory={entry['inventory']}"
#         for entry in forecast_table_data
#     )

#     prompt = f"""
# You are the EMS action executor for CheeseCraft Co.

# Product: Mozzarella Cheese

# Here is the weekly forecast data:
# {forecast_summary}

# Here are the recommended business actions to apply:
# {action}

# Your task:
# 1. Apply the recommended actions to adjust the forecast data where necessary.
# 2. Update only relevant fields: Sales, Revenue, Profit, and Inventory for each week.
# 3. Calculate the expected impact of each action (as percentage changes).
# 4. Return a JSON object with two parts:
#    - "updated_forecast": Array of weekly records with original and adjusted values
#    - "impact_analysis": Summary of total impact across all weeks   
# """

#     response = groq_llm(prompt)
    
#     try:
#         return json.loads(response)
#     except json.JSONDecodeError:
#         print("Failed to parse LLM response as JSON")
#         return {
#             "updated_forecast": forecast_table_data,
#             "impact_analysis": {}
#         }

# # Example usage for integrating with your existing flow:
# # Step 1: Generate recommendations based on forecast
# recommendations = recommend_action(product, forecast_table)

# # Step 2: Apply recommendations to the forecast
# adjusted_forecast = ems_recommended_data(recommendations, forecast_table)

# # Step 3: Use Impact Analysis Agent to calculate the impact
# impact_agent = ImpactAnalysisAgent(adjusted_forecast["updated_forecast"], recommendations)
# impact_data = impact_agent.apply_impact()

# # Step 4: Generate and print impact report
# report = impact_agent.generate_impact_report(impact_data)
# print(report)


##################################### version 2***************************************

# from app.utils import groq_llm, get_kb_context
# import json

# class ImpactAnalysisAgent:
#     def __init__(self, forecast_table_data: list[dict], action: str):
#         self.forecast_table_data = forecast_table_data
#         self.action = action

#     def apply_impact(self):
#         """
#         Applies EMS strategy actions to forecast data and returns updated forecast along with impact analysis.
#         """
#         forecast_summary = "\n".join(
#             f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
#             f"Profit={entry['profit']}, Inventory={entry['inventory']}"
#             for entry in self.forecast_table_data
#         )

#         # Constructing the prompt for Groq-based LLM to calculate impact
#         prompt = f"""
#         You are the EMS impact analysis agent for CheeseCraft Co.
#         Here is the weekly forecast data:
#         {forecast_summary}
#         Here are the recommended business actions to apply:
#         {self.action}
        
#         Your task:
#         1. Apply the recommended actions to adjust the forecast data where necessary.
#         2. Update only relevant fields: Sales, Revenue, Profit, and Inventory for each week.
#         3. Calculate the expected impact of each action (as percentage changes).
#         4. Return a JSON object with two parts:
#            - "updated_forecast": Array of weekly records with original and adjusted values
#            - "impact_analysis": Summary of total impact across all weeks
#         """
#         response = groq_llm(prompt)
#         print("impact analysis agent response==>",response)

#         # Parsing the response as JSON
#         try:
#             return json.loads(response)
#         except json.JSONDecodeError:
#             print("Failed to parse LLM response as JSON")
#             return {
#                 "updated_forecast": self.forecast_table_data,
#                 "impact_analysis": {}
#             }

#     def generate_impact_report(self, ems_data: dict) -> str:
#         """
#         Generates a human-readable impact report from the EMS-generated data
#         """
#         if not ems_data or "impact_analysis" not in ems_data:
#             return "No impact analysis data available"

#         impact = ems_data["impact_analysis"]
#         report = ["\nEMS Recommendation Impact Analysis Report"]
#         report.append("="*50)

#         # Summary metrics
#         report.append(f"Total Sales Impact: {impact.get('total_sales_impact', 0):.1f}%")
#         report.append(f"Total Revenue Impact: {impact.get('total_revenue_impact', 0):.1f}%")
#         report.append(f"Total Profit Impact: {impact.get('total_profit_impact', 0):.1f}%")

#         # Weekly breakdown
#         report.append("\nWeekly Breakdown:")
#         for week in ems_data.get("updated_forecast", []):
#             report.append(
#                 f"Week {week['week']}: "
#                 f"Sales Impact: {week.get('sales_impact', 0):+.1f}%, "
#                 f"Revenue Impact: {week.get('revenue_impact', 0):+.1f}%, "
#                 f"Profit Impact: {week.get('profit_impact', 0):+.1f}%"
#             )

#         return "\n".join(report)

# # Recommendation generation
# def recommend_action(product, forecast_table: list[dict]) -> str:
#     """
#     Generate business recommendations using multi-week forecast + Mozzarella strategy KB + outlier thresholds.
#     Input: forecast_table = list of forecast dicts (week, sales, revenue, profit, inventory)
#     """
#     strategy_kb = get_kb_context("mozzarella strategy")
#     outlier_kb = get_kb_context("outlier thresholds")

#     forecast_summary = "\n".join(
#         f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
#         f"Profit={entry['profit']}, Inventory={entry['inventory']}"
#         for entry in forecast_table
#     )

#     prompt = f"""
#     You are the EMS strategist for CheeseCraft Co.
#     Product: {product}
#     Weekly Forecast Summary:
#     {forecast_summary}
#     Mozzarella Strategy (from internal KB):
#     {strategy_kb}
#     Outlier Thresholds (for anomaly detection):
#     {outlier_kb}
    
#     Task:
#     - Analyze the weekly forecast and identify unusual patterns or optimization opportunities.
#     - Recommend 4 actions for Sales and 4 actions for Revenue (e.g., price change, inventory adjustment, marketing, rerouting).
#     - Each recommendation must include a clear reason and explicitly cite the relevant KB section number and title.
#     - Ensure that Sales and Revenue trends are always considered in every recommendation.
#     - Detect and act upon forecast anomalies using outlier thresholds.
#     - Avoid repeating identical actions unless the justification and KB reference differ.
#     - Give the actions and reasoning for sales and revenue increase.
#     - Give the reason in 2-3 lines
    
#     Return only the week-wise recommendations. Do not add summaries or explanations.
#     """
#     response = groq_llm(prompt)
#     return response

# # Applying EMS recommendations to forecast data
# def ems_recommended_data(action: str, forecast_table_data: list[dict]) -> dict:
#     """
#     Applies EMS strategy actions to the forecast table and returns:
#     - Updated weekly metrics
#     - Impact analysis comparing forecasted vs EMS-generated values
#     """
#     forecast_summary = "\n".join(
#         f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
#         f"Profit={entry['profit']}, Inventory={entry['inventory']}"
#         for entry in forecast_table_data
#     )

#     prompt = f"""
#     You are the EMS action executor for CheeseCraft Co.
#     Product: Mozzarella Cheese
#     Here is the weekly forecast data:
#     {forecast_summary}
#     Here are the recommended business actions to apply:
#     {action}
    
#     Your task:
#     1. Apply the recommended actions to adjust the forecast data where necessary.
#     2. Update only relevant fields: Sales, Revenue, Profit, and Inventory for each week.
#     3. Calculate the expected impact of each action (as percentage changes).
#     4. Return a JSON object with two parts:
#        - "updated_forecast": Array of weekly records with original and adjusted values
#        - "impact_analysis": Summary of total impact across all weeks   
#     """
#     response = groq_llm(prompt)
    
#     try:
#         return json.loads(response)
#     except json.JSONDecodeError:
#         print("Failed to parse LLM response as JSON")
#         return {
#             "updated_forecast": forecast_table_data,
#             "impact_analysis": {}
#         }




from app.utils import groq_llm, get_kb_context
import json

class ImpactAnalysisAgent:
    def __init__(self, forecast_table_data: list[dict], action: str):
        self.forecast_table_data = forecast_table_data
        self.action = action

    def apply_impact(self):
        forecast_summary = "\n".join(
            f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
            f"Profit={entry['profit']}, Inventory={entry['inventory']}"
            for entry in self.forecast_table_data
        )

        prompt = f"""
        You are the EMS impact analysis agent for CheeseCraft Co.
        Weekly Forecast:
        {forecast_summary}

        Actions to apply:
        {self.action}

        Your task:
        1. Apply actions to adjust forecast.
        2. Return updated_forecast and impact_analysis.
        Format: JSON with updated_forecast & impact_analysis keys.
        """
        response = groq_llm(prompt)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "updated_forecast": self.forecast_table_data,
                "impact_analysis": {}
            }

    def generate_impact_report(self, ems_data: dict) -> str:
        if not ems_data or "impact_analysis" not in ems_data:
            return "No impact analysis available."

        impact = ems_data["impact_analysis"]
        report = ["\n EMS Recommendation Impact Analysis"]
        report.append("=" * 50)

        report.append(f"Total Sales Impact: {impact.get('total_sales_impact', 0):.1f}%")
        report.append(f"Total Revenue Impact: {impact.get('total_revenue_impact', 0):.1f}%")
        report.append(f"Total Profit Impact: {impact.get('total_profit_impact', 0):.1f}%")

        report.append("\nWeekly Breakdown:")
        for week in ems_data.get("updated_forecast", []):
            report.append(
                f"Week {week['week']}: Sales Impact: {week.get('sales_impact', 0):+.1f}%, "
                f"Revenue Impact: {week.get('revenue_impact', 0):+.1f}%, "
                f"Profit Impact: {week.get('profit_impact', 0):+.1f}%"
            )
        return "\n".join(report)


def recommend_action(product, forecast_table: list[dict]) -> str:
    strategy_kb = get_kb_context("mozzarella strategy")
    outlier_kb = get_kb_context("outlier thresholds")

    forecast_summary = "\n".join(
        f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
        f"Profit={entry['profit']}, Inventory={entry['inventory']}"
        for entry in forecast_table
    )

    prompt = f"""
    You are the EMS strategist for CheeseCraft Co.
    Product: {product}
    Forecast:
    {forecast_summary}

    Mozzarella Strategy:
    {strategy_kb}

    Outlier Thresholds:
    {outlier_kb}

    Task:
    - Recommend 4 actions for Sales and 4 for Revenue per week.
    - Avoid contradictions. Cite KB sections.
    - Give actionable results.
    - Format per week:
      Week <week> Recommendation:
      - Action for sale: ...
      - Action for Revenue: ...
      - Reason: ... (mention KB section)
    Return only recommendations.
    """
    return groq_llm(prompt)


def ems_recommended_data(action: str, forecast_table_data: list[dict]) -> dict:
    forecast_summary = "\n".join(
        f"Week {entry['week']}: Sales={entry['sales']}, Revenue={entry['revenue']}, "
        f"Profit={entry['profit']}, Inventory={entry['inventory']}"
        for entry in forecast_table_data
    )

    # prompt = f"""
    # You are the EMS action executor for CheeseCraft Co.
    # Forecast:
    # {forecast_summary}
    # Actions:
    # {action}

    # Your Task:
    # 1. Apply recommended actions to forecast.
    # 2. Return a list of updated records as JSON with:
    #    - week, sales, revenue, profit, inventory.
    # 3. Do NOT add markdown or comments.
    # """

    prompt = f"""
You are the EMS action executor for CheeseCraft Co.

Forecast:
{forecast_summary}

Actions:
{action}

Your Task:
1. Apply the recommended actions to adjust the forecast.
2. Update the following fields per week: sales, revenue, profit, and inventory.
3. Inventory should reflect expected demand and must increase if sales are projected to rise.
4. Return a list of JSON records. Each record must include:
   - week
   - sales
   - revenue
   - profit
   - inventory
5. Do not return any markdown or explanation. Only return a clean JSON list.
6. Do not change the unit price unless pricing-related action is explicitly present.

"""

    response = groq_llm(prompt)

    try:
        parsed = json.loads(response)
        return {"updated_forecast": parsed} if isinstance(parsed, list) else parsed
    except json.JSONDecodeError:
        return {"updated_forecast": forecast_table_data}


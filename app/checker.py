##################### version 1 ; solving underperformed issue
# from app.utils import compute_dynamic_threshold, smart_threshold
# import pandas as pd

# def analyze_deviation(product, week, actual, forecast):
#     # ✅ Edge Case: Avoid divide by zero
#     if forecast == 0:
#         return 0, " Forecast is zero; deviation cannot be computed."

#     # 🔢 Deviation calculation
#     diff = actual - forecast
#     pct = (diff / forecast) * 100

#     #  Dynamic threshold (ensemble method)
#     threshold = smart_threshold(product, week)

#     #  Fallback if threshold is missing or broken
#     if threshold is None or not isinstance(threshold, (int, float)) or pd.isna(threshold):
#         threshold = 10.0  # fallback

#     # Deviation Interpretation
#     if abs(pct) < threshold:
#         status = f"Sales are within ±{threshold:.1f}% of forecast. No major deviation."
#     elif pct > threshold:
#         status = f"Sales exceeded forecast by {pct:.2f}% (above {threshold:.1f}% threshold)."
#     else:
#         status = f"Sales underperformed by {abs(pct):.2f}% (below {threshold:.1f}% threshold)."

#     return pct, status




###### Version3 : for sales, revenue.profit and inventory for 3-4 weeks(multiweek)
from app.utils import compute_dynamic_threshold, smart_threshold
import pandas as pd

# Default thresholds (can be refined or replaced with LLM-based or smart logic)
DEFAULT_THRESHOLDS = {
    "sales": 10.0,
    "revenue": 12.0,
    "profit": 15.0,
    "inventory": 10.0
}

def compute_deviation(actual, forecast):
    if forecast == 0:
        return 0, "Forecast is zero; deviation cannot be computed."
    pct = ((actual - forecast) / forecast) * 100
    return pct, ""

def analyze_multi_deviation(product, week, actuals: dict, forecasts: dict):
    """
    Compare actual vs forecast for all 4 metrics.
    Returns: dict of deviations + summary text
    """
    summary = []
    deviations = {}

    for metric in ["sales", "revenue", "profit", "inventory"]:
        actual = actuals.get(metric, 0)
        forecast = forecasts.get(metric, 0)

        pct, msg = compute_deviation(actual, forecast)

        # Use dynamic threshold for sales, static for others
        threshold = smart_threshold(product, week) if metric == "sales" else DEFAULT_THRESHOLDS[metric]

        if msg:
            summary.append(f" {metric.capitalize()}: {msg}")
        elif abs(pct) < threshold:
            pass  # within acceptable range — skip
        elif pct > threshold:
            summary.append(f"{metric.capitalize()} exceeded forecast by {pct:.2f}% (>{threshold}%)")
        else:
            summary.append(f"{metric.capitalize()} underperformed by {abs(pct):.2f}% (<-{threshold}%)")

        deviations[metric] = round(pct, 2)

    if not summary:
        summary.append(" All metrics are within acceptable deviation thresholds.")

    return deviations, "\n".join(summary)

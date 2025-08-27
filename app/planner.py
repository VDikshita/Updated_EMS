
## version A2
# planner.py
from pathlib import Path
import pandas as pd
import joblib

# --- Paths (robust) ---
HERE = Path(__file__).resolve().parent            # .../Updated_EMS/app
ROOT = HERE.parent                                 # .../Updated_EMS
MODELS_DIR = HERE / "models"                       # app/models
DATA_CSV = ROOT / "data" / "historical_sales_enriched_final_ready.csv"

def _load_model(name: str):
    p = MODELS_DIR / name
    if not p.exists():
        avail = "\n".join(f"- {x.name}" for x in MODELS_DIR.glob("*.pkl"))
        raise FileNotFoundError(
            f"Missing model file: {p}\nModels folder: {MODELS_DIR}\nAvailable:\n{avail or '(none)'}"
        )
    return joblib.load(p)

# --- Load trained models ---
model_sales = _load_model("model_sales_1.pkl")
# If you actually have/need a revenue model, uncomment next line and add it below.
# model_revenue = _load_model("model_revenue_1.pkl")
model_profit = _load_model("model_profit.pkl")
model_inventory = _load_model("model_inventory.pkl")

# --- Load historical data ---
if not DATA_CSV.exists():
    raise FileNotFoundError(f"Data CSV not found at: {DATA_CSV}")
df = pd.read_csv(DATA_CSV)

def get_season_from_week(week: int) -> str:
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
    unit_price = 7.5  # fixed price used for revenue

    for i in range(1, weeks_ahead + 1):
        week = current_week + i

        # lag features
        lag_1 = forecasts[-1]["sales"] if forecasts else actual_sales
        if len(forecasts) >= 2:
            lag_2 = forecasts[-2]["sales"]
        elif not df[df["week"] == current_week - 1].empty:
            lag_2 = df.loc[df["week"] == current_week - 1, "sales"].values[0]
        else:
            lag_2 = actual_sales

        # feature row
        row = pd.DataFrame([{
            "week": week,
            "product": product,
            "price": unit_price,
            "promotion_flag": 0,
            "season": get_season_from_week(week),
            "month": ((week - 1) // 4 + 1),
            "lag_1_sales": lag_1,
            "lag_2_sales": lag_2
        }])

        # one-hot encode + align to model features
        x = pd.get_dummies(row)
        # ensure all expected columns exist
        for model in (model_sales, model_profit, model_inventory):
            for col in model.feature_names_in_:
                if col not in x:
                    x[col] = 0
        # order columns to match the sales model (others share same schema)
        x = x[model_sales.feature_names_in_]

        # predictions
        sales = int(model_sales.predict(x)[0])
        revenue = int(sales * unit_price)  # using fixed price
        profit = int(model_profit.predict(x)[0])
        inventory = int(model_inventory.predict(x)[0])

        forecasts.append({
            "week": week,
            "sales": sales,
            "revenue": revenue,
            "profit": profit,
            "inventory": inventory
        })

    return forecasts

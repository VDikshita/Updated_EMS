import re

def parse_weekly_recommendations(recommendation_text: str) -> dict:
    week_pattern = re.compile(r"Week (\d+):")
    current_week = None
    section = None
    result = {}

    for line in recommendation_text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = week_pattern.match(line)
        if match:
            current_week = int(match.group(1))
            result[current_week] = {"sales": [], "revenue": []}
            section = None
        elif "Sales:" in line:
            section = "sales"
        elif "Revenue:" in line:
            section = "revenue"
        elif section and current_week:
            result[current_week][section].append(line)

    return result


def estimate_weekly_impact(original: dict, recommendations: list) -> dict:
    sales = original["sales"]
    revenue = original["revenue"]

    sales_boost = 1 + 0.04 * len([r for r in recommendations if "Sales" in r or "marketing" in r.lower()])
    revenue_boost = 1 + 0.035 * len([r for r in recommendations if "Revenue" in r or "price" in r.lower()])

    return {
        "original_sales": sales,
        "original_revenue": revenue,
        "adjusted_sales": int(sales * sales_boost),
        "adjusted_revenue": int(revenue * revenue_boost),
        "sales_impact": round((sales_boost - 1) * 100, 1),
        "revenue_impact": round((revenue_boost - 1) * 100, 1)
    }

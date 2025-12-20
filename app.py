from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from calculation import calculate_furniture_depreciation, property_investment_calculator

app = Flask(__name__, static_folder="static", template_folder="templates")


def build_furniture_items(
    furniture_table: list[dict],
    lifespan_kitchen: float,
    lifespan_appliances: float,
    lifespan_furniture: float,
) -> dict[str, tuple[float, float]]:
    items: dict[str, tuple[float, float]] = {}
    lifespan_map = {
        "kitchen": lifespan_kitchen,
        "appliances": lifespan_appliances,
        "furniture": lifespan_furniture,
    }
    for item in furniture_table or []:
        name = str(item.get("name", "")).strip()
        value = item.get("value")
        category = item.get("category", "furniture")
        if name and value not in (None, ""):
            items[name] = (float(value), float(lifespan_map.get(category, 0)))
    return items


def get_float(data: dict, key: str, default: float = 0.0) -> float:
    value = data.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/api/furniture-depreciation")
def furniture_depreciation() -> tuple[str, int] | str:
    data = request.get_json() or {}
    items = data.get("items", [])
    lifespans = data.get("lifespans", {})
    furniture_items = build_furniture_items(
        items,
        lifespan_kitchen=get_float(lifespans, "kitchen", 10),
        lifespan_appliances=get_float(lifespans, "appliances", 5),
        lifespan_furniture=get_float(lifespans, "furniture", 10),
    )
    depreciation_method = data.get("method", "berlin")
    depreciation_value = calculate_furniture_depreciation(
        method=depreciation_method, items=furniture_items
    )
    total_cost = sum(value for value, _ in furniture_items.values())
    return jsonify({"depreciation": depreciation_value, "total_cost": total_cost})


@app.post("/api/simulate")
def simulate() -> tuple[str, int] | str:
    data = request.get_json() or {}

    furnishing_option = data.get("furnishing_option", "unfurnished")
    furniture_table = data.get("furniture_table", [])
    furniture_items = None
    if furnishing_option == "furnished":
        furniture_items = build_furniture_items(
            furniture_table,
            lifespan_kitchen=get_float(data, "lifespan_kitchen", 10),
            lifespan_appliances=get_float(data, "lifespan_appliances", 5),
            lifespan_furniture=get_float(data, "lifespan_furniture", 10),
        )

    result = property_investment_calculator(
        purchase_price=get_float(data, "purchase_price", 300000),
        mortgage_rate=get_float(data, "mortgage_rate", 4) / 100,
        loan_percentage=get_float(data, "loan_percentage", 100) / 100,
        rental_income_monthly=get_float(data, "rental_income_monthly", 1500),
        hausgeld_monthly=get_float(data, "hausgeld_monthly", 300),
        grundsteuer_yearly=get_float(data, "grundsteuer_yearly", 400),
        maintenance_reserve_per_sqm_yearly=get_float(
            data, "maintenance_reserve_per_sqm_yearly", 0
        ),
        apartment_size_sqm=get_float(data, "apartment_size_sqm", 60),
        salary_income=get_float(data, "salary_income", 6400 * 12),
        monthly_expenses=get_float(data, "monthly_expenses", 2000),
        salary_increase_rate=get_float(data, "salary_increase_rate", 2) / 100,
        years=int(get_float(data, "years", 32)),
        vacancy_rate=get_float(data, "vacancy_rate", 2) / 100,
        property_transfer_tax_rate=get_float(data, "property_transfer_tax_rate", 6)
        / 100,
        provision_rate=get_float(data, "provision_rate", 3.57) / 100,
        notary_fee_rate=get_float(data, "notary_fee_rate", 1.5) / 100,
        grundbuch_fee_rate=get_float(data, "grundbuch_fee_rate", 0.5) / 100,
        renovation_costs=get_float(data, "renovation_costs", 5000),
        depreciation_rate=get_float(data, "depreciation_rate", 2) / 100,
        land_value_per_sqm=get_float(data, "land_value_per_sqm", 1100),
        rental_increase_rate=get_float(data, "rental_increase_rate", 2) / 100,
        savings_interest_rate=get_float(data, "savings_interest_rate", 0) / 100,
        furniture_items=furniture_items,
        furniture_depreciation_method=data.get("depreciation_method", "berlin"),
    )

    figure = result["figure"].to_plotly_json()
    summary = {key: value for key, value in result.items() if key != "figure"}

    return jsonify({"figure": figure, "summary": summary})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

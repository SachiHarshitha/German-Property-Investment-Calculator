import random

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL
from werkzeug.debug import Console
from collections import defaultdict

from calculation import property_investment_calculator
from controls import create_input, create_slider

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dynamic Property Comparison"


def property_inputs(prefix):
    return dbc.Card(
        [
            html.H5(f"🏠 Property {prefix.upper()}", className="card-title"),
            html.Div([
                create_input("Purchase Price (€)", {"type": "input", "property": prefix, "field": "price"}, 300000),
                create_input("Apartment Size (sqm)", {"type": "input", "property": prefix, "field": "size"}, 60),
                create_input("Hausgeld Monthly (€)", {"type": "input", "property": prefix, "field": "hausgeld"}, 300),
                create_input("Renovation Cost", {"type": "input", "property": prefix, "field": "renovation"}, 0),
                create_input("Rental Income Monthly (€)", {"type": "input", "property": prefix, "field": "rent"}, 1200),
                create_input("Grundsteuer Yearly (€)", {"type": "input", "property": prefix, "field": "tax"}, 400),
                create_input("Land Value per sqm (€)", {"type": "input", "property": prefix, "field": "land_value"}, 1100),
                create_input("Maintenance Reserve (€/sqm/year)", {"type": "input", "property": prefix, "field": "maintenance_reserve"}, 0),
                create_slider("Transfer Tax Rate (%)", {"type": "slider", "property": prefix, "field": "transfer_tax_rate"}, 0, 10, 0.1, 6),
                create_slider("Provision Rate (%)", {"type": "slider", "property": prefix, "field": "provision_rate"}, 0, 10, 0.1, 3.57),
                create_slider("Notary Fee Rate (%)", {"type": "slider", "property": prefix, "field": "notary_fee"}, 0, 5, 0.1, 1.5),
                create_slider("Grundbuch Fee Rate (%)", {"type": "slider", "property": prefix, "field": "grundbuch_fee"}, 0, 5, 0.1, 0.5),
            ]),
        ],
        body=True,
        style={
            "flex": "1 1 300px",  # Each card takes equal width (min 300px)
            "minWidth": "300px",  # Cards won't shrink below this width
            "margin": "5px"  # Optional margin
        }
    )


def shared_inputs():
    return dbc.Card([
        html.H5("📊 Shared Inputs", className="card-title"),
        html.Div([
            create_input("Salary Income (€/year)", "salary", 5000 * 12),
            create_input("Monthly Expenses (€)", "expenses", 2000),
            create_input("Mortgage Rate (%)", "rate", 4, 0.1),
            create_input("Loan Percentage (%)", "loan_pct", 100, 1),
            create_input("Simulation Years", "years", 30),
        ])
    ], body=True)


def summary_card(label, result):
    return dbc.Card(
        [
            html.H5(label, className="card-title"),
            dcc.Graph(figure=result["figure"]),
            html.Ul([
                html.Li(f"Net Wealth: €{result['Net Wealth With Property']:.2f}"),
                html.Li(f"Property Value: €{result['Property Value']:.2f}"),
                html.Li(f"Loan Balance: €{result['Loan Balance']:.2f}"),
                html.Li(f"Monthly Loan Payment: €{result['Monthly Loan Payment (Annuität)']:.2f}"),
                html.Li(f"Cashflow (Last Year): €{result['Operating Cashflow (Last Year)']:.2f}"),
                html.Li(f"Tax Paid (Last Year): €{result['Tax Paid With Property (Last Year)']:.2f}"),
                html.Li(
                    f"📐 Wealth Delta: €{result['Net Wealth With Property'] - result['Net Wealth Without Property']:.2f}"),
                html.Li(f"ROI: {result['ROI']}"),
                html.Li(f"IRR: {result['IRR']}%"),
            ]),
        ],
        body=True,
        style={
            "flex": "1 1 300px",
            "minWidth": "300px",
            "margin": "5px"
        }
    )


app.layout = dbc.Container([
    html.H2("📈 Property Investment Comparison"),
    dcc.Store(id="property-store", data=["a", "b"]),
    dbc.Button("➕ Add Property", id="add-btn", color="success", style={"marginRight": "10px"}),
    dbc.Button("➖ Remove Property", id="remove-btn", color="danger"),
    html.Br(), html.Br(),
    html.Div(id="property-inputs-container"),
    shared_inputs(),
    html.Br(),
    dbc.Button("Compare Properties", id="compare_btn", color="primary"),
    html.Br(), html.Div(id="results-container")
], fluid=True)


@app.callback(
    Output("property-store", "data"),
    Input("add-btn", "n_clicks"),
    Input("remove-btn", "n_clicks"),
    State("property-store", "data"),
    prevent_initial_call=True
)
def modify_property_list(add_clicks, remove_clicks, current):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "add-btn":
        new_id = chr(ord(max(current)) + 1) if current else "a"
        return current + [new_id]
    elif button_id == "remove-btn" and len(current) > 1:
        return current[:-1]
    return current


@app.callback(
    Output("property-inputs-container", "children"),
    Input("property-store", "data")
)
def render_properties(properties):
    cards = [property_inputs(pid) for pid in properties]
    return html.Div(cards, style={
        "display": "flex",
        "flexWrap": "wrap",
        "gap": "10px",  # Optional spacing between cards
    })


@app.callback(
    Output("results-container", "children"),
    Input("compare_btn", "n_clicks"),
    State("property-store", "data"),
    State({"type": "input", "property": ALL, "field": ALL}, "value"),
    State({"type": "slider", "property": ALL, "field": ALL}, "value"),
    State("salary", "value"),
    State("expenses", "value"),
    State("rate", "value"),
    State("loan_pct", "value"),
    State("years", "value"),
)
def compare_dynamic_properties(n, prop_ids, input_values, slider_values, salary, expenses, rate, loan_pct, years):
    if not n:
        return ""

    # Dash States for input and slider values
    states_inputs = dash.callback_context.states_list[1]  # instead of inputs_list
    states_sliders = dash.callback_context.states_list[2]

    # Make sure these are always present
    if not states_inputs:
        states_inputs = []
    if not states_sliders:
        states_sliders = []

    # Now you can safely iterate over them
    from collections import defaultdict


    inputs = defaultdict(dict)
    for i, id_dict in enumerate(states_inputs):
        inputs[id_dict['id']["property"]][id_dict['id']["field"]] = input_values[i]
    for i, id_dict in enumerate(states_sliders):
        inputs[id_dict['id']["property"]][id_dict['id']["field"]] = slider_values[i]

    inflation_rates = [random.gauss(0.02, 0.01) for _ in range(years)]
    appreciation_rates = [random.uniform(-0.01, 0.07) for _ in range(years)]
    common = {
        "mortgage_rate": rate / 100,
        "loan_percentage": loan_pct / 100,
        "salary_income": salary,
        "monthly_expenses": expenses,
        "years": years,
        "inflation_rates": inflation_rates,
        "appreciation_rates": appreciation_rates,
    }

    cards = []
    for pid in prop_ids:
        print(f"pid: {pid}")
        transfer_tax_rate = inputs[f"transfer_tax_{pid}"]
        print(f"transfer_tax_rate: {transfer_tax_rate}")
        provision_rate = inputs[f"provision_{pid}"]
        print(f"provision_rate: {provision_rate}")
        notary_fee_rate = inputs[f"notary_{pid}"]
        print(f"notary_fee_rate: {notary_fee_rate}")
        grundbuch_fee_rate = inputs[f"grundbuch_{pid}"]
        print(f"grundbuch_fee_rate: {grundbuch_fee_rate}")
        hausgeld = inputs[f"hausgeld_{pid}"]
        print(f"hausgeld: {hausgeld}")
        params = {
            "purchase_price": inputs[pid]["price"],
            "rental_income_monthly": inputs[pid]["rent"],
            "apartment_size_sqm": inputs[pid]["size"],
            "hausgeld_monthly": inputs[pid]["hausgeld"],
            "grundsteuer_yearly": inputs[pid]["tax"],
            "land_value_per_sqm": inputs[pid]["land_value"],
            "renovation_costs": inputs[pid]["renovation"],
            "property_transfer_tax_rate": inputs[pid]["transfer_tax_rate"] / 100,
            "provision_rate": inputs[pid]["provision_rate"] / 100,
            "notary_fee_rate": inputs[pid]["notary_fee"] / 100,
            "grundbuch_fee_rate": inputs[pid]["grundbuch_fee"] / 100,
            "maintenance_reserve_per_sqm_yearly": inputs[pid]["maintenance_reserve"],
            **common,
        }
        result = property_investment_calculator(**params)
        card = dbc.Card([
            html.H5(f"📄 Property {pid.upper()} Results"),
            dcc.Graph(figure=result["figure"]),
            html.Ul([
                html.Li(f"Net Wealth: €{result['Net Wealth With Property']:.2f}"),
                html.Li(f"Property Value: €{result['Property Value']:.2f}"),
                html.Li(f"Loan Balance: €{result['Loan Balance']:.2f}"),
                html.Li(f"Monthly Loan Payment: €{result['Monthly Loan Payment (Annuität)']:.2f}"),
                html.Li(f"Cashflow (Last Year): €{result['Operating Cashflow (Last Year)']:.2f}"),
                html.Li(f"Tax Paid (Last Year): €{result['Tax Paid With Property (Last Year)']:.2f}"),
                html.Li(
                    f"📐 Wealth Delta: €{result['Net Wealth With Property'] - result['Net Wealth Without Property']:.2f}"),
                html.Li(f"ROI: {result['ROI']}"),
                html.Li(f"IRR: {result['IRR']}%"),
            ])
        ],body=True, style={
    "flex": "1 1 300px",  # Make cards expand to available space
    "minWidth": "300px",
    "margin": "5px"
})
        cards.append(card)

    # Wrap all cards in a flex container
    return html.Div(
        cards,
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": "10px",
            "marginTop": "10px",
        },
    )



if __name__ == "__main__":
    app.run(debug=True)

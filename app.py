from flask import Flask, render_template, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'merger_model_secret_2024'

# --- Pre-built Deal Templates ---
TEMPLATES = {
    'tech_acquisition': {
        'name': 'Tech Acquisition (Large Cap)',
        'acquirer': {'Revenue': 50000, 'EBITDA': 15000, 'Net_Income': 10000, 'Shares_Outstanding': 2000, 'Share_Price': 150, 'Debt': 20000, 'Cash': 8000, 'Tax_Rate': 0.21},
        'target':   {'Revenue': 12000, 'EBITDA': 3500,  'Net_Income': 2000,  'Shares_Outstanding': 500,  'Share_Price': 80,  'Debt': 2000,  'Cash': 1500, 'Tax_Rate': 0.21},
        'deal':     {'Purchase_Price_per_Share': 110, 'Cash_Mix': 40, 'Stock_Mix': 60, 'Synergies': 2500, 'New_Debt_Financing': 5000, 'Interest_Rate': 0.045}
    },
    'pharma_merger': {
        'name': 'Pharma Merger (Mid Cap)',
        'acquirer': {'Revenue': 20000, 'EBITDA': 6000, 'Net_Income': 4000, 'Shares_Outstanding': 800, 'Share_Price': 90, 'Debt': 8000, 'Cash': 2000, 'Tax_Rate': 0.22},
        'target':   {'Revenue': 8000,  'EBITDA': 2400, 'Net_Income': 1600, 'Shares_Outstanding': 300, 'Share_Price': 60, 'Debt': 1500, 'Cash': 500,  'Tax_Rate': 0.22},
        'deal':     {'Purchase_Price_per_Share': 78, 'Cash_Mix': 70, 'Stock_Mix': 30, 'Synergies': 1200, 'New_Debt_Financing': 6000, 'Interest_Rate': 0.05}
    },
    'retail_buyout': {
        'name': 'Retail Buyout (Small Cap)',
        'acquirer': {'Revenue': 5000, 'EBITDA': 1500, 'Net_Income': 1000, 'Shares_Outstanding': 200, 'Share_Price': 50, 'Debt': 2000, 'Cash': 500, 'Tax_Rate': 0.25},
        'target':   {'Revenue': 2000, 'EBITDA': 600,  'Net_Income': 400,  'Shares_Outstanding': 100, 'Share_Price': 40, 'Debt': 500,  'Cash': 200, 'Tax_Rate': 0.25},
        'deal':     {'Purchase_Price_per_Share': 45, 'Cash_Mix': 50, 'Stock_Mix': 50, 'Synergies': 300, 'New_Debt_Financing': 800, 'Interest_Rate': 0.05}
    },
    'bank_acquisition': {
        'name': 'Banking Acquisition',
        'acquirer': {'Revenue': 30000, 'EBITDA': 12000, 'Net_Income': 8000, 'Shares_Outstanding': 1500, 'Share_Price': 120, 'Debt': 50000, 'Cash': 15000, 'Tax_Rate': 0.21},
        'target':   {'Revenue': 10000, 'EBITDA': 4000,  'Net_Income': 2500, 'Shares_Outstanding': 600,  'Share_Price': 55,  'Debt': 20000, 'Cash': 6000, 'Tax_Rate': 0.21},
        'deal':     {'Purchase_Price_per_Share': 72, 'Cash_Mix': 100, 'Stock_Mix': 0, 'Synergies': 1800, 'New_Debt_Financing': 10000, 'Interest_Rate': 0.04}
    }
}

def run_model(acquirer, target, deal):
    # --- Valuation ---
    target_equity_value = target['Shares_Outstanding'] * deal['Purchase_Price_per_Share']
    target_ev = target_equity_value + target['Debt'] - target['Cash']
    deal_premium = ((deal['Purchase_Price_per_Share'] - target['Share_Price']) / target['Share_Price']) * 100

    # --- Payment Structure ---
    cash_payment = (deal['Cash_Mix'] / 100) * target_equity_value
    stock_payment = (deal['Stock_Mix'] / 100) * target_equity_value
    exchange_ratio = deal['Purchase_Price_per_Share'] / acquirer['Share_Price'] if acquirer['Share_Price'] > 0 else 0
    new_shares_issued = stock_payment / deal['Purchase_Price_per_Share'] if deal['Purchase_Price_per_Share'] > 0 else 0
    dilution_pct = (new_shares_issued / acquirer['Shares_Outstanding']) * 100 if acquirer['Shares_Outstanding'] > 0 else 0

    # --- Pro Forma ---
    pro_forma_shares = acquirer['Shares_Outstanding'] + new_shares_issued
    synergies_after_tax = deal['Synergies'] * (1 - acquirer['Tax_Rate'])
    interest_expense = deal['New_Debt_Financing'] * deal['Interest_Rate']
    interest_after_tax = interest_expense * (1 - acquirer['Tax_Rate'])
    pro_forma_net_income = acquirer['Net_Income'] + target['Net_Income'] + synergies_after_tax - interest_after_tax
    pro_forma_eps = pro_forma_net_income / pro_forma_shares if pro_forma_shares > 0 else 0
    acquirer_eps = acquirer['Net_Income'] / acquirer['Shares_Outstanding'] if acquirer['Shares_Outstanding'] > 0 else 0
    eps_impact = pro_forma_eps - acquirer_eps
    eps_impact_pct = (eps_impact / acquirer_eps) * 100 if acquirer_eps != 0 else 0

    # --- Combined Financials ---
    pf_revenue = acquirer['Revenue'] + target['Revenue']
    pf_ebitda = acquirer['EBITDA'] + target['EBITDA'] + deal['Synergies']
    pf_ebitda_margin = (pf_ebitda / pf_revenue) * 100 if pf_revenue > 0 else 0
    acq_ebitda_margin = (acquirer['EBITDA'] / acquirer['Revenue']) * 100 if acquirer['Revenue'] > 0 else 0
    tgt_ebitda_margin = (target['EBITDA'] / target['Revenue']) * 100 if target['Revenue'] > 0 else 0

    # --- Leverage ---
    combined_debt = acquirer['Debt'] + target['Debt'] + deal['New_Debt_Financing']
    combined_cash = acquirer['Cash'] + target['Cash'] - cash_payment
    net_debt = combined_debt - combined_cash
    leverage_ratio = net_debt / pf_ebitda if pf_ebitda > 0 else 0

    # --- Multiples ---
    acq_ev = acquirer['Shares_Outstanding'] * acquirer['Share_Price'] + acquirer['Debt'] - acquirer['Cash']
    acq_ev_ebitda = acq_ev / acquirer['EBITDA'] if acquirer['EBITDA'] > 0 else 0
    tgt_ev_ebitda = target_ev / target['EBITDA'] if target['EBITDA'] > 0 else 0
    pf_ev = pro_forma_shares * acquirer['Share_Price']
    pf_ev_ebitda = pf_ev / pf_ebitda if pf_ebitda > 0 else 0

    return {
        'target_equity_value': round(target_equity_value, 2),
        'target_ev': round(target_ev, 2),
        'deal_premium': round(deal_premium, 2),
        'cash_payment': round(cash_payment, 2),
        'stock_payment': round(stock_payment, 2),
        'exchange_ratio': round(exchange_ratio, 4),
        'new_shares_issued': round(new_shares_issued, 2),
        'dilution_pct': round(dilution_pct, 2),
        'pro_forma_shares': round(pro_forma_shares, 2),
        'synergies_after_tax': round(synergies_after_tax, 2),
        'interest_expense': round(interest_expense, 2),
        'pro_forma_net_income': round(pro_forma_net_income, 2),
        'pro_forma_eps': round(pro_forma_eps, 4),
        'acquirer_eps': round(acquirer_eps, 4),
        'eps_impact': round(eps_impact, 4),
        'eps_impact_pct': round(eps_impact_pct, 2),
        'deal_status': 'Accretive' if eps_impact > 0 else 'Dilutive',
        'pf_revenue': round(pf_revenue, 2),
        'pf_ebitda': round(pf_ebitda, 2),
        'pf_ebitda_margin': round(pf_ebitda_margin, 2),
        'acq_ebitda_margin': round(acq_ebitda_margin, 2),
        'tgt_ebitda_margin': round(tgt_ebitda_margin, 2),
        'combined_debt': round(combined_debt, 2),
        'combined_cash': round(combined_cash, 2),
        'net_debt': round(net_debt, 2),
        'leverage_ratio': round(leverage_ratio, 2),
        'acq_ev_ebitda': round(acq_ev_ebitda, 2),
        'tgt_ev_ebitda': round(tgt_ev_ebitda, 2),
        'pf_ev_ebitda': round(pf_ev_ebitda, 2),
    }

@app.route('/')
def index():
    return render_template('index.html', templates=TEMPLATES)

@app.route('/get_template/<name>')
def get_template(name):
    if name in TEMPLATES:
        return jsonify(TEMPLATES[name])
    return jsonify({'error': 'Template not found'}), 404

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    acquirer = data['acquirer']
    target = data['target']
    deal = data['deal']
    results = run_model(acquirer, target, deal)
    return jsonify({'results': results, 'acquirer': acquirer, 'target': target, 'deal': deal})

if __name__ == '__main__':
    app.run(debug=True)

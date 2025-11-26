import xlsxwriter

# Inputs for the Acquirer and Target
acquirer_data = {
    "Revenue": 5000,
    "EBITDA": 1500,
    "Net Income": 1000,
    "Shares Outstanding": 200,
    "Share Price": 50,
    "Debt": 2000,
    "Cash": 500,
    "Tax Rate": 0.25,
}

target_data = {
    "Revenue": 2000,
    "EBITDA": 600,
    "Net Income": 400,
    "Shares Outstanding": 100,
    "Share Price": 40,
    "Debt": 500,
    "Cash": 200,
    "Tax Rate": 0.25,
}

deal_terms = {
    "Purchase Price per Share": 45,  # Purchase price offered for target's shares
    "Payment Mix": {"Cash": 50, "Stock": 50},  # % split
    "Synergies": 300,  # Cost savings or revenue enhancements
    "New Debt Financing": 800,  # Debt raised for the deal
}

# Calculate Enterprise Value and Purchase Price
target_equity_value = target_data["Shares Outstanding"] * deal_terms["Purchase Price per Share"]
target_enterprise_value = target_equity_value + target_data["Debt"] - target_data["Cash"]

# Deal payment breakdown
cash_payment = (deal_terms["Payment Mix"]["Cash"] / 100) * target_equity_value
stock_payment = (deal_terms["Payment Mix"]["Stock"] / 100) * target_equity_value

# Shares issued for stock payment
exchange_ratio = deal_terms["Purchase Price per Share"] / acquirer_data["Share Price"]
new_shares_issued = stock_payment / deal_terms["Purchase Price per Share"]

# Pro Forma Shares Outstanding
pro_forma_shares = acquirer_data["Shares Outstanding"] + new_shares_issued

# Pro Forma Net Income (including synergies and deal financing impacts)
synergies_after_tax = deal_terms["Synergies"] * (1 - acquirer_data["Tax Rate"])
interest_expense = deal_terms["New Debt Financing"] * 0.05  # Assuming 5% interest rate
interest_after_tax = interest_expense * (1 - acquirer_data["Tax Rate"])

pro_forma_net_income = (
    acquirer_data["Net Income"]
    + target_data["Net Income"]
    + synergies_after_tax
    - interest_after_tax
)

# Pro Forma EPS
pro_forma_eps = pro_forma_net_income / pro_forma_shares

# Standalone EPS for Acquirer
acquirer_eps = acquirer_data["Net Income"] / acquirer_data["Shares Outstanding"]

# Accretion/Dilution Analysis
eps_impact = pro_forma_eps - acquirer_eps
eps_status = "Accretive" if eps_impact > 0 else "Dilutive"

# Output Summary
output = {
    "Pro Forma Revenue": acquirer_data["Revenue"] + target_data["Revenue"],
    "Pro Forma EBITDA": acquirer_data["EBITDA"] + target_data["EBITDA"] + deal_terms["Synergies"],
    "Pro Forma Net Income": pro_forma_net_income,
    "Pro Forma Shares Outstanding": pro_forma_shares,
    "Pro Forma EPS": pro_forma_eps,
    "Standalone Acquirer EPS": acquirer_eps,
    "EPS Impact": eps_impact,
    "Deal Status": eps_status,
}

# Create an Excel Dashboard
file_name = "Merger_Model_Dashboard.xlsx"
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet("Dashboard")

# Define formats
header_format = workbook.add_format({"bold": True, "bg_color": "#4CAF50", "font_color": "white", "align": "center", "border": 1})
section_header_format = workbook.add_format({"bold": True, "bg_color": "#FFC107", "align": "left", "border": 1})
currency_format = workbook.add_format({"num_format": "$#,##0.00", "border": 1})
decimal_format = workbook.add_format({"num_format": "0.00", "border": 1})
text_format = workbook.add_format({"border": 1})

# Add title
worksheet.merge_range("A1:D1", "Dynamic Merger Model Dashboard", header_format)

# Write Input Data
worksheet.merge_range("A3:D3", "Input Parameters", section_header_format)
worksheet.write("A4", "Acquirer Data", text_format)
worksheet.write("A5", "Revenue", text_format)
worksheet.write("B5", acquirer_data["Revenue"], currency_format)
worksheet.write("A6", "Net Income", text_format)
worksheet.write("B6", acquirer_data["Net Income"], currency_format)
worksheet.write("A7", "Shares Outstanding", text_format)
worksheet.write("B7", acquirer_data["Shares Outstanding"])
worksheet.write("A8", "Target Data", text_format)
worksheet.write("A9", "Revenue", text_format)
worksheet.write("B9", target_data["Revenue"], currency_format)
worksheet.write("A10", "Net Income", text_format)
worksheet.write("B10", target_data["Net Income"], currency_format)
worksheet.write("A11", "Shares Outstanding", text_format)
worksheet.write("B11", target_data["Shares Outstanding"])

# Write Output Data
worksheet.merge_range("A13:D13", "Pro Forma Output", section_header_format)
worksheet.write("A14", "Pro Forma Revenue", text_format)
worksheet.write("B14", output["Pro Forma Revenue"], currency_format)
worksheet.write("A15", "Pro Forma EBITDA", text_format)
worksheet.write("B15", output["Pro Forma EBITDA"], currency_format)
worksheet.write("A16", "Pro Forma Net Income", text_format)
worksheet.write("B16", output["Pro Forma Net Income"], currency_format)
worksheet.write("A17", "Pro Forma Shares Outstanding", text_format)
worksheet.write("B17", output["Pro Forma Shares Outstanding"])
worksheet.write("A18", "Pro Forma EPS", text_format)
worksheet.write("B18", output["Pro Forma EPS"], decimal_format)
worksheet.write("A19", "Standalone Acquirer EPS", text_format)
worksheet.write("B19", output["Standalone Acquirer EPS"], decimal_format)
worksheet.write("A20", "EPS Impact", text_format)
worksheet.write("B20", output["EPS Impact"], decimal_format)
worksheet.write("A21", "Deal Status", text_format)
worksheet.write("B21", output["Deal Status"], text_format)

# Set column widths for better visibility
worksheet.set_column("A:A", 25)
worksheet.set_column("B:B", 20)

# Add conditional formatting for Deal Status
worksheet.conditional_format("B21", {
    "type": "text",
    "criteria": "containing",
    "value": "Accretive",
    "format": workbook.add_format({"bg_color": "#DFF0D8", "font_color": "#3C763D", "border": 1}),
})
worksheet.conditional_format("B21", {
    "type": "text",
    "criteria": "containing",
    "value": "Dilutive",
    "format": workbook.add_format({"bg_color": "#F2DEDE", "font_color": "#A94442", "border": 1}),
})

workbook.close()
print(f"Excel dashboard saved as {file_name}")

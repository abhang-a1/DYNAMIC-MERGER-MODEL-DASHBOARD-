# 🚀 DYNAMIC M&A MERGER MODEL DASHBOARD

## 🎯 Professional Financial M&A Analysis Web Application

A sophisticated Flask-based web application for analyzing mergers and acquisitions with real-time financial modeling, pro forma analysis, and interactive data visualizations.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🎨 Modern UI/UX
- **Glassmorphism Design** - Beautiful frosted glass effects with backdrop blur
- **Gradient Backgrounds** - Professional purple-blue color scheme
- **Responsive Layout** - Works perfectly on desktop, tablet, and mobile
- **Interactive Charts** - Real-time Chart.js visualizations

### 📊 Financial Analysis
- **Complete M&A Modeling** - Full merger & acquisition financial analysis
- **EPS Accretion/Dilution** - Automatic calculation of deal impact
- **Pro Forma Financials** - Combined company projections
- **Synergy Analysis** - Cost savings and revenue enhancements
- **Leverage Ratios** - Debt/EBITDA and other key metrics
- **Valuation Multiples** - EV/EBITDA calculations

### 🎯 Pre-built Templates
1. **💻 Tech Acquisition** - Large cap technology company merger
2. **💊 Pharma Merger** - Mid cap pharmaceutical consolidation  
3. **🛒 Retail Buyout** - Small cap retail business acquisition
4. **🏦 Bank Acquisition** - Financial services strategic merger

### 📈 Visualizations
- Revenue comparison bar chart
- EPS impact analysis chart
- EBITDA breakdown doughnut chart
- Real-time updates on calculation

---

## 🗂️ Project Structure

```
DYNAMIC-MERGER-MODEL-DASHBOARD/
│
├── app.py                 # Flask backend with API endpoints
├── dmm.py                 # Original Excel-based model
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
└── templates/
    └── index.html        # Full dashboard UI with forms & charts
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/abhang-a1/DYNAMIC-MERGER-MODEL-DASHBOARD-.git
cd DYNAMIC-MERGER-MODEL-DASHBOARD-
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://127.0.0.1:5000
```

---

## 💻 Usage Guide

### Using Pre-built Templates

1. Click on any template card (Tech, Pharma, Retail, or Bank)
2. The form will auto-populate with industry-specific data
3. Click "Calculate Pro Forma Analysis" button
4. View comprehensive results with charts

### Custom Analysis

1. **Acquirer Data** - Enter your acquiring company financials:
   - Revenue, EBITDA, Net Income
   - Shares Outstanding, Share Price
   - Debt, Cash, Tax Rate

2. **Target Data** - Enter target company information:
   - Same financial metrics as acquirer

3. **Deal Terms** - Define the transaction:
   - Purchase price per share
   - Cash/Stock payment mix (%)
   - Expected synergies
   - New debt financing amount
   - Interest rate on new debt

4. **Calculate** - Click the button to run the model

### Understanding Results

#### 💰 Deal Valuation
- Target Equity Value
- Target Enterprise Value  
- Deal Premium (%)
- Cash vs Stock Payment Split

#### 📈 EPS Impact
- Standalone Acquirer EPS
- Pro Forma Combined EPS
- EPS Impact ($ and %)
- **Deal Status**: Accretive ✅ or Dilutive ❌

#### 💵 Pro Forma Financials
- Combined Revenue
- Combined EBITDA (with synergies)
- Combined Net Income
- EBITDA Margin

#### 📊 Leverage & Multiples
- Total Combined Debt
- Net Debt
- Leverage Ratio (Net Debt/EBITDA)
- Pro Forma EV/EBITDA Multiple

---

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Werkzeug 3.0.1** - WSGI utility library

### Frontend  
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with glassmorphism
- **Vanilla JavaScript** - No heavy frameworks
- **Chart.js** - Interactive data visualizations

### Design
- Gradient backgrounds
- Backdrop filter effects
- Responsive grid layouts
- Smooth animations and transitions

---

## 📊 API Endpoints

### `GET /`
Renders the main dashboard page

### `GET /get_template/<template_name>`
Returns pre-built template data in JSON format

**Example Response:**
```json
{
  "name": "Tech Acquisition (Large Cap)",
  "acquirer": { ... },
  "target": { ... },
  "deal": { ... }
}
```

### `POST /calculate`
Performs M&A financial analysis

**Request Body:**
```json
{
  "acquirer": { "Revenue": 5000, ... },
  "target": { "Revenue": 2000, ... },
  "deal": { "Purchase_Price_per_Share": 45, ... }
}
```

**Response:**
```json
{
  "results": {
    "target_equity_value": 4500,
    "eps_impact": 0.125,
    "deal_status": "Accretive",
    ...
  }
}
```

---

## 🎓 Business Use Cases

### Investment Banking
- Pitch book preparation
- Deal modeling and valuation
- Client presentations
- Scenario analysis

### Private Equity
- LBO modeling
- Add-on acquisition analysis  
- Portfolio company consolidation
- Exit strategy planning

### Corporate Development
- M&A target evaluation
- Strategic planning
- Board presentations
- Integration planning

### Financial Analysis
- Academic research
- Case study preparation
- Training and education
- Interview preparation

---

## 🚀 Deployment

### Local Development
```bash
python app.py
# Runs on http://127.0.0.1:5000
```

### Production Deployment Options

#### 1. PythonAnywhere (Free)
```bash
# Upload files via Files tab
# Set up virtual environment
# Configure WSGI file
# Point to app.py
```

#### 2. Heroku
```bash
heroku create your-app-name
git push heroku main
```

#### 3. AWS/GCP/Azure
- Deploy using Elastic Beanstalk, App Engine, or App Service
- Configure environment variables
- Set up domain and SSL

---

## 📝 Future Enhancements

- [ ] PDF report generation
- [ ] Excel export functionality
- [ ] Sensitivity analysis tables
- [ ] Comparable company analysis
- [ ] Precedent transaction analysis
- [ ] Monte Carlo simulation
- [ ] User authentication
- [ ] Save/load scenarios
- [ ] Historical deal database

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Abhang A1**  
GitHub: [@abhang-a1](https://github.com/abhang-a1)

---

## 🙏 Acknowledgments

- Chart.js for beautiful visualizations
- Flask community for excellent documentation
- Financial modeling best practices from investment banking

---

**⭐ Star this repo if you find it useful!**

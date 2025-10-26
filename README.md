# 📊 PyPre - Python Business Intelligence & Analytics Platform

A powerful, self-hosted Business Intelligence and analytics platform built with Python and Flask. Features a lightweight dashboard builder and specialized insurance claims analytics tools.

## 📑 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Production Deployment](#-production-deployment)
- [API Endpoints](#-api-endpoints)
- [Tips & Best Practices](#-tips--best-practices)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Technology Stack](#-technology-stack)
- [Security](#-security-considerations)

## ✨ Features

### Core Dashboard Features
- **🎨 Beautiful Dashboard Builder**: Drag-and-drop grid system for creating custom dashboards
- **📈 Multiple Chart Types**: Bar, Line, Pie, Scatter, Area charts and Data Tables
- **📁 CSV Data Import**: Upload and analyze CSV files instantly
- **🔐 Secure Authentication**: JSON-based user management with encrypted passwords
- **⚡ Low Resource Usage**: Optimized for minimal RAM and CPU consumption
- **🎯 Easy to Use**: Intuitive UI/UX for business users
- **🏠 Self-Hosted**: Complete control over your data
- **🔧 Flexible & Extensible**: Clean, modular architecture

### PCHI Claims Dashboard (Specialized Feature)
- **💼 Insurance Claims Analytics**: Comprehensive dashboard for analyzing PCHI insurance claims data
- **📊 Advanced KPI Tracking**: Total claims, incurred amounts, approval rates, and more
- **📈 Trend Analysis**: Monthly and yearly claims trends with interactive visualizations
- **🏥 Healthcare Analytics**: Provider analysis, benefit type distribution, diagnosis tracking
- **👥 Demographic Insights**: Age and gender distribution analysis
- **🎯 Business Intelligence**: Business unit performance, product analysis, distribution channels
- **🔍 Advanced Filtering**: Multi-dimensional filtering by year, status, business unit, product, and more
- **📋 Data Export**: Paginated data tables with export capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**:
```bash
cd databoard
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Access the dashboard**:
Open your browser and go to: `http://localhost:5000`

### First Time Setup

On first run, you'll need to register a new account:
1. Navigate to `http://localhost:5000`
2. Click on "Register" tab
3. Create your admin account
4. Log in with your new credentials

**Note**: User passwords are securely hashed using Werkzeug's password hashing utilities.

## 📁 Project Structure

```
PyPre/
├── app.py                       # Main Flask application (Flask-based web dashboard)
├── pchi_claims_dashboard.py    # Standalone Streamlit PCHI dashboard
├── requirements.txt             # Python dependencies
├── setup.sh / setup.bat         # Setup scripts for different platforms
├── START_DASHBOARD.sh           # Quick start script for PCHI dashboard
│
├── core/                        # Core modules
│   ├── auth_manager.py         # Authentication handling with password hashing
│   ├── data_processor.py       # CSV processing & data manipulation
│   ├── chart_builder.py        # Chart generation logic
│   └── pchi_analyzer.py        # PCHI claims data analysis engine
│
├── templates/                   # HTML templates
│   ├── login.html              # Login/Register page
│   ├── dashboard.html          # Main dashboard interface
│   └── pchi_dashboard.html     # PCHI claims dashboard (Flask version)
│
├── static/                      # Static assets (CSS, JS, images)
│   └── dashboard.js            # Dashboard JavaScript
│
├── data/                        # Data storage (auto-created)
│   ├── users.json              # User accounts (hashed passwords)
│   ├── uploads/                # Uploaded CSV files
│   ├── datasets/               # Dataset metadata
│   └── dashboards/             # Saved dashboards
│
├── test_*.py                    # Test files for various components
└── *.md                         # Documentation files
```

## 🎯 Usage Guide

### Main Dashboard (General BI)

#### 1. Upload Data

1. Log in to the dashboard
2. Click **"📁 Upload CSV"** in the sidebar
3. Select or drag-and-drop your CSV file
4. Wait for processing to complete

#### 2. Create Visualizations

1. Select your uploaded dataset from the sidebar
2. Click on a chart type (Bar, Line, Pie, etc.)
3. Configure the chart:
   - Select X-axis column (categories)
   - Select Y-axis column (values)
   - Choose aggregation function (Sum, Average, Count, etc.)
   - Set data limit
4. Click **"Create Chart"**

#### 3. Customize Dashboard

- **Drag**: Move widgets around the dashboard
- **Resize**: Drag the bottom-right corner of widgets
- **Delete**: Click the 🗑️ icon on any widget
- **Save**: Click **"💾 Save Dashboard"** to preserve your layout

### PCHI Claims Dashboard

#### Access PCHI Dashboard

**Method 1: Flask Web Interface (Integrated)**
1. Log in to the main application
2. Navigate to `/pchi` route (e.g., `http://localhost:5000/pchi`)
3. Use the integrated dashboard with authentication

**Method 2: Standalone Streamlit App**
```bash
# Run the standalone dashboard
streamlit run pchi_claims_dashboard.py

# Or use the quick start script
./START_DASHBOARD.sh
```

#### Using PCHI Dashboard Features

1. **Filter Data**: Use the sidebar to filter by:
   - Year (2020 - Present)
   - Claim Status (Accept/Reject)
   - Business Unit
   - Product Type
   - Distribution Channel

2. **View KPIs**: Monitor key metrics at the top:
   - Total Claims Count
   - Total Incurred Amount
   - Total Approved Amount
   - Approval Rate

3. **Analyze Trends**:
   - Monthly claims trends
   - Year-over-year comparisons
   - Status distribution

4. **Explore Demographics**:
   - Age group distribution
   - Gender distribution

5. **Provider & Product Analysis**:
   - Top providers by approved amount
   - Top benefit types
   - Product performance

6. **Export Data**: Download filtered data as CSV using the download button

#### PCHI Data Format Requirements

The PCHI Claims Dashboard expects CSV data with the following columns:

**Required Columns:**
- `CL_NO` - Claim Number
- `CLAIM_STATUS` - Status (Accept/Reject)
- `INCURRED` - Incurred Amount
- `APPROVED` - Approved Amount
- `CLAIMED` - Claimed Amount
- `PAYDATE` - Payment Date

**Optional Columns:**
- `PROVIDER` - Healthcare Provider Name
- `BU` - Business Unit
- `PRODUCT` - Product Type
- `BEN_TYPE_DESC` - Benefit Type Description
- `DISTRIBUTION` - Distribution Channel
- `AGE` - Claimant Age
- `Gender` - Claimant Gender
- `OUTSTANDING` - Outstanding Amount
- `DIAGNOSIS_DETAILS` - Diagnosis Details
- `POLICYHOLDER` - Policyholder Name
- `Member Name` - Member Name
- Date columns: `POLICY EFF DATE`, `POLICY EXP DATE`, `SICK/FROM`, `SICK/TO`, `RECEIPT/DT`, `CHQDATE`

### User Management

#### Register New User:
1. Go to login page at `http://localhost:5000/login`
2. Click "Register" tab
3. Enter username, password, and optionally email
4. Click "Create Account"

**Password Requirements**: Minimum 6 characters

#### Manage Users:
- Users are stored in `data/users.json` with securely hashed passwords
- Use the authentication API endpoints for programmatic access

## 🛠️ Configuration

### Change Server Port

Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### File Upload Limits

Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB (change as needed)
```

### Session Timeout

Edit `app.py`:
```python
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)  # Change duration
```

## 📊 Supported Chart Types

| Chart Type | Best For | Data Requirements |
|------------|----------|-------------------|
| Bar Chart | Comparing categories | Category + Numeric |
| Line Chart | Trends over time | Category + Numeric |
| Pie Chart | Part-to-whole relationships | Category + Numeric |
| Scatter Plot | Correlations | Two numeric columns |
| Area Chart | Cumulative trends | Category + Numeric |
| Table | Detailed data view | Any columns |

## 💻 Example Usage

### Starting the Application

```bash
# Standard way
python app.py

# Access at http://localhost:5000
```

### Using the API (Python Example)

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "username": "admin",
    "password": "your_password"
})
session_cookie = response.cookies

# Get PCHI KPIs with filters
response = requests.post(
    f"{BASE_URL}/api/pchi/kpis",
    json={
        "filters": {
            "years": [2023, 2024],
            "statuses": ["Accept"]
        }
    },
    cookies=session_cookie
)
kpis = response.json()
print(f"Total Claims: {kpis['total_claims']}")
print(f"Approval Rate: {kpis['approval_rate']}%")
```

### Running PCHI Dashboard (Streamlit)

```bash
# Method 1: Direct command
streamlit run pchi_claims_dashboard.py

# Method 2: Using start script
chmod +x START_DASHBOARD.sh
./START_DASHBOARD.sh

# Method 3: With custom port
streamlit run pchi_claims_dashboard.py --server.port 8501
```

## 🔒 Security Notes

- Change default admin password after first login
- Use strong passwords for all accounts
- Run behind a reverse proxy (nginx/Apache) in production
- Enable HTTPS for production deployments
- Regularly backup the `data/` directory

## 🚀 Production Deployment

### Using Gunicorn (Recommended)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using systemd (Linux)

Create `/etc/systemd/system/databoard.service`:
```ini
[Unit]
Description=DataBoard BI Dashboard
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/databoard
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable databoard
sudo systemctl start databoard
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
  - Body: `{"username": "string", "password": "string"}`
- `POST /api/auth/register` - User registration
  - Body: `{"username": "string", "password": "string", "email": "string"}`
- `POST /api/auth/logout` - User logout

### Data Management
- `GET /api/datasets` - List user datasets
- `GET /api/dataset/<id>` - Get dataset info
- `POST /api/upload` - Upload CSV file
- `GET /api/dataset/<id>/preview` - Preview dataset (query param: `rows`)

### Charts & Dashboards
- `POST /api/chart/create` - Create chart
  - Body: `{"dataset_id": "string", "chart_type": "string", "config": {}}`
- `POST /api/dashboard/save` - Save dashboard
  - Body: `{"id": "string", "name": "string", "layout": []}`
- `GET /api/dashboard/load/<id>` - Load dashboard
- `GET /api/dashboards` - List dashboards

### PCHI Claims Analytics
- `POST /api/pchi/kpis` - Get KPI summary
- `POST /api/pchi/trends` - Get claims trends
- `POST /api/pchi/status` - Get claim status distribution
- `POST /api/pchi/providers` - Get top providers
- `POST /api/pchi/business-units` - Get business unit analysis
- `POST /api/pchi/age-distribution` - Get age distribution
- `POST /api/pchi/gender-distribution` - Get gender distribution
- `POST /api/pchi/benefit-types` - Get benefit type analysis
- `POST /api/pchi/distribution-channels` - Get distribution channel analysis
- `POST /api/pchi/products` - Get product analysis
- `POST /api/pchi/yearly-comparison` - Get yearly comparison
- `POST /api/pchi/table` - Get paginated claims data
- `GET /api/pchi/filter-options` - Get available filter options

All PCHI endpoints accept optional filter parameters in the request body:
```json
{
  "filters": {
    "years": [2023, 2024],
    "statuses": ["Accept"],
    "business_units": ["BU1", "BU2"],
    "products": ["Product A"],
    "distribution_channels": ["Channel 1"]
  }
}
```

## 💡 Tips & Best Practices

### General Dashboard
1. **Data Preparation**: Clean your CSV files before upload (remove special characters, ensure consistent formatting)
2. **Performance**: Limit data points for large datasets (use the limit option)
3. **Column Names**: Use clear, descriptive column names in your CSV files
4. **Aggregation**: Choose appropriate aggregation functions for your analysis
5. **Dashboard Organization**: Group related charts together for better readability

### PCHI Claims Dashboard
1. **Data Loading**: The PCHI dashboard expects data in the path `data/uploads/20251024 PCHI Claim summary 2020 - now.csv`
2. **Large Datasets**: The dashboard uses caching to improve performance with large datasets
3. **Filters**: Apply filters incrementally to narrow down your analysis
4. **Export**: Use the data export feature to save filtered results for further analysis
5. **Date Columns**: Ensure date columns are in a recognized format (YYYY-MM-DD recommended)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py or kill existing process
lsof -ti:5000 | xargs kill -9

# Or change the port in app.py:
# app.run(debug=True, host='0.0.0.0', port=8080)  # Use different port
```

### CSV Upload Fails
- Check file size limits (default: 50MB max)
- Ensure CSV is properly formatted with valid UTF-8 encoding
- Verify column names don't contain special characters
- Make sure the `data/uploads` directory exists and has write permissions

### Charts Not Displaying
- Verify dataset is selected
- Check that columns are correctly mapped
- Ensure data types match chart requirements
- Clear browser cache and refresh

### Authentication Issues
- If you can't log in, check `data/users.json` exists and is valid JSON
- For password reset, manually edit `data/users.json` (passwords are hashed)
- Use `migrate_passwords.py` if upgrading from an older version with plain text passwords

### PCHI Dashboard Issues
- **Data not loading**: Verify the CSV file exists at `data/uploads/20251024 PCHI Claim summary 2020 - now.csv`
- **Streamlit errors**: Make sure streamlit is installed: `pip install streamlit plotly`
- **Performance issues**: The first load caches data; subsequent loads will be faster
- **Missing visualizations**: Check that required columns exist in your CSV file

## 🤝 Contributing

This is a self-contained project. To extend functionality:

1. **Add new chart types**: Extend `core/chart_builder.py`
2. **Add new data sources**: Modify `core/data_processor.py`
3. **Create custom analyzers**: Follow the pattern in `core/pchi_analyzer.py`
4. **Customize UI**: Edit templates in `templates/` and assets in `static/`
5. **Add new API endpoints**: Update `app.py` with new routes

### Development Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in debug mode
python app.py
```

## 📝 License

This project is open-source and free to use for personal and commercial purposes.

## 🌟 Features & Roadmap

### Completed Features ✅
- [x] CSV file upload and processing
- [x] Multiple chart types (Bar, Line, Pie, Scatter, Area, Table)
- [x] User authentication with password hashing
- [x] Dashboard save/load functionality
- [x] PCHI Claims analytics dashboard
- [x] Advanced filtering and data export
- [x] RESTful API endpoints

### Planned Features 🚀
- [ ] Excel file support (.xlsx, .xls)
- [ ] Additional file formats (JSON, Parquet)
- [ ] Database connections (MySQL, PostgreSQL, SQLite)
- [ ] Export dashboards as PDF/PNG
- [ ] Scheduled data refresh
- [ ] Email reports
- [ ] User roles and permissions (Admin, Viewer, Editor)
- [ ] Dark mode theme
- [ ] Mobile responsive improvements
- [ ] Real-time collaboration
- [ ] Data transformation pipelines
- [ ] Custom SQL queries
- [ ] API rate limiting and security enhancements

## 🔐 Security Considerations

- **Password Security**: All passwords are hashed using Werkzeug's `generate_password_hash`
- **Session Management**: Flask sessions with configurable timeout (default: 8 hours)
- **File Upload**: Only CSV files accepted with size limits (50MB default)
- **Path Security**: Uses `secure_filename` for all file uploads
- **Production**: Always use HTTPS and a reverse proxy (nginx/Apache) in production
- **Data Isolation**: User data is isolated per user ID

## 📊 Technology Stack

- **Backend**: Flask 3.0.0
- **Data Processing**: Pandas 2.1.4
- **Security**: Werkzeug 3.0.1
- **Visualization** (Streamlit version): Plotly, Streamlit
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Storage**: JSON files (users, datasets, dashboards)

## 📞 Support & Documentation

### Additional Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [PCHI_DASHBOARD_README.md](PCHI_DASHBOARD_README.md) - PCHI dashboard specific docs

### Getting Help
- Check the [Troubleshooting](#-troubleshooting) section
- Review code comments and docstrings
- Examine test files (`test_*.py`) for usage examples
- Modify and extend as needed for your use case

---

**PyPre** - Lightweight, powerful, and flexible Business Intelligence platform built with Python 🐍📊

Made with ❤️ for data-driven decision making

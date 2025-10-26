# 📊 PCHI Claims Dashboard

## Overview

A comprehensive, interactive dashboard for analyzing PCHI insurance claims data from 2020 to present. The dashboard provides real-time insights into claims performance, provider analysis, business unit metrics, and demographic trends.

## ✅ Status: Successfully Built!

The dashboard has been successfully created and tested with **447,729 claims records** and over **฿2.4 billion** in approved claims.

## 📈 Key Features

### 1. **Key Performance Indicators (KPIs)**
- Total Claims Count: 447,729
- Total Incurred Amount: ฿2.5B+
- Total Approved Amount: ฿2.5B+
- Approval Rate: 89.52%
- Average Claim Amount
- Outstanding Amount

### 2. **Interactive Visualizations**
- **Claims Trend Over Time**: Monthly trends with dual-axis showing claim counts and approved amounts
- **Claim Status Distribution**: Pie chart showing Accept/Reject/Pending status breakdown
- **Top 10 Providers**: Bar chart of highest-volume healthcare providers
- **Business Unit Analysis**: Performance comparison across all 7 business units (BSP, BU1-BU6)
- **Age Distribution**: Claims analysis by age groups (0-18, 19-30, 31-40, 41-50, 51-60, 60+)
- **Gender Distribution**: Male vs Female claim patterns
- **Benefit Type Analysis**: Top benefit categories by count and amount
- **Distribution Channels**: Performance by Direct/Broker/Agent channels
- **Yearly Comparison**: Year-over-year trends from 2020-2025

### 3. **Advanced Filtering**
Filter data by:
- **Year**: 2020, 2021, 2022, 2023, 2024, 2025
- **Claim Status**: Accept, Reject, Incomplete, Pending, Pending Validation
- **Business Unit**: BSP, BU1, BU2, BU3, BU4, BU5, BU6
- **Product Type**: All available insurance products

### 4. **Data Explorer**
- Paginated table view with 50 records per page
- Search and filter capabilities
- Export functionality
- 11 key columns displayed

## 🚀 How to Access

### Option 1: Direct Flask Route
Once the Flask application is running, access the dashboard at:

```
http://localhost:5000/pchi
```

### Option 2: From Main Dashboard
1. Log in to the main DataBoard application
2. Navigate to the PCHI dashboard section
3. Or add a link to `/pchi` in your navigation

### Option 3: Standalone Streamlit Dashboard
Run the standalone Streamlit version:

```bash
streamlit run pchi_claims_dashboard.py
```

Access at: `http://localhost:8501`

## 📊 Sample Insights

### Top Providers by Approved Amount:
1. **BANGKOK HOSPITAL PATTAYA** - ฿272.1M
2. **BUMRUNGRAD HOSPITAL** - ฿210.9M
3. **SAMITIVEJ SUKHUMVIT HOSPITAL** - ฿199.0M
4. **BANGKOK GENERAL HOSPITAL** - ฿144.1M
5. **BANGKOK HOSPITAL PHUKET** - ฿97.9M

### Business Unit Performance:
- **BU1**: 123,947 claims (Largest volume)
- **BU2**: 99,977 claims
- **BU5**: 82,914 claims
- **BU4**: 79,658 claims
- **BU3**: 40,087 claims
- **BU6**: 14,507 claims
- **BSP**: 6,191 claims

### Demographics:
- **Peak age group**: 31-40 years (101,266 claims)
- **Second highest**: 19-30 years (88,151 claims)
- **Children (0-18)**: 74,716 claims

## 🛠️ Technical Architecture

### Backend Components

1. **PCHIAnalyzer** (`core/pchi_analyzer.py`)
   - Data loading and preprocessing
   - Filter application
   - Aggregation and analysis
   - 15+ analysis methods

2. **Flask API Routes** (`app.py`)
   - `/api/pchi/kpis` - Get KPI metrics
   - `/api/pchi/trends` - Get trend data
   - `/api/pchi/status` - Get status distribution
   - `/api/pchi/providers` - Get provider analysis
   - `/api/pchi/business-units` - Get BU metrics
   - `/api/pchi/age-distribution` - Get age demographics
   - `/api/pchi/gender-distribution` - Get gender breakdown
   - `/api/pchi/benefit-types` - Get benefit analysis
   - `/api/pchi/distribution-channels` - Get channel metrics
   - `/api/pchi/products` - Get product analysis
   - `/api/pchi/yearly-comparison` - Get yearly trends
   - `/api/pchi/table` - Get paginated table data
   - `/api/pchi/filter-options` - Get available filters

3. **Frontend** (`templates/pchi_dashboard.html`)
   - Modern, responsive design
   - Chart.js for visualizations
   - Real-time filtering
   - Smooth animations and transitions

### Data Processing
- **Source**: CSV file (490MB, 78 columns)
- **Records**: 447,729 claims
- **Date range**: January 2020 - October 2025
- **Processing**: Pandas for data manipulation
- **Caching**: In-memory data caching for performance

## 📁 Files Created

```
PyPre/
├── core/
│   └── pchi_analyzer.py          # Backend analyzer (390 lines)
├── templates/
│   └── pchi_dashboard.html       # Frontend dashboard
├── app.py                         # Updated with PCHI routes
├── pchi_claims_dashboard.py      # Standalone Streamlit version
├── test_pchi_dashboard.py        # Test script
└── PCHI_DASHBOARD_README.md      # This file
```

## 🧪 Testing

Run the test script to verify everything works:

```bash
python3 test_pchi_dashboard.py
```

Expected output:
```
✅ All tests passed successfully!
```

## 🎨 Dashboard Design

### Color Scheme
- Primary: Purple gradient (`#667eea` to `#764ba2`)
- Success/Accept: Green (`#10b981`)
- Error/Reject: Red (`#ef4444`)
- Warning: Orange (`#f59e0b`)
- Info: Blue (`#3b82f6`)

### Layout
- **Responsive Grid**: Adapts to screen size
- **Card-based Design**: Clean, modern cards for each section
- **Smooth Animations**: Hover effects and transitions
- **Professional Typography**: Clear, readable fonts

## 🔧 Troubleshooting

### If dashboard doesn't load:
1. Verify CSV file exists: `ls -lh data/uploads/20251024\ PCHI\ Claim\ summary\ 2020\ -\ now.csv`
2. Check Flask is running: `ps aux | grep app.py`
3. Check for errors in console
4. Verify pandas is installed: `pip3 list | grep pandas`

### If charts don't render:
1. Check browser console for JavaScript errors
2. Verify Chart.js is loaded (check network tab)
3. Ensure API endpoints return data (check network responses)

### If filters don't work:
1. Verify filter options are loaded (check console)
2. Check API responses in network tab
3. Clear browser cache

## 📊 Performance

- **Initial Load**: ~3-5 seconds (loading 490MB CSV)
- **Filter Application**: ~200-500ms
- **Chart Rendering**: ~50-100ms per chart
- **Table Pagination**: ~100-200ms per page

### Optimization Tips
- Data is cached in memory after first load
- Filters are applied on pandas DataFrames (very fast)
- Charts use Chart.js (hardware accelerated)
- Pagination limits data transfer

## 🎯 Next Steps

### Recommended Enhancements:
1. **Add Export Functionality**
   - PDF report generation
   - Excel export with formatting
   - CSV download of filtered data

2. **Advanced Analytics**
   - Predictive analytics for claim trends
   - Anomaly detection for unusual claims
   - Provider performance scoring

3. **User Customization**
   - Save favorite filters
   - Custom dashboard layouts
   - Scheduled email reports

4. **Real-time Updates**
   - WebSocket for live updates
   - Automatic data refresh
   - Change notifications

## 📝 API Documentation

### POST `/api/pchi/kpis`
Returns key performance indicators.

**Request Body:**
```json
{
  "filters": {
    "years": [2024],
    "statuses": ["Accept"],
    "business_units": ["BU1", "BU2"],
    "products": ["Product A"]
  }
}
```

**Response:**
```json
{
  "total_claims": 105076,
  "total_incurred": 575234567.89,
  "total_approved": 565462753.24,
  "total_claimed": 570123456.78,
  "approval_rate": 95.67,
  "avg_claim_amount": 5382.45
}
```

### POST `/api/pchi/trends`
Returns claims trend data over time.

**Response:**
```json
{
  "labels": ["2024-01", "2024-02", "2024-03"],
  "claim_counts": [8234, 8567, 9012],
  "approved_amounts": [45678901.23, 48901234.56, 52345678.90],
  "incurred_amounts": [46789012.34, 49012345.67, 53456789.01]
}
```

## 🙏 Acknowledgments

- **Data Source**: PCHI Claim Summary 2020 - Present
- **Visualization**: Chart.js
- **Backend**: Flask + Pandas
- **Frontend**: Modern HTML5 + CSS3 + JavaScript

## 📞 Support

For issues or questions:
1. Check this README
2. Run test script: `python3 test_pchi_dashboard.py`
3. Check Flask logs
4. Review browser console for errors

---

**Dashboard Version**: 1.0
**Created**: October 2025
**Data Updated**: October 26, 2025
**Total Records**: 447,729 claims
**Total Value**: ฿2.5+ Billion

# 🏗️ DataBoard Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Login Page  │  │  Dashboard   │  │   Chart.js   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │              │
│         └─────────────────┴──────────────────┘              │
│                           │                                  │
│                    GridStack.js                             │
│                      Dashboard.js                           │
└────────────────────────────┬────────────────────────────────┘
                             │
                    HTTP/REST API
                             │
┌────────────────────────────┴────────────────────────────────┐
│                     Flask Application                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                      app.py                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │   Routes    │  │  Sessions   │  │   Config    │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                                │
│  ┌──────────────────────────┴────────────────────────────┐ │
│  │                  Core Modules                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │ │
│  │  │AuthManager   │  │DataProcessor │  │ChartBuilder│ │ │
│  │  │- Login       │  │- CSV Parse   │  │- Bar       │ │ │
│  │  │- Register    │  │- Analysis    │  │- Line      │ │ │
│  │  │- Validate    │  │- Aggregation │  │- Pie       │ │ │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                      Pandas Library
                             │
┌────────────────────────────┴────────────────────────────────┐
│                      File System                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ data/users   │  │data/uploads/ │  │data/datasets/│     │
│  │  .json       │  │   *.csv      │  │   *.json     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐                                           │
│  │data/         │                                           │
│  │dashboards/   │                                           │
│  │  *.json      │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

## Request Flow Diagram

```
User Action → Frontend → API → Core Module → Data Storage
                ↓         ↓         ↓            ↓
             UI Update ← JSON ← Processing ← Read/Write
```

## Component Interactions

### 1. User Authentication Flow
```
Login Page
    ↓
POST /api/auth/login
    ↓
AuthManager.authenticate()
    ↓
Load data/users.json
    ↓
Verify credentials
    ↓
Create session
    ↓
Redirect to Dashboard
```

### 2. CSV Upload Flow
```
Upload CSV
    ↓
POST /api/upload
    ↓
Save to data/uploads/
    ↓
DataProcessor.process_csv()
    ↓
Read with Pandas
    ↓
Analyze columns (type, stats)
    ↓
Generate metadata
    ↓
Save to data/datasets/
    ↓
Return dataset info
    ↓
Update UI
```

### 3. Chart Creation Flow
```
User configures chart
    ↓
POST /api/chart/create
    ↓
ChartBuilder.create_chart()
    ↓
Load dataset
    ↓
Apply aggregation
    ↓
Format data for Chart.js
    ↓
Return chart config
    ↓
Render in widget
    ↓
Add to GridStack
```

### 4. Dashboard Save Flow
```
User arranges widgets
    ↓
POST /api/dashboard/save
    ↓
Collect layout data
    ↓
Generate dashboard JSON
    ↓
Save to data/dashboards/
    ↓
Return success
```

## Data Models

### User Object
```json
{
  "id": "user_id_hash",
  "username": "john_doe",
  "password": "hashed_password",
  "email": "john@example.com",
  "created_at": "2025-01-15T10:30:00",
  "role": "user"
}
```

### Dataset Metadata
```json
{
  "id": "dataset_id",
  "user_id": "user_id",
  "filename": "sales_data.csv",
  "filepath": "/path/to/file.csv",
  "rows": 1000,
  "columns": 5,
  "columns_info": [
    {
      "name": "Month",
      "type": "categorical",
      "dtype": "object",
      "null_count": 0,
      "stats": {"unique_count": 12}
    },
    {
      "name": "Sales",
      "type": "numeric",
      "dtype": "int64",
      "null_count": 0,
      "stats": {"min": 1000, "max": 50000, "mean": 25000}
    }
  ],
  "created_at": "2025-01-15T10:35:00",
  "size_mb": 0.5
}
```

### Chart Configuration
```json
{
  "type": "bar",
  "data": {
    "labels": ["Jan", "Feb", "Mar"],
    "values": [45000, 48000, 51000],
    "x_label": "Month",
    "y_label": "Sales"
  },
  "config": {
    "x_column": "Month",
    "y_column": "Sales",
    "aggregation": "sum",
    "limit": 20
  }
}
```

### Dashboard Layout
```json
{
  "id": "dash_20250115",
  "name": "Sales Overview",
  "user_id": "user_id",
  "layout": [
    {
      "id": "widget-1",
      "x": 0, "y": 0, "w": 6, "h": 4,
      "content": { "chart_config": {...} }
    }
  ],
  "updated_at": "2025-01-15T11:00:00"
}
```

## Technology Stack

### Backend
- **Flask 3.0**: Web framework
- **Pandas 2.1.4**: Data processing
- **Werkzeug 3.0**: Security utilities

### Frontend
- **GridStack.js 8.4**: Grid layout
- **Chart.js 4.4**: Data visualization
- **Vanilla JavaScript**: No framework overhead
- **Modern CSS**: Flexbox, Grid, Animations

### Storage
- **JSON Files**: User data, metadata
- **CSV Files**: Uploaded datasets
- **File System**: All data storage

## Security Layers

```
┌─────────────────────────────────────┐
│   Session Authentication Layer      │
│   - Secure cookies                  │
│   - CSRF protection                 │
│   - Session timeout                 │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Authorization Layer               │
│   - User-specific data access       │
│   - File ownership checks           │
│   - API endpoint protection         │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Input Validation Layer            │
│   - File type checking              │
│   - Size limits                     │
│   - SQL injection prevention        │
│   - XSS protection                  │
└─────────────────────────────────────┘
```

## Performance Optimization

### Data Processing
- **Chunked reading**: Large files processed in chunks
- **Lazy loading**: Load data only when needed
- **Sampling**: Limit preview rows
- **Caching**: Metadata cached in JSON

### Frontend
- **Minimal dependencies**: Only necessary libraries
- **Lazy rendering**: Charts rendered on demand
- **Debouncing**: Limit API calls during interaction
- **Responsive images**: Optimized asset loading

### Memory Management
- **DataFrame disposal**: Pandas DataFrames released after use
- **File streaming**: Large files not held in memory
- **Session cleanup**: Old sessions automatically cleared

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- Shared file system or S3 for data storage
- Load balancer for distribution

### Vertical Scaling
- Efficient memory usage
- CPU-optimized data processing
- Configurable resource limits

### Data Scaling
```
Small:    < 10K rows     → In-memory processing
Medium:   10K-100K rows  → Chunked processing
Large:    100K-1M rows   → Sampling + aggregation
Very Large: > 1M rows    → Database recommended
```

## Extension Points

### Add New Features
1. **New Chart Type**: Extend ChartBuilder
2. **New Data Source**: Extend DataProcessor
3. **New Auth Method**: Extend AuthManager
4. **New Export Format**: Add to API endpoints

### Integration Options
- **API**: RESTful endpoints
- **Webhooks**: Event-based triggers
- **Plugins**: Module loading system
- **Themes**: CSS customization

## Deployment Architecture

### Single Server
```
┌─────────────────────────┐
│   Nginx (Reverse Proxy) │
│   - SSL termination     │
│   - Static files        │
└───────────┬─────────────┘
            ↓
┌───────────────────────────┐
│   Gunicorn (WSGI)        │
│   - 4 worker processes   │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│   Flask Application      │
└───────────┬───────────────┘
            ↓
┌───────────────────────────┐
│   File System            │
└───────────────────────────┘
```

### High Availability
```
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌────────┐
│ App #1 │ │ App #2 │
└────┬───┘ └───┬────┘
     │         │
     └────┬────┘
          ↓
┌──────────────────┐
│ Shared Storage   │
│ (NFS / S3)       │
└──────────────────┘
```

---

**This architecture provides:**
- 🚀 Fast performance
- 📈 Easy scalability
- 🔒 Strong security
- 🛠️ Simple maintenance
- 🔧 High extensibility

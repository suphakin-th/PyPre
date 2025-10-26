# 📊 DataBoard - Lightweight Python BI Dashboard

A powerful, self-hosted Business Intelligence dashboard built with Python and Flask. Similar to PowerBI but lightweight, flexible, and easy to deploy.

## ✨ Features

- **🎨 Beautiful Dashboard Builder**: Drag-and-drop grid system for creating custom dashboards
- **📈 Multiple Chart Types**: Bar, Line, Pie, Scatter, Area charts and Data Tables
- **📁 CSV Data Import**: Upload and analyze CSV files instantly
- **🔐 JSON-Based Authentication**: Simple user management without database complexity
- **⚡ Low Resource Usage**: Optimized for minimal RAM and CPU consumption
- **🎯 Easy to Use**: Intuitive UI/UX for business users
- **🏠 Self-Hosted**: Complete control over your data
- **🔧 Flexible & Extensible**: Clean, modular architecture

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

### Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
databoard/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── core/                   # Core modules
│   ├── auth_manager.py    # Authentication handling
│   ├── data_processor.py  # CSV processing & data manipulation
│   └── chart_builder.py   # Chart generation logic
├── templates/             # HTML templates
│   ├── login.html        # Login/Register page
│   └── dashboard.html    # Main dashboard interface
├── static/               # Static assets
│   └── dashboard.js      # Dashboard JavaScript
├── data/                 # Data storage (auto-created)
│   ├── users.json       # User accounts
│   ├── uploads/         # Uploaded CSV files
│   ├── datasets/        # Dataset metadata
│   └── dashboards/      # Saved dashboards
└── README.md            # This file
```

## 🎯 Usage Guide

### 1. Upload Data

1. Log in to the dashboard
2. Click **"📁 Upload CSV"** in the sidebar
3. Select or drag-and-drop your CSV file
4. Wait for processing to complete

### 2. Create Visualizations

1. Select your uploaded dataset from the sidebar
2. Click on a chart type (Bar, Line, Pie, etc.)
3. Configure the chart:
   - Select X-axis column (categories)
   - Select Y-axis column (values)
   - Choose aggregation function (Sum, Average, Count, etc.)
   - Set data limit
4. Click **"Create Chart"**

### 3. Customize Dashboard

- **Drag**: Move widgets around the dashboard
- **Resize**: Drag the bottom-right corner of widgets
- **Delete**: Click the 🗑️ icon on any widget
- **Save**: Click **"💾 Save Dashboard"** to preserve your layout

### 4. User Management

#### Register New User:
1. Go to login page
2. Click "Register" tab
3. Enter username and password
4. Click "Create Account"

#### Manage Users:
Edit `data/users.json` file directly or use the authentication API

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
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Data Management
- `GET /api/datasets` - List user datasets
- `GET /api/dataset/<id>` - Get dataset info
- `POST /api/upload` - Upload CSV file
- `GET /api/dataset/<id>/preview` - Preview dataset

### Charts & Dashboards
- `POST /api/chart/create` - Create chart
- `POST /api/dashboard/save` - Save dashboard
- `GET /api/dashboard/load/<id>` - Load dashboard
- `GET /api/dashboards` - List dashboards

## 💡 Tips & Best Practices

1. **Data Preparation**: Clean your CSV files before upload (remove special characters, ensure consistent formatting)
2. **Performance**: Limit data points for large datasets (use the limit option)
3. **Column Names**: Use clear, descriptive column names in your CSV files
4. **Aggregation**: Choose appropriate aggregation functions for your analysis
5. **Dashboard Organization**: Group related charts together for better readability

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py or kill existing process
lsof -ti:5000 | xargs kill -9
```

### CSV Upload Fails
- Check file size limits
- Ensure CSV is properly formatted
- Verify column names don't contain special characters

### Charts Not Displaying
- Verify dataset is selected
- Check that columns are correctly mapped
- Ensure data types match chart requirements

## 🤝 Contributing

This is a self-contained project. To extend functionality:

1. Add new chart types in `core/chart_builder.py`
2. Add new data sources in `core/data_processor.py`
3. Customize UI in `templates/` and `static/`

## 📝 License

This project is open-source and free to use for personal and commercial purposes.

## 🌟 Features Roadmap

- [ ] Excel file support
- [ ] Database connections (MySQL, PostgreSQL)
- [ ] Export dashboards as PDF
- [ ] Scheduled data refresh
- [ ] Email reports
- [ ] User roles and permissions
- [ ] Dark mode
- [ ] Mobile responsive improvements

## 📞 Support

For issues, questions, or contributions:
- Check the troubleshooting section
- Review the code comments
- Modify as needed for your use case

---

**Made with ❤️ for lightweight, powerful data visualization**
# PyPre

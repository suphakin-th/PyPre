# 🚀 Quick Start Guide

Get DataBoard up and running in 5 minutes!

## Step 1: Install Dependencies

### Option A: Automatic Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Option B: Manual Setup

```bash
# Install Python packages
pip install -r requirements.txt

# Create data directories
mkdir -p data/uploads data/datasets data/dashboards static
```

## Step 2: Start the Server

```bash
python app.py
```

You should see:
```
🚀 DataBoard - Lightweight BI Dashboard
📊 Server starting at: http://localhost:5000
```

## Step 3: Login

1. Open your browser to: **http://localhost:5000**
2. Login with default credentials:
   - **Username:** `admin`
   - **Password:** `admin123`

## Step 4: Upload Sample Data

1. Click **"📁 Upload CSV"** in the sidebar
2. Upload the included `sample_data.csv` file
3. Wait for processing to complete

## Step 5: Create Your First Chart

1. The sample dataset should now appear in the sidebar
2. Click on it to select it
3. Click **"📊 Bar Chart"** in the "Add Widget" section
4. Configure the chart:
   - **X-Axis:** Select `Month`
   - **Y-Axis:** Select `Sales`
   - **Aggregation:** Keep as `Sum`
   - Click **"Create Chart"**

## Step 6: Customize Your Dashboard

- **Move widgets:** Drag them around
- **Resize widgets:** Drag the bottom-right corner
- **Add more charts:** Try different chart types
- **Save dashboard:** Click **"💾 Save Dashboard"**

## 🎉 You're Done!

Now explore different chart types and build your own dashboards!

## Next Steps

- Upload your own CSV data
- Try different chart types (Line, Pie, Scatter, etc.)
- Create multiple dashboards
- Invite team members (register new users)

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the troubleshooting section
- Examine the sample data structure in `sample_data.csv`

## Common First-Time Tasks

### Create a New User
1. Logout from admin account
2. Click "Register" tab on login page
3. Enter new username and password
4. Click "Create Account"

### Upload Your Own Data
Your CSV should have:
- Header row with column names
- Consistent data types in each column
- No special characters in column names (use underscore instead)

### Best Chart for Your Data

| Data Type | Best Chart |
|-----------|------------|
| Categories vs Values | Bar Chart |
| Time Series | Line Chart |
| Proportions | Pie Chart |
| Correlations | Scatter Plot |
| Detailed View | Table |

---

**Happy Analyzing! 📊**

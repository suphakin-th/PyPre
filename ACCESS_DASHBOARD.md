# 🚀 Quick Access Guide - PCHI Dashboard

## ✅ Authentication Fixed!

The password hashing issue has been resolved. You can now log in!

## 🔑 Login Credentials

**Username:** `admin`
**Password:** `admin123`

## 📍 Dashboard URL

Once Flask is running, access the PCHI dashboard at:

```
http://localhost:5000/pchi
```

## 🎯 Steps to Access

### 1. Start the Flask Application

The Flask app should already be running. If not:

```bash
python3 app.py
```

You should see:
```
🚀 DataBoard - Lightweight BI Dashboard
📊 Server starting at: http://localhost:5000
```

### 2. Log In

1. Open your browser and go to: `http://localhost:5000`
2. You'll be redirected to the login page
3. Enter:
   - **Username**: `admin`
   - **Password**: `admin123`
4. Click "Login"

### 3. Access PCHI Dashboard

After logging in, you have two options:

**Option A:** Direct URL
- Navigate to: `http://localhost:5000/pchi`

**Option B:** From Main Dashboard
- If there's a navigation menu, look for "PCHI" or "Claims Dashboard"
- Or manually type `/pchi` in the URL bar

## 🎨 What You'll See

When you access `/pchi`, you'll see:

- **Header**: Purple gradient with "PCHI Claims Dashboard" title
- **Filters Section**: 4 multi-select filters (Year, Status, BU, Product)
- **6 KPI Cards**:
  - Total Claims: 447,729
  - Total Incurred: ฿2.5M
  - Total Approved: ฿2.5M
  - Total Claimed: ฿2.5M
  - Approval Rate: 89.52%
  - Avg Claim Amount
- **10 Interactive Charts**: Beautiful visualizations
- **Data Table**: Paginated claims data (50 per page)

## 🔄 If You Need to Restart

1. Stop Flask: `Ctrl+C` in the terminal
2. Restart: `python3 app.py`
3. Access: `http://localhost:5000/pchi`

## 🆘 Troubleshooting

### Can't Log In?
- Ensure you're using `admin` / `admin123`
- Check that `data/users.json` exists
- Try registering a new account

### Dashboard Not Loading?
- Check Flask console for errors
- Verify CSV file exists: `ls data/uploads/20251024*`
- Check browser console (F12)

### Charts Not Showing?
- Clear browser cache
- Check internet connection (Chart.js loads from CDN)
- Look for JavaScript errors in console

## 📊 Using the Dashboard

### Applying Filters
1. Use Ctrl/Cmd + Click to select multiple options in filters
2. Filters update automatically
3. All charts and KPIs refresh with filtered data

### Exploring Data
- Hover over charts for details
- Use pagination buttons at bottom of table
- Scroll through the page to see all visualizations

### Key Insights to Look For
- Monthly trends in claims
- Top performing providers
- Business unit comparison
- Age and gender demographics
- Approval rates by channel

## 🎉 You're Ready!

Your PCHI Claims Dashboard is fully functional and ready to use. Enjoy exploring your 447K+ claims records!

---

**Need Help?** Check the comprehensive documentation in `PCHI_DASHBOARD_README.md`

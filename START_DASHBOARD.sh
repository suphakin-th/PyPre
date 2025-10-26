#!/bin/bash
# Quick start script for PCHI Dashboard

echo "======================================"
echo "🚀 PCHI Claims Dashboard Launcher"
echo "======================================"
echo ""

# Check if CSV exists
if [ ! -f "data/uploads/20251024 PCHI Claim summary 2020 - now.csv" ]; then
    echo "❌ Error: CSV file not found!"
    echo "   Expected: data/uploads/20251024 PCHI Claim summary 2020 - now.csv"
    exit 1
fi

echo "✅ CSV file found"
echo ""

# Check Python dependencies
echo "Checking dependencies..."
python3 -c "import pandas, flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip3 install pandas flask --break-system-packages
fi

echo "✅ Dependencies OK"
echo ""

# Run test
echo "Running quick test..."
python3 test_pchi_dashboard.py | grep "All tests passed"
if [ $? -eq 0 ]; then
    echo "✅ Tests passed"
else
    echo "⚠️  Warning: Tests had issues, but continuing..."
fi

echo ""
echo "======================================"
echo "Choose an option:"
echo "======================================"
echo "1. Start Flask app (integrated dashboard)"
echo "2. Start Streamlit app (standalone dashboard)"
echo "3. Run tests only"
echo "4. Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Flask application..."
        echo "📊 Dashboard will be available at: http://localhost:5000/pchi"
        echo ""
        python3 app.py
        ;;
    2)
        echo ""
        echo "🚀 Starting Streamlit dashboard..."
        echo "📊 Dashboard will be available at: http://localhost:8501"
        echo ""
        streamlit run pchi_claims_dashboard.py
        ;;
    3)
        echo ""
        echo "🧪 Running tests..."
        python3 test_pchi_dashboard.py
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

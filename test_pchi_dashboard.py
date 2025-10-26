"""
Test script for PCHI Dashboard
Tests the PCHI analyzer without authentication
"""
from core.pchi_analyzer import PCHIAnalyzer
import json

def test_pchi_analyzer():
    """Test PCHI analyzer functionality"""
    print("=" * 60)
    print("Testing PCHI Claims Dashboard Analyzer")
    print("=" * 60)

    # Initialize analyzer
    csv_path = 'data/uploads/20251024 PCHI Claim summary 2020 - now.csv'
    print(f"\n📂 Loading data from: {csv_path}")

    try:
        analyzer = PCHIAnalyzer(csv_path)
        print("✅ Data loaded successfully!")

        # Test 1: Get filter options
        print("\n1️⃣ Testing filter options...")
        options = analyzer.get_filter_options()
        print(f"   Available years: {options.get('years', [])}")
        print(f"   Available statuses: {options.get('statuses', [])}")
        print(f"   Available BUs: {options.get('business_units', [])}")
        print(f"   Products count: {len(options.get('products', []))}")

        # Test 2: Get KPIs
        print("\n2️⃣ Testing KPI summary...")
        kpis = analyzer.get_kpi_summary()
        print(f"   Total Claims: {kpis['total_claims']:,}")
        print(f"   Total Approved: ฿{kpis['total_approved']:,.2f}")
        print(f"   Approval Rate: {kpis['approval_rate']:.2f}%")

        # Test 3: Get claims trend
        print("\n3️⃣ Testing claims trend...")
        trends = analyzer.get_claims_trend()
        print(f"   Months: {len(trends['labels'])}")
        print(f"   Sample months: {trends['labels'][:5]}")

        # Test 4: Get top providers
        print("\n4️⃣ Testing top providers...")
        providers = analyzer.get_top_providers(limit=5)
        print(f"   Top 5 providers:")
        for i, (label, value) in enumerate(zip(providers['labels'], providers['values']), 1):
            print(f"   {i}. {label}: ฿{value:,.2f}")

        # Test 5: Get business unit analysis
        print("\n5️⃣ Testing business unit analysis...")
        bu_data = analyzer.get_bu_analysis()
        print(f"   Business units: {len(bu_data['labels'])}")
        for label, count in zip(bu_data['labels'], bu_data['claim_counts']):
            print(f"   {label}: {count:,} claims")

        # Test 6: Get age distribution
        print("\n6️⃣ Testing age distribution...")
        age_data = analyzer.get_age_distribution()
        print(f"   Age groups:")
        for label, count in zip(age_data['labels'], age_data['values']):
            print(f"   {label}: {count:,} claims")

        # Test 7: Test with filters
        print("\n7️⃣ Testing with filters...")
        filters = {
            'years': [2024],
            'statuses': ['Accept']
        }
        filtered_kpis = analyzer.get_kpi_summary(filters)
        print(f"   Filtered (2024, Accept only):")
        print(f"   Total Claims: {filtered_kpis['total_claims']:,}")
        print(f"   Total Approved: ฿{filtered_kpis['total_approved']:,.2f}")

        # Test 8: Get claims data table
        print("\n8️⃣ Testing claims data table...")
        table_data = analyzer.get_claims_data_table(page=1, page_size=10)
        print(f"   Total records: {table_data['total_records']:,}")
        print(f"   Columns: {len(table_data['columns'])}")
        print(f"   Sample columns: {table_data['columns'][:5]}")
        print(f"   Retrieved rows: {len(table_data['data'])}")

        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_pchi_analyzer()

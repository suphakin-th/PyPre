"""
DataBoard - Lightweight Python BI Dashboard
Main application entry point
"""
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import json
import pandas as pd
from datetime import datetime, timedelta
import secrets

from core.data_processor import DataProcessor
from core.chart_builder import ChartBuilder
from core.auth_manager import AuthManager
from core.pchi_analyzer import PCHIAnalyzer

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data/dashboards', exist_ok=True)
os.makedirs('data/datasets', exist_ok=True)

# Initialize managers
auth_manager = AuthManager()
data_processor = DataProcessor()
chart_builder = ChartBuilder()

# Initialize PCHI analyzer (lazy loading)
pchi_analyzer = None

def get_pchi_analyzer():
    """Get or create PCHI analyzer instance"""
    global pchi_analyzer
    if pchi_analyzer is None:
        csv_path = 'data/uploads/20251024 PCHI Claim summary 2020 - now.csv'
        if os.path.exists(csv_path):
            pchi_analyzer = PCHIAnalyzer(csv_path)
    return pchi_analyzer


def login_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ==================== Authentication Routes ====================

@app.route('/')
def index():
    """Landing page - redirect based on auth status"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle login request"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = auth_manager.authenticate(username, password)
    if user:
        session.permanent = True
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'user': {'username': user['username']}})
    
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """Handle registration request"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    success, message = auth_manager.register(username, password, email)
    if success:
        return jsonify({'success': True, 'message': message})
    
    return jsonify({'error': message}), 400


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """Handle logout request"""
    session.clear()
    return jsonify({'success': True})


# ==================== Dashboard Routes ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html', username=session.get('username'))


@app.route('/api/datasets', methods=['GET'])
@login_required
def get_datasets():
    """Get all uploaded datasets for current user"""
    datasets = data_processor.get_user_datasets(session['user_id'])
    return jsonify(datasets)


@app.route('/api/dataset/<dataset_id>', methods=['GET'])
@login_required
def get_dataset_info(dataset_id):
    """Get detailed information about a dataset"""
    info = data_processor.get_dataset_info(dataset_id, session['user_id'])
    if info:
        return jsonify(info)
    return jsonify({'error': 'Dataset not found'}), 404


@app.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle CSV file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400
    
    try:
        filename = secure_filename(file.filename)
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_id'])
        os.makedirs(user_folder, exist_ok=True)
        
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)
        
        # Process the file
        dataset_info = data_processor.process_csv(filepath, session['user_id'], filename)
        
        return jsonify({
            'success': True,
            'dataset': dataset_info
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500


@app.route('/api/dataset/<dataset_id>/preview', methods=['GET'])
@login_required
def preview_dataset(dataset_id):
    """Get preview of dataset (first 100 rows)"""
    rows = int(request.args.get('rows', 100))
    preview = data_processor.get_dataset_preview(dataset_id, session['user_id'], rows)
    
    if preview:
        return jsonify(preview)
    return jsonify({'error': 'Dataset not found'}), 404


@app.route('/api/chart/create', methods=['POST'])
@login_required
def create_chart():
    """Create a chart configuration"""
    data = request.json
    dataset_id = data.get('dataset_id')
    chart_type = data.get('chart_type')
    config = data.get('config')
    
    try:
        chart_data = chart_builder.create_chart(
            dataset_id=dataset_id,
            user_id=session['user_id'],
            chart_type=chart_type,
            config=config
        )
        return jsonify(chart_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/save', methods=['POST'])
@login_required
def save_dashboard():
    """Save dashboard configuration"""
    data = request.json
    dashboard_id = data.get('id', f"dash_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    dashboard_name = data.get('name', 'Untitled Dashboard')
    layout = data.get('layout', [])
    
    dashboard_file = os.path.join('data/dashboards', f"{session['user_id']}_{dashboard_id}.json")
    
    dashboard_data = {
        'id': dashboard_id,
        'name': dashboard_name,
        'user_id': session['user_id'],
        'layout': layout,
        'updated_at': datetime.now().isoformat()
    }
    
    with open(dashboard_file, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    return jsonify({'success': True, 'dashboard_id': dashboard_id})


@app.route('/api/dashboard/load/<dashboard_id>', methods=['GET'])
@login_required
def load_dashboard(dashboard_id):
    """Load saved dashboard configuration"""
    dashboard_file = os.path.join('data/dashboards', f"{session['user_id']}_{dashboard_id}.json")
    
    if os.path.exists(dashboard_file):
        with open(dashboard_file, 'r') as f:
            dashboard_data = json.load(f)
        return jsonify(dashboard_data)
    
    return jsonify({'error': 'Dashboard not found'}), 404


@app.route('/api/dashboards', methods=['GET'])
@login_required
def list_dashboards():
    """List all dashboards for current user"""
    dashboards = []
    user_prefix = f"{session['user_id']}_"
    
    for filename in os.listdir('data/dashboards'):
        if filename.startswith(user_prefix) and filename.endswith('.json'):
            filepath = os.path.join('data/dashboards', filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                dashboards.append({
                    'id': data['id'],
                    'name': data['name'],
                    'updated_at': data['updated_at']
                })
    
    return jsonify(dashboards)


# ==================== PCHI Claims Dashboard Routes ====================

@app.route('/pchi')
@login_required
def pchi_dashboard():
    """PCHI Claims Dashboard page"""
    return render_template('pchi_dashboard.html', username=session.get('username'))


@app.route('/api/pchi/kpis', methods=['POST'])
@login_required
def get_pchi_kpis():
    """Get PCHI KPIs"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        kpis = analyzer.get_kpi_summary(filters)
        return jsonify(kpis)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/trends', methods=['POST'])
@login_required
def get_pchi_trends():
    """Get claims trends"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        trends = analyzer.get_claims_trend(filters)
        return jsonify(trends)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/status', methods=['POST'])
@login_required
def get_pchi_status():
    """Get claim status distribution"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        status = analyzer.get_status_distribution(filters)
        return jsonify(status)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/providers', methods=['POST'])
@login_required
def get_pchi_providers():
    """Get top providers"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        providers = analyzer.get_top_providers(filters, limit=10)
        return jsonify(providers)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/business-units', methods=['POST'])
@login_required
def get_pchi_business_units():
    """Get business unit analysis"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        bu_data = analyzer.get_bu_analysis(filters)
        return jsonify(bu_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/age-distribution', methods=['POST'])
@login_required
def get_pchi_age():
    """Get age distribution"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        age_data = analyzer.get_age_distribution(filters)
        return jsonify(age_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/gender-distribution', methods=['POST'])
@login_required
def get_pchi_gender():
    """Get gender distribution"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        gender_data = analyzer.get_gender_distribution(filters)
        return jsonify(gender_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/benefit-types', methods=['POST'])
@login_required
def get_pchi_benefits():
    """Get benefit type analysis"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        benefit_data = analyzer.get_benefit_type_analysis(filters, limit=10)
        return jsonify(benefit_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/distribution-channels', methods=['POST'])
@login_required
def get_pchi_channels():
    """Get distribution channel analysis"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        channel_data = analyzer.get_distribution_channel_analysis(filters)
        return jsonify(channel_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/products', methods=['POST'])
@login_required
def get_pchi_products():
    """Get product analysis"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        product_data = analyzer.get_product_analysis(filters, limit=10)
        return jsonify(product_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/yearly-comparison', methods=['POST'])
@login_required
def get_pchi_yearly():
    """Get yearly comparison"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        filters = request.json.get('filters', {}) if request.json else {}
        yearly_data = analyzer.get_yearly_comparison(filters)
        return jsonify(yearly_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/table', methods=['POST'])
@login_required
def get_pchi_table():
    """Get claims data table"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        data = request.json if request.json else {}
        filters = data.get('filters', {})
        page = data.get('page', 1)
        page_size = data.get('page_size', 100)

        table_data = analyzer.get_claims_data_table(filters, page, page_size)
        return jsonify(table_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pchi/filter-options', methods=['GET'])
@login_required
def get_pchi_filter_options():
    """Get available filter options"""
    try:
        analyzer = get_pchi_analyzer()
        if not analyzer:
            return jsonify({'error': 'PCHI data not available'}), 404

        options = analyzer.get_filter_options()
        return jsonify(options)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DataBoard - Lightweight BI Dashboard")
    print("="*60)
    print(f"📊 Server starting at: http://localhost:5000")
    print(f"📁 Data folder: {os.path.abspath('data')}")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

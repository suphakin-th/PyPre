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


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DataBoard - Lightweight BI Dashboard")
    print("="*60)
    print(f"📊 Server starting at: http://localhost:5000")
    print(f"📁 Data folder: {os.path.abspath('data')}")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
ADMIN_EMAIL = 'streambase@admin.com'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_services():
    """Load services from JSON file"""
    try:
        with open('data/services.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_services(services):
    """Save services to JSON file"""
    with open('data/services.json', 'w') as f:
        json.dump(services, f, indent=2)

def load_settings():
    """Load settings from JSON file"""
    try:
        with open('data/settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'placeholders': {
                'user': 'User',
                'pass': 'Pass',
                'expiry': 'Expiry',
                'additional': 'Additional'
            }
        }

def save_settings(settings):
    """Save settings to JSON file"""
    with open('data/settings.json', 'w') as f:
        json.dump(settings, f, indent=2)

def generate_env_code():
    """Generate environment code for GitHub updates"""
    services = load_services()
    env_code = f"SERVICES_UPDATE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(services)}"
    return env_code

@app.route('/')
def index():
    services = load_services()
    return render_template('index.html', services=services)

@app.route('/service/<service_id>')
def service_detail(service_id):
    services = load_services()
    service = next((s for s in services if s['id'] == service_id), None)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('index'))
    
    settings = load_settings()
    return render_template('service.html', service=service, placeholders=settings.get('placeholders', {}))

@app.route('/admin')
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    email = request.form.get('email', '').strip().lower()
    if email == ADMIN_EMAIL:
        session['admin_logged_in'] = True
        flash('Successfully logged in as admin', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid email address', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    services = load_services()
    env_code = generate_env_code()
    return render_template('admin_dashboard.html', services=services, env_code=env_code)

@app.route('/admin/service/new')
def admin_service_new():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    settings = load_settings()
    return render_template('admin_service_form.html', service=None, placeholders=settings.get('placeholders', {}))

@app.route('/admin/service/<service_id>/edit')
def admin_service_edit(service_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    services = load_services()
    service = next((s for s in services if s['id'] == service_id), None)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    settings = load_settings()
    return render_template('admin_service_form.html', service=service, placeholders=settings.get('placeholders', {}))

@app.route('/admin/service/save', methods=['POST'])
def admin_service_save():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    services = load_services()
    service_id = request.form.get('service_id')
    
    # Handle file upload
    icon_path = None
    if 'icon_file' in request.files:
        file = request.files['icon_file']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            icon_path = f"uploads/{filename}"
    
    # Parse accounts based on account type
    account_type = request.form.get('account_type', 'credentials')
    accounts_text = request.form.get('accounts', '').strip()
    accounts = []
    
    if accounts_text:
        for line in accounts_text.split('\n'):
            line = line.strip()
            if line:
                if account_type == 'cookies':
                    accounts.append({'type': 'cookies', 'data': line})
                else:
                    # Parse credentials format: user|pass|expiry|additional or email:pass format
                    account = {'type': 'credentials'}
                    
                    # Check if it's email:pass format
                    if ':' in line and '|' not in line:
                        parts = line.split(':', 1)  # Split only on first colon
                        if len(parts) == 2:
                            account['user'] = parts[0].strip()
                            account['pass'] = parts[1].strip()
                    else:
                        # Parse pipe-separated format: user|pass|expiry|additional
                        parts = line.split('|')
                        if len(parts) >= 1 and parts[0].strip():
                            account['user'] = parts[0].strip()
                        if len(parts) >= 2 and parts[1].strip():
                            account['pass'] = parts[1].strip()
                        if len(parts) >= 3 and parts[2].strip():
                            account['expiry'] = parts[2].strip()
                        if len(parts) >= 4 and parts[3].strip():
                            account['additional'] = parts[3].strip()
                    
                    # Only add the account if it has at least one field
                    if any(key in account for key in ['user', 'pass', 'expiry', 'additional']):
                        accounts.append(account)
    
    # Parse placeholders
    placeholders = {}
    for key in ['user', 'pass', 'expiry', 'additional']:
        placeholder_value = request.form.get(f'placeholder_{key}', '').strip()
        if placeholder_value:
            placeholders[key] = placeholder_value
    
    service_data = {
        'id': service_id or str(uuid.uuid4()),
        'name': request.form.get('name', '').strip(),
        'icon_class': request.form.get('icon_class', '').strip(),
        'icon_path': icon_path or request.form.get('existing_icon_path'),
        'color': request.form.get('color', '').strip(),
        'account_type': account_type,
        'accounts': accounts,
        'comments': request.form.get('comments', '').strip(),
        'placeholders': placeholders,
        'updated_at': datetime.now().isoformat(),
        'is_new': True  # Mark as new for the indicator
    }
    
    if service_id:
        # Update existing service
        for i, service in enumerate(services):
            if service['id'] == service_id:
                services[i] = service_data
                break
        flash('Service updated successfully', 'success')
    else:
        # Add new service
        services.append(service_data)
        flash('Service created successfully', 'success')
    
    save_services(services)
    
    # Update global placeholders if provided
    settings = load_settings()
    if any(request.form.get(f'placeholder_{key}') for key in ['user', 'pass', 'expiry', 'additional']):
        for key in ['user', 'pass', 'expiry', 'additional']:
            placeholder_value = request.form.get(f'placeholder_{key}', '').strip()
            if placeholder_value:
                settings['placeholders'][key] = placeholder_value
        save_settings(settings)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/service/<service_id>/delete', methods=['POST'])
def admin_service_delete(service_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    services = load_services()
    services = [s for s in services if s['id'] != service_id]
    save_services(services)
    
    flash('Service deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/service/<service_id>/mark_old', methods=['POST'])
def admin_service_mark_old(service_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    services = load_services()
    for service in services:
        if service['id'] == service_id:
            service['is_new'] = False
            break
    
    save_services(services)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

// Dashboard JavaScript
let grid;
let datasets = [];
let selectedDataset = null;
let currentWidgetId = null;
let widgetCounter = 0;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeGrid();
    loadDatasets();
    setupFileUpload();
});

// Initialize GridStack
function initializeGrid() {
    grid = GridStack.init({
        cellHeight: 80,
        acceptWidgets: true,
        removable: false,
        float: true,
        disableOneColumnMode: true,
        animate: true
    });
}

// Load datasets
async function loadDatasets() {
    try {
        const response = await fetch('/api/datasets');
        if (response.ok) {
            datasets = await response.json();
            renderDatasetsList();
        }
    } catch (error) {
        console.error('Failed to load datasets:', error);
    }
}

// Render datasets list
function renderDatasetsList() {
    const container = document.getElementById('datasets-list');
    
    if (datasets.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #6b7280; font-size: 13px; padding: 20px;">No datasets uploaded yet</div>';
        return;
    }
    
    container.innerHTML = datasets.map(dataset => `
        <div class="dataset-item ${selectedDataset?.id === dataset.id ? 'active' : ''}" 
             onclick="selectDataset('${dataset.id}')">
            <div class="dataset-name">${dataset.filename}</div>
            <div class="dataset-meta">${dataset.rows} rows × ${dataset.columns} cols</div>
        </div>
    `).join('');
}

// Select dataset
function selectDataset(datasetId) {
    selectedDataset = datasets.find(d => d.id === datasetId);
    renderDatasetsList();
    showToast('Dataset selected: ' + selectedDataset.filename);
}

// File upload
function setupFileUpload() {
    const uploadArea = document.getElementById('file-upload-area');
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
}

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    document.getElementById('upload-progress').style.display = 'block';
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('File uploaded successfully!');
            closeModal('upload-modal');
            await loadDatasets();
            document.getElementById('file-input').value = '';
        } else {
            alert('Upload failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Upload failed: ' + error.message);
    } finally {
        document.getElementById('upload-progress').style.display = 'none';
    }
}

// Add widget
function addWidget(type) {
    if (!selectedDataset) {
        alert('Please select a dataset first!');
        return;
    }
    
    currentWidgetId = 'widget-' + (++widgetCounter);
    document.getElementById('chart-type').value = type;
    openChartModal();
}

// Chart configuration
async function updateColumnOptions() {
    const datasetId = document.getElementById('chart-dataset').value;
    
    if (!datasetId) return;
    
    try {
        const response = await fetch(`/api/dataset/${datasetId}`);
        if (response.ok) {
            const data = await response.json();
            
            const xSelect = document.getElementById('chart-x-column');
            const ySelect = document.getElementById('chart-y-column');
            
            xSelect.innerHTML = '<option value="">Select column...</option>' +
                data.columns_info.map(col => 
                    `<option value="${col.name}">${col.name} (${col.type})</option>`
                ).join('');
            
            ySelect.innerHTML = '<option value="">Select column...</option>' +
                data.columns_info.filter(col => col.type === 'numeric').map(col =>
                    `<option value="${col.name}">${col.name}</option>`
                ).join('');
        }
    } catch (error) {
        console.error('Failed to load columns:', error);
    }
}

// Create chart
async function createChart() {
    const datasetId = document.getElementById('chart-dataset').value;
    const chartType = document.getElementById('chart-type').value;
    const xColumn = document.getElementById('chart-x-column').value;
    const yColumn = document.getElementById('chart-y-column').value;
    const aggregation = document.getElementById('chart-aggregation').value;
    const limit = parseInt(document.getElementById('chart-limit').value);
    
    if (!datasetId) {
        alert('Please select a dataset');
        return;
    }
    
    if (chartType !== 'table' && !xColumn) {
        alert('Please select X-axis column');
        return;
    }
    
    const config = {
        x_column: xColumn,
        y_column: yColumn,
        aggregation: aggregation,
        limit: limit
    };
    
    try {
        const response = await fetch('/api/chart/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                dataset_id: datasetId,
                chart_type: chartType,
                config: config
            })
        });
        
        if (response.ok) {
            const chartData = await response.json();
            addChartWidget(currentWidgetId, chartData);
            closeModal('chart-modal');
            hideEmptyState();
        } else {
            const error = await response.json();
            alert('Failed to create chart: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Failed to create chart: ' + error.message);
    }
}

// Add chart widget to grid
function addChartWidget(widgetId, chartData) {
    const widgetHtml = `
        <div class="grid-stack-item" gs-w="6" gs-h="4" gs-id="${widgetId}">
            <div class="grid-stack-item-content">
                <div class="widget-header">
                    <div class="widget-title">${chartData.type.charAt(0).toUpperCase() + chartData.type.slice(1)} Chart</div>
                    <div class="widget-actions">
                        <button class="widget-btn" onclick="removeWidget('${widgetId}')">🗑️</button>
                    </div>
                </div>
                <div class="widget-body">
                    <canvas id="chart-${widgetId}"></canvas>
                    <div id="table-${widgetId}"></div>
                </div>
            </div>
        </div>
    `;
    
    grid.addWidget(widgetHtml);
    
    // Render chart
    setTimeout(() => {
        if (chartData.type === 'table') {
            renderTable(widgetId, chartData.data);
        } else {
            renderChart(widgetId, chartData);
        }
    }, 100);
}

// Render chart using Chart.js
function renderChart(widgetId, chartData) {
    const canvas = document.getElementById(`chart-${widgetId}`);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    let chartConfig;
    
    if (chartData.type === 'scatter') {
        chartConfig = {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Data Points',
                    data: chartData.data.data,
                    backgroundColor: 'rgba(102, 126, 234, 0.5)',
                    borderColor: 'rgba(102, 126, 234, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { title: { display: true, text: chartData.data.x_label } },
                    y: { title: { display: true, text: chartData.data.y_label } }
                }
            }
        };
    } else {
        const colors = generateColors(chartData.data.labels.length);
        
        chartConfig = {
            type: chartData.type === 'horizontal_bar' ? 'bar' : chartData.type,
            data: {
                labels: chartData.data.labels,
                datasets: [{
                    label: chartData.data.y_label || 'Value',
                    data: chartData.data.values,
                    backgroundColor: chartData.type.includes('pie') || chartData.type.includes('doughnut') 
                        ? colors 
                        : 'rgba(102, 126, 234, 0.7)',
                    borderColor: chartData.type.includes('pie') || chartData.type.includes('doughnut')
                        ? colors.map(c => c.replace('0.7', '1'))
                        : 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    fill: chartData.type === 'area'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: chartData.type === 'horizontal_bar' ? 'y' : 'x',
                plugins: {
                    legend: {
                        display: chartData.type.includes('pie') || chartData.type.includes('doughnut'),
                        position: 'right'
                    }
                }
            }
        };
    }
    
    new Chart(ctx, chartConfig);
}

// Render table
function renderTable(widgetId, data) {
    const container = document.getElementById(`table-${widgetId}`);
    if (!container || !data.rows || data.rows.length === 0) return;
    
    const columns = data.columns || Object.keys(data.rows[0]);
    
    let html = '<table><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    data.rows.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            html += `<td>${row[col] !== null && row[col] !== undefined ? row[col] : ''}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// Generate colors
function generateColors(count) {
    const baseColors = [
        'rgba(102, 126, 234, 0.7)',
        'rgba(118, 75, 162, 0.7)',
        'rgba(237, 100, 166, 0.7)',
        'rgba(255, 154, 158, 0.7)',
        'rgba(250, 208, 196, 0.7)',
        'rgba(156, 207, 216, 0.7)',
        'rgba(102, 187, 106, 0.7)',
        'rgba(255, 202, 40, 0.7)'
    ];
    
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    return colors;
}

// Remove widget
function removeWidget(widgetId) {
    const elements = grid.engine.nodes.filter(n => n.id === widgetId);
    if (elements.length > 0) {
        grid.removeWidget(elements[0].el);
    }
    
    if (grid.engine.nodes.length === 0) {
        showEmptyState();
    }
}

// Clear dashboard
function clearDashboard() {
    if (confirm('Are you sure you want to clear all widgets?')) {
        grid.removeAll();
        showEmptyState();
    }
}

// Save dashboard
async function saveDashboard() {
    const layout = grid.save();
    const dashboardName = prompt('Enter dashboard name:', 'My Dashboard');
    
    if (!dashboardName) return;
    
    try {
        const response = await fetch('/api/dashboard/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: dashboardName,
                layout: layout
            })
        });
        
        if (response.ok) {
            showToast('Dashboard saved successfully!');
        } else {
            alert('Failed to save dashboard');
        }
    } catch (error) {
        alert('Failed to save dashboard: ' + error.message);
    }
}

// Modal functions
function openUploadModal() {
    document.getElementById('upload-modal').classList.add('active');
}

function openChartModal() {
    const modal = document.getElementById('chart-modal');
    modal.classList.add('active');
    
    // Populate dataset selector
    const datasetSelect = document.getElementById('chart-dataset');
    datasetSelect.innerHTML = '<option value="">Select dataset...</option>' +
        datasets.map(ds => `<option value="${ds.id}" ${selectedDataset?.id === ds.id ? 'selected' : ''}>${ds.filename}</option>`).join('');
    
    if (selectedDataset) {
        datasetSelect.value = selectedDataset.id;
        updateColumnOptions();
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Close modal on outside click
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

// Show/hide empty state
function showEmptyState() {
    document.getElementById('empty-state').style.display = 'block';
}

function hideEmptyState() {
    document.getElementById('empty-state').style.display = 'none';
}

// Toast notification
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Logout
async function logout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

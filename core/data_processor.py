"""
Data Processor Module
Handles CSV file processing, data extraction, and transformations
"""
import pandas as pd
import json
import os
from datetime import datetime
import hashlib


class DataProcessor:
    """Handles all data processing operations"""
    
    def __init__(self):
        self.datasets_path = 'data/datasets'
        os.makedirs(self.datasets_path, exist_ok=True)
    
    def process_csv(self, filepath, user_id, filename):
        """Process uploaded CSV file and extract metadata"""
        try:
            # Read CSV with efficient memory usage
            df = pd.read_csv(filepath, low_memory=False)
            
            # Generate dataset ID
            dataset_id = hashlib.md5(f"{user_id}_{filename}_{datetime.now()}".encode()).hexdigest()[:16]
            
            # Analyze columns
            columns_info = []
            for col in df.columns:
                col_data = df[col]
                dtype = str(col_data.dtype)
                
                # Determine column type
                if pd.api.types.is_numeric_dtype(col_data):
                    col_type = 'numeric'
                    stats = {
                        'min': float(col_data.min()) if not pd.isna(col_data.min()) else None,
                        'max': float(col_data.max()) if not pd.isna(col_data.max()) else None,
                        'mean': float(col_data.mean()) if not pd.isna(col_data.mean()) else None,
                    }
                elif pd.api.types.is_datetime64_any_dtype(col_data):
                    col_type = 'datetime'
                    stats = {}
                else:
                    col_type = 'categorical'
                    unique_values = col_data.nunique()
                    stats = {
                        'unique_count': int(unique_values),
                        'top_values': col_data.value_counts().head(10).to_dict() if unique_values < 1000 else {}
                    }
                
                columns_info.append({
                    'name': col,
                    'type': col_type,
                    'dtype': dtype,
                    'null_count': int(col_data.isnull().sum()),
                    'stats': stats
                })
            
            # Create dataset metadata
            dataset_meta = {
                'id': dataset_id,
                'user_id': user_id,
                'filename': filename,
                'filepath': filepath,
                'rows': len(df),
                'columns': len(df.columns),
                'columns_info': columns_info,
                'created_at': datetime.now().isoformat(),
                'size_mb': os.path.getsize(filepath) / (1024 * 1024)
            }
            
            # Save metadata
            meta_file = os.path.join(self.datasets_path, f"{dataset_id}.json")
            with open(meta_file, 'w') as f:
                json.dump(dataset_meta, f, indent=2)
            
            return dataset_meta
        
        except Exception as e:
            raise Exception(f"Error processing CSV: {str(e)}")
    
    def get_user_datasets(self, user_id):
        """Get all datasets for a specific user"""
        datasets = []
        
        for filename in os.listdir(self.datasets_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.datasets_path, filename)
                with open(filepath, 'r') as f:
                    meta = json.load(f)
                    if meta.get('user_id') == user_id:
                        datasets.append({
                            'id': meta['id'],
                            'filename': meta['filename'],
                            'rows': meta['rows'],
                            'columns': meta['columns'],
                            'created_at': meta['created_at'],
                            'size_mb': round(meta['size_mb'], 2)
                        })
        
        return sorted(datasets, key=lambda x: x['created_at'], reverse=True)
    
    def get_dataset_info(self, dataset_id, user_id):
        """Get detailed information about a dataset"""
        meta_file = os.path.join(self.datasets_path, f"{dataset_id}.json")
        
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                if meta.get('user_id') == user_id:
                    return meta
        
        return None
    
    def get_dataset_preview(self, dataset_id, user_id, rows=100):
        """Get preview of dataset"""
        meta = self.get_dataset_info(dataset_id, user_id)
        
        if not meta:
            return None
        
        try:
            df = pd.read_csv(meta['filepath'], nrows=rows)
            
            # Convert to JSON-serializable format
            data = df.to_dict('records')
            columns = list(df.columns)
            
            return {
                'columns': columns,
                'data': data,
                'total_rows': meta['rows']
            }
        
        except Exception as e:
            return None
    
    def get_column_data(self, dataset_id, user_id, column_name):
        """Get all data for a specific column"""
        meta = self.get_dataset_info(dataset_id, user_id)
        
        if not meta:
            return None
        
        try:
            df = pd.read_csv(meta['filepath'], usecols=[column_name])
            return df[column_name].tolist()
        
        except Exception as e:
            return None
    
    def aggregate_data(self, dataset_id, user_id, group_by, value_column, agg_func='sum'):
        """Aggregate data by group"""
        meta = self.get_dataset_info(dataset_id, user_id)
        
        if not meta:
            return None
        
        try:
            df = pd.read_csv(meta['filepath'])
            
            # Perform aggregation
            if agg_func == 'sum':
                result = df.groupby(group_by)[value_column].sum()
            elif agg_func == 'mean':
                result = df.groupby(group_by)[value_column].mean()
            elif agg_func == 'count':
                result = df.groupby(group_by)[value_column].count()
            elif agg_func == 'min':
                result = df.groupby(group_by)[value_column].min()
            elif agg_func == 'max':
                result = df.groupby(group_by)[value_column].max()
            else:
                return None
            
            return {
                'labels': result.index.tolist(),
                'values': result.values.tolist()
            }
        
        except Exception as e:
            return None

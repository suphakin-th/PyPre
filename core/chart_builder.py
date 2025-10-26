"""
Chart Builder Module
Generates chart configurations and data for various visualization types
"""
import pandas as pd
from core.data_processor import DataProcessor


class ChartBuilder:
    """Handles chart creation and configuration"""
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.supported_charts = [
            'bar', 'line', 'pie', 'scatter', 'area', 
            'horizontal_bar', 'doughnut', 'table'
        ]
    
    def create_chart(self, dataset_id, user_id, chart_type, config):
        """Create a chart with given configuration"""
        
        if chart_type not in self.supported_charts:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        # Get dataset info
        meta = self.data_processor.get_dataset_info(dataset_id, user_id)
        if not meta:
            raise ValueError("Dataset not found")
        
        # Load data
        df = pd.read_csv(meta['filepath'])
        
        # Extract configuration
        x_column = config.get('x_column')
        y_column = config.get('y_column')
        agg_function = config.get('aggregation', 'sum')
        limit = config.get('limit', 50)
        sort_by = config.get('sort_by', 'value')
        
        if chart_type == 'table':
            return self._create_table(df, config, limit)
        
        # Prepare data based on chart type
        if chart_type in ['bar', 'horizontal_bar', 'line', 'area']:
            chart_data = self._create_categorical_chart(
                df, x_column, y_column, agg_function, limit, sort_by
            )
        elif chart_type in ['pie', 'doughnut']:
            chart_data = self._create_pie_chart(
                df, x_column, y_column, agg_function, limit
            )
        elif chart_type == 'scatter':
            chart_data = self._create_scatter_chart(
                df, x_column, y_column, limit
            )
        else:
            raise ValueError(f"Chart type {chart_type} not implemented")
        
        return {
            'type': chart_type,
            'data': chart_data,
            'config': config
        }
    
    def _create_categorical_chart(self, df, x_column, y_column, agg_func, limit, sort_by):
        """Create data for bar, line, and area charts"""
        
        if not x_column or not y_column:
            raise ValueError("Both x_column and y_column are required")
        
        # Aggregate data
        if agg_func == 'sum':
            grouped = df.groupby(x_column)[y_column].sum()
        elif agg_func == 'mean':
            grouped = df.groupby(x_column)[y_column].mean()
        elif agg_func == 'count':
            grouped = df.groupby(x_column)[y_column].count()
        elif agg_func == 'min':
            grouped = df.groupby(x_column)[y_column].min()
        elif agg_func == 'max':
            grouped = df.groupby(x_column)[y_column].max()
        else:
            grouped = df.groupby(x_column)[y_column].sum()
        
        # Sort
        if sort_by == 'value':
            grouped = grouped.sort_values(ascending=False)
        else:
            grouped = grouped.sort_index()
        
        # Limit results
        grouped = grouped.head(limit)
        
        return {
            'labels': [str(label) for label in grouped.index.tolist()],
            'values': [float(val) if pd.notna(val) else 0 for val in grouped.values.tolist()],
            'x_label': x_column,
            'y_label': y_column
        }
    
    def _create_pie_chart(self, df, category_column, value_column, agg_func, limit):
        """Create data for pie and doughnut charts"""
        
        if not category_column:
            raise ValueError("category_column is required for pie charts")
        
        if value_column:
            # Aggregate by category
            if agg_func == 'count':
                grouped = df.groupby(category_column).size()
            else:
                grouped = df.groupby(category_column)[value_column].sum()
        else:
            # Just count occurrences
            grouped = df[category_column].value_counts()
        
        # Sort and limit
        grouped = grouped.sort_values(ascending=False).head(limit)
        
        return {
            'labels': [str(label) for label in grouped.index.tolist()],
            'values': [float(val) if pd.notna(val) else 0 for val in grouped.values.tolist()]
        }
    
    def _create_scatter_chart(self, df, x_column, y_column, limit):
        """Create data for scatter charts"""
        
        if not x_column or not y_column:
            raise ValueError("Both x_column and y_column are required for scatter charts")
        
        # Sample data if too large
        if len(df) > limit:
            df_sample = df.sample(n=limit)
        else:
            df_sample = df
        
        # Remove rows with null values in either column
        df_clean = df_sample[[x_column, y_column]].dropna()
        
        return {
            'data': [
                {
                    'x': float(row[x_column]) if pd.notna(row[x_column]) else 0,
                    'y': float(row[y_column]) if pd.notna(row[y_column]) else 0
                }
                for _, row in df_clean.iterrows()
            ],
            'x_label': x_column,
            'y_label': y_column
        }
    
    def _create_table(self, df, config, limit):
        """Create data for table view"""
        
        columns = config.get('columns', df.columns.tolist())
        
        # Filter columns
        df_filtered = df[columns].head(limit)
        
        return {
            'columns': columns,
            'rows': df_filtered.to_dict('records')
        }

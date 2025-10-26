"""
PCHI Claims Analyzer
Backend module for analyzing PCHI insurance claims data
"""
import pandas as pd
import numpy as np
from datetime import datetime
import json


class PCHIAnalyzer:
    """Analyzer for PCHI claims data"""

    def __init__(self, csv_path):
        """Initialize with CSV file path"""
        self.csv_path = csv_path
        self.df = None
        self._load_data()

    def _load_data(self):
        """Load and preprocess the claims data"""
        try:
            # Load data
            self.df = pd.read_csv(self.csv_path)

            # Convert date columns
            date_columns = ['POLICY EFF DATE', 'POLICY EXP DATE', 'SICK/FROM', 'SICK/TO',
                           'RECEIPT/DT', 'PAYDATE', 'CHQDATE', 'CREATE_DATE', 'UPDATE_DATE']
            for col in date_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')

            # Convert numeric columns
            numeric_columns = ['INCURRED', 'APPROVED', 'CLAIMED', 'OUTSTANDING',
                              'DED_AMT', 'COPAY_AMT', 'MANUAL_REJECTED_AMT', 'AGE']
            for col in numeric_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

            # Add derived columns
            if 'PAYDATE' in self.df.columns:
                self.df['YEAR'] = self.df['PAYDATE'].dt.year
                self.df['MONTH'] = self.df['PAYDATE'].dt.month
                self.df['QUARTER'] = self.df['PAYDATE'].dt.quarter
                self.df['YEAR_MONTH'] = self.df['PAYDATE'].dt.to_period('M').astype(str)

        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def get_kpi_summary(self, filters=None):
        """Get key performance indicators"""
        df = self._apply_filters(filters)

        total_claims = len(df)
        total_incurred = float(df['INCURRED'].sum()) if 'INCURRED' in df.columns else 0
        total_approved = float(df['APPROVED'].sum()) if 'APPROVED' in df.columns else 0
        total_claimed = float(df['CLAIMED'].sum()) if 'CLAIMED' in df.columns else 0
        total_outstanding = float(df['OUTSTANDING'].sum()) if 'OUTSTANDING' in df.columns else 0

        approval_rate = 0
        if 'CLAIM_STATUS' in df.columns and total_claims > 0:
            approval_rate = float((df['CLAIM_STATUS'] == 'Accept').sum() / total_claims * 100)

        avg_claim_amount = float(df['APPROVED'].mean()) if 'APPROVED' in df.columns else 0

        return {
            'total_claims': total_claims,
            'total_incurred': round(total_incurred, 2),
            'total_approved': round(total_approved, 2),
            'total_claimed': round(total_claimed, 2),
            'total_outstanding': round(total_outstanding, 2),
            'approval_rate': round(approval_rate, 2),
            'avg_claim_amount': round(avg_claim_amount, 2)
        }

    def get_claims_trend(self, filters=None):
        """Get claims trend over time"""
        df = self._apply_filters(filters)

        if 'YEAR_MONTH' not in df.columns:
            return {'labels': [], 'claim_counts': [], 'approved_amounts': [], 'incurred_amounts': []}

        monthly_data = df.groupby('YEAR_MONTH').agg({
            'CL_NO': 'count',
            'INCURRED': 'sum',
            'APPROVED': 'sum'
        }).reset_index()

        return {
            'labels': monthly_data['YEAR_MONTH'].tolist(),
            'claim_counts': monthly_data['CL_NO'].tolist(),
            'approved_amounts': [round(x, 2) for x in monthly_data['APPROVED'].tolist()],
            'incurred_amounts': [round(x, 2) for x in monthly_data['INCURRED'].tolist()]
        }

    def get_status_distribution(self, filters=None):
        """Get claim status distribution"""
        df = self._apply_filters(filters)

        if 'CLAIM_STATUS' not in df.columns:
            return {'labels': [], 'values': []}

        status_counts = df['CLAIM_STATUS'].value_counts()

        return {
            'labels': status_counts.index.tolist(),
            'values': status_counts.values.tolist()
        }

    def get_top_providers(self, filters=None, limit=10):
        """Get top providers by approved amount"""
        df = self._apply_filters(filters)

        if 'PROVIDER' not in df.columns or 'APPROVED' not in df.columns:
            return {'labels': [], 'values': []}

        top_providers = df.groupby('PROVIDER')['APPROVED'].sum().nlargest(limit)

        return {
            'labels': top_providers.index.tolist(),
            'values': [round(x, 2) for x in top_providers.values.tolist()]
        }

    def get_bu_analysis(self, filters=None):
        """Get business unit analysis"""
        df = self._apply_filters(filters)

        if 'BU' not in df.columns:
            return {'labels': [], 'claim_counts': [], 'approved_amounts': []}

        bu_data = df.groupby('BU').agg({
            'CL_NO': 'count',
            'APPROVED': 'sum'
        }).reset_index()

        return {
            'labels': bu_data['BU'].tolist(),
            'claim_counts': bu_data['CL_NO'].tolist(),
            'approved_amounts': [round(x, 2) for x in bu_data['APPROVED'].tolist()]
        }

    def get_age_distribution(self, filters=None):
        """Get age distribution of claimants"""
        df = self._apply_filters(filters)

        if 'AGE' not in df.columns:
            return {'labels': [], 'values': []}

        age_bins = [0, 18, 30, 40, 50, 60, 100]
        age_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']
        df['AGE_GROUP'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels)

        age_dist = df['AGE_GROUP'].value_counts().sort_index()

        return {
            'labels': age_dist.index.tolist(),
            'values': age_dist.values.tolist()
        }

    def get_gender_distribution(self, filters=None):
        """Get gender distribution"""
        df = self._apply_filters(filters)

        if 'Gender' not in df.columns:
            return {'labels': [], 'values': []}

        gender_dist = df['Gender'].value_counts()

        return {
            'labels': gender_dist.index.tolist(),
            'values': gender_dist.values.tolist()
        }

    def get_benefit_type_analysis(self, filters=None, limit=10):
        """Get benefit type analysis"""
        df = self._apply_filters(filters)

        if 'BEN_TYPE_DESC' not in df.columns:
            return {'by_count': {'labels': [], 'values': []}, 'by_amount': {'labels': [], 'values': []}}

        # Top by count
        top_by_count = df['BEN_TYPE_DESC'].value_counts().head(limit)

        # Top by amount
        top_by_amount = df.groupby('BEN_TYPE_DESC')['APPROVED'].sum().nlargest(limit)

        return {
            'by_count': {
                'labels': top_by_count.index.tolist(),
                'values': top_by_count.values.tolist()
            },
            'by_amount': {
                'labels': top_by_amount.index.tolist(),
                'values': [round(x, 2) for x in top_by_amount.values.tolist()]
            }
        }

    def get_distribution_channel_analysis(self, filters=None):
        """Get distribution channel analysis"""
        df = self._apply_filters(filters)

        if 'DISTRIBUTION' not in df.columns:
            return {'labels': [], 'claim_counts': [], 'approved_amounts': [], 'approval_rates': []}

        # Channel performance
        channel_data = df.groupby('DISTRIBUTION').agg({
            'CL_NO': 'count',
            'APPROVED': 'sum'
        }).reset_index()

        # Approval rates
        approval_rates = []
        for channel in channel_data['DISTRIBUTION']:
            channel_df = df[df['DISTRIBUTION'] == channel]
            if len(channel_df) > 0 and 'CLAIM_STATUS' in df.columns:
                rate = (channel_df['CLAIM_STATUS'] == 'Accept').sum() / len(channel_df) * 100
                approval_rates.append(round(rate, 2))
            else:
                approval_rates.append(0)

        return {
            'labels': channel_data['DISTRIBUTION'].tolist(),
            'claim_counts': channel_data['CL_NO'].tolist(),
            'approved_amounts': [round(x, 2) for x in channel_data['APPROVED'].tolist()],
            'approval_rates': approval_rates
        }

    def get_product_analysis(self, filters=None, limit=10):
        """Get product analysis"""
        df = self._apply_filters(filters)

        if 'PRODUCT' not in df.columns:
            return {'labels': [], 'claim_counts': [], 'approved_amounts': []}

        product_data = df.groupby('PRODUCT').agg({
            'CL_NO': 'count',
            'APPROVED': 'sum'
        }).nlargest(limit, 'APPROVED').reset_index()

        return {
            'labels': product_data['PRODUCT'].tolist(),
            'claim_counts': product_data['CL_NO'].tolist(),
            'approved_amounts': [round(x, 2) for x in product_data['APPROVED'].tolist()]
        }

    def get_yearly_comparison(self, filters=None):
        """Get year-over-year comparison"""
        df = self._apply_filters(filters)

        if 'YEAR' not in df.columns:
            return {'labels': [], 'claim_counts': [], 'approved_amounts': []}

        yearly_data = df.groupby('YEAR').agg({
            'CL_NO': 'count',
            'APPROVED': 'sum'
        }).reset_index()

        return {
            'labels': [int(x) for x in yearly_data['YEAR'].tolist()],
            'claim_counts': yearly_data['CL_NO'].tolist(),
            'approved_amounts': [round(x, 2) for x in yearly_data['APPROVED'].tolist()]
        }

    def get_claims_data_table(self, filters=None, page=1, page_size=100):
        """Get paginated claims data for table view"""
        df = self._apply_filters(filters)

        # Select relevant columns
        display_columns = ['CL_NO', 'CLAIM_STATUS', 'PROVIDER', 'PAYDATE',
                          'INCURRED', 'APPROVED', 'CLAIMED', 'BEN_TYPE_DESC',
                          'DIAGNOSIS_DETAILS', 'POLICYHOLDER', 'Member Name']

        available_columns = [col for col in display_columns if col in df.columns]
        df_display = df[available_columns].copy()

        # Convert dates to strings
        for col in df_display.columns:
            if pd.api.types.is_datetime64_any_dtype(df_display[col]):
                df_display[col] = df_display[col].dt.strftime('%Y-%m-%d')

        # Pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        df_page = df_display.iloc[start_idx:end_idx]

        return {
            'columns': df_page.columns.tolist(),
            'data': df_page.fillna('').values.tolist(),
            'total_records': len(df_display),
            'page': page,
            'page_size': page_size,
            'total_pages': (len(df_display) + page_size - 1) // page_size
        }

    def get_filter_options(self):
        """Get available filter options"""
        options = {}

        if 'YEAR' in self.df.columns:
            options['years'] = sorted([int(x) for x in self.df['YEAR'].dropna().unique()])

        if 'CLAIM_STATUS' in self.df.columns:
            options['statuses'] = self.df['CLAIM_STATUS'].dropna().unique().tolist()

        if 'BU' in self.df.columns:
            options['business_units'] = sorted(self.df['BU'].dropna().unique().tolist())

        if 'PRODUCT' in self.df.columns:
            products = self.df['PRODUCT'].dropna().unique().tolist()
            options['products'] = sorted(products)[:20]  # Limit to top 20

        if 'DISTRIBUTION' in self.df.columns:
            options['distribution_channels'] = sorted(self.df['DISTRIBUTION'].dropna().unique().tolist())

        return options

    def _apply_filters(self, filters):
        """Apply filters to dataframe"""
        if filters is None or not filters:
            return self.df.copy()

        df = self.df.copy()

        if 'years' in filters and filters['years'] and 'YEAR' in df.columns:
            df = df[df['YEAR'].isin(filters['years'])]

        if 'statuses' in filters and filters['statuses'] and 'CLAIM_STATUS' in df.columns:
            df = df[df['CLAIM_STATUS'].isin(filters['statuses'])]

        if 'business_units' in filters and filters['business_units'] and 'BU' in df.columns:
            df = df[df['BU'].isin(filters['business_units'])]

        if 'products' in filters and filters['products'] and 'PRODUCT' in df.columns:
            df = df[df['PRODUCT'].isin(filters['products'])]

        if 'distribution_channels' in filters and filters['distribution_channels'] and 'DISTRIBUTION' in df.columns:
            df = df[df['DISTRIBUTION'].isin(filters['distribution_channels'])]

        return df

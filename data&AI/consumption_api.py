import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import calendar

def load_data(file_path='cleaned_filtered_data.csv'):
    """Load and prepare the consumption data"""
    try:
        df = pd.read_csv(file_path)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def get_consumption_data(meter_id: Optional[int] = None, period: str = '24h', 
                        consumption_type: str = 'net') -> Dict:
    """
    Get consumption data for specified period and format for React frontend
    
    Parameters:
    -----------
    meter_id : int, optional
        Specific meter ID. If None, aggregates all meters
    period : str
        Time period: '24h', 'week', 'month', 'year'
    consumption_type : str
        Type of consumption: 'import', 'export', 'net' (import-export)
    
    Returns:
    --------
    dict
        JSON-formatted data for React components
    """
    
    df = load_data()
    
    # Filter by meter if specified
    if meter_id is not None:
        df = df[df['meter_id'] == meter_id]
        if df.empty:
            return {"error": f"No data found for meter {meter_id}"}
    
    # Calculate consumption based on type
    if consumption_type == 'import':
        df['consumption'] = df['import_consumption']
    elif consumption_type == 'export':
        df['consumption'] = df['export_consumption']
    else:  # net consumption
        df['consumption'] = df['import_consumption'] - df['export_consumption']
    
    # Get current time and calculate period start
    now = datetime(2025, 6, 8, 12, 0, 0) # assume today is 2025-06-09 for consistency
    
    if period == '24h':
        start_time = now - timedelta(hours=24)
        df_period = df[df['datetime'] >= start_time]
        return _format_hourly_data(df_period)
    
    elif period == 'week':
        start_time = now - timedelta(days=7)
        df_period = df[df['datetime'] >= start_time]
        return _format_weekly_data(df_period)
    
    elif period == 'month':
        start_time = now - timedelta(days=30)
        df_period = df[df['datetime'] >= start_time]
        return _format_monthly_data(df_period)
    
    elif period == 'year':
        start_time = now - timedelta(days=365)
        df_period = df[df['datetime'] >= start_time]
        return _format_yearly_data(df_period)
    
    else:
        return {"error": f"Invalid period: {period}. Use '24h', 'week', 'month', or 'year'"}

def _format_hourly_data(df: pd.DataFrame) -> Dict:
    """Format data for hourly consumption (last 24 hours)"""
    if df.empty:
        return {"data": [], "period": "24h", "total": 0}
    
    # Group by hour of day
    df['hour'] = df['datetime'].dt.hour
    hourly_consumption = df.groupby('hour')['consumption'].sum().reset_index()
    
    # Ensure all 24 hours are represented
    all_hours = pd.DataFrame({'hour': range(24)})
    hourly_consumption = all_hours.merge(hourly_consumption, on='hour', how='left')
    hourly_consumption['consumption'] = hourly_consumption['consumption'].fillna(0)
    
    # Format for React
    data = [
        {"hour": int(row['hour']), "consumption": round(float(row['consumption']), 3)}
        for _, row in hourly_consumption.iterrows()
    ]
    
    return {
        "data": data,
        "period": "24h",
        "total": round(float(hourly_consumption['consumption'].sum()), 3)
    }

def _format_weekly_data(df: pd.DataFrame) -> Dict:
    """Format data for weekly consumption (last 7 days chronologically)"""
    if df.empty:
        return {"data": [], "period": "week", "total": 0}
    
    # Group by date (not day_name) to get actual daily totals for the last 7 days
    df['date'] = df['datetime'].dt.date
    daily_consumption = df.groupby('date')['consumption'].sum().reset_index()
    
    # Sort by date to get chronological order
    daily_consumption = daily_consumption.sort_values('date')
    
    # Take only the last 7 days (should already be filtered by caller, but ensure it)
    daily_consumption = daily_consumption.tail(7)
    
    # Add day names for each date
    daily_consumption['day_name'] = pd.to_datetime(daily_consumption['date']).dt.day_name()
    daily_consumption['day_short'] = pd.to_datetime(daily_consumption['date']).dt.strftime('%a')
    
    # Format for React - chronological order of actual dates
    data = [
        {
            "day": row['day_short'], 
            "consumption": round(float(row['consumption']), 3),
            "date": row['date'].strftime('%Y-%m-%d')
        }
        for _, row in daily_consumption.iterrows()
    ]
    
    return {
        "data": data,
        "period": "week",
        "total": round(float(daily_consumption['consumption'].sum()), 3)
    }

def _format_monthly_data(df: pd.DataFrame) -> Dict:
    """Format data for monthly consumption (last 30 days)"""
    if df.empty:
        return {"data": [], "period": "month", "total": 0}
    
    # Group by day of month
    df['day'] = df['datetime'].dt.day
    daily_consumption = df.groupby('day')['consumption'].sum().reset_index()
    
    # Get all days in current month
    now = datetime(2025, 6, 8, 12, 0, 0) # assume today is 2025-06-09 for consistency
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    all_days = pd.DataFrame({'day': range(1, days_in_month + 1)})
    daily_consumption = all_days.merge(daily_consumption, on='day', how='left')
    daily_consumption['consumption'] = daily_consumption['consumption'].fillna(0)
    
    # Format for React
    data = [
        {"date": str(int(row['day'])), "consumption": round(float(row['consumption']), 3)}
        for _, row in daily_consumption.iterrows()
    ]
    
    return {
        "data": data,
        "period": "month",
        "total": round(float(daily_consumption['consumption'].sum()), 3)
    }

def _format_yearly_data(df: pd.DataFrame) -> Dict:
    """Format data for yearly consumption (last 12 months)"""
    if df.empty:
        return {"data": [], "period": "year", "total": 0}
    
    # Group by month
    df['month'] = df['datetime'].dt.month
    monthly_consumption = df.groupby('month')['consumption'].sum().reset_index()
    
    # Ensure all months are represented
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    all_months = pd.DataFrame({
        'month': range(1, 13),
        'month_name': month_names
    })
    monthly_consumption = all_months.merge(monthly_consumption, on='month', how='left')
    monthly_consumption['consumption'] = monthly_consumption['consumption'].fillna(0)
    
    # Format for React
    data = [
        {"month": row['month_name'], "consumption": round(float(row['consumption']), 3)}
        for _, row in monthly_consumption.iterrows()
    ]
    
    return {
        "data": data,
        "period": "year",
        "total": round(float(monthly_consumption['consumption'].sum()), 3)
    }

def get_meter_list(file_path='cleaned_filtered_data.csv') -> List[Dict]:
    """Get list of available meters"""
    try:
        df = load_data(file_path)
        meters = df['meter_id'].unique()
        
        meter_info = []
        for meter in sorted(meters):
            meter_data = df[df['meter_id'] == meter]
            meter_info.append({
                "meter_id": int(meter),
                "record_count": len(meter_data),
                "date_range": {
                    "start": meter_data['datetime'].min().isoformat(),
                    "end": meter_data['datetime'].max().isoformat()
                },
                "total_import": round(float(meter_data['import_consumption'].sum()), 3),
                "total_export": round(float(meter_data['export_consumption'].sum()), 3)
            })
        
        return meter_info
    except Exception as e:
        return [{"error": f"Error getting meter list: {str(e)}"}]

# Example usage and testing
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    print("Testing Consumption API Functions")
    print("=" * 40)
    
    # Test meter list
    print("\n1. Getting meter list...")
    meters = get_meter_list()
    print(f"Found {len(meters)} meters")
    
    if meters and "error" not in meters[0]:
        # Test with first meter
        test_meter = meters[0]["meter_id"]
        print(f"\n2. Testing with meter {test_meter}")
        
        # Test different periods with visualizations
        periods = ['24h', 'week', 'month', 'year']
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, period in enumerate(periods):
            print(f"\n{period.upper()} consumption:")
            result = get_consumption_data(meter_id=test_meter, period=period, consumption_type="import")
            
            if "error" not in result and result['data']:
                print(f"  - Data points: {len(result['data'])}")
                print(f"  - Total consumption: {result['total']} Wh")
                print(f"  - Sample data: {result['data'][:3]}")
                
                # Create visualization for each period
                data_points = result['data']
                
                if period == '24h':
                    x_vals = [point['hour'] for point in data_points]
                    x_label = 'Hour of Day'
                    title = f'24-Hour Import Pattern\n(Meter {test_meter})'
                elif period == 'week':
                    x_vals = range(len(data_points))
                    x_label = 'Day of Week'
                    title = f'Weekly Import Pattern\n(Meter {test_meter})'
                    day_labels = [point['day'] for point in data_points]
                    axes[i].set_xticks(x_vals)
                    axes[i].set_xticklabels(day_labels, rotation=45)
                elif period == 'month':
                    x_vals = [int(point['date']) for point in data_points]
                    x_label = 'Day of Month'
                    title = f'Monthly Import Pattern\n(Meter {test_meter})'
                else:  # year
                    x_vals = range(len(data_points))
                    x_label = 'Month'
                    title = f'Yearly Import Pattern\n(Meter {test_meter})'
                    month_labels = [point['month'] for point in data_points]
                    axes[i].set_xticks(x_vals)
                    axes[i].set_xticklabels(month_labels, rotation=45)
                
                y_vals = [point['consumption'] for point in data_points]
                
                # Plot the data
                axes[i].plot(x_vals, y_vals, marker='o', linewidth=2, markersize=4, alpha=0.8)
                axes[i].fill_between(x_vals, y_vals, alpha=0.3)
                axes[i].set_title(title, fontsize=12, fontweight='bold')
                axes[i].set_xlabel(x_label)
                axes[i].set_ylabel('Consumption (Wh)')
                axes[i].grid(True, alpha=0.3)
                
                # Add statistics text
                stats_text = f"Total: {result['total']:.0f} Wh\nAvg: {np.mean(y_vals):.1f} Wh\nMax: {max(y_vals):.1f} Wh"
                axes[i].text(0.02, 0.98, stats_text, transform=axes[i].transAxes, 
                           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
                
            else:
                print(f"  - Error or no data: {result.get('error', 'No data available')}")
                axes[i].text(0.5, 0.5, f'No data for\n{period.upper()} period', 
                           ha='center', va='center', transform=axes[i].transAxes)
                axes[i].set_title(f'{period.upper()} Import Pattern\n(Meter {test_meter})')
        
        plt.tight_layout()
        
        # Save the visualization
        filename = f"consumption_periods_test_{test_meter}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 Visualization saved as: {filename}")
        plt.show()
        
        # Additional detailed example for 24h period
        print(f"\n3. Detailed 24h analysis...")
        result_24h = get_consumption_data(meter_id=test_meter, period='24h', consumption_type="net")
        
        if result_24h['data']:
            fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Net consumption pattern
            hours = [point['hour'] for point in result_24h['data']]
            net_consumption = [point['consumption'] for point in result_24h['data']]
            
            ax1.bar(hours, net_consumption, alpha=0.7, color='blue')
            ax1.set_title(f'24h Net Consumption Pattern\n(Meter {test_meter})')
            ax1.set_xlabel('Hour of Day')
            ax1.set_ylabel('Net Consumption (Wh)')
            ax1.set_xticks(range(0, 24, 2))
            ax1.grid(True, alpha=0.3)
            
            # Compare import vs export
            import_result = get_consumption_data(meter_id=test_meter, period='24h', consumption_type="import")
            export_result = get_consumption_data(meter_id=test_meter, period='24h', consumption_type="export")
            
            if import_result['data'] and export_result['data']:
                import_vals = [point['consumption'] for point in import_result['data']]
                export_vals = [point['consumption'] for point in export_result['data']]
                
                ax2.plot(hours, import_vals, marker='o', label='Import', color='red', linewidth=2)
                ax2.plot(hours, export_vals, marker='s', label='Export', color='green', linewidth=2)
                ax2.set_title(f'24h Import vs Export\n(Meter {test_meter})')
                ax2.set_xlabel('Hour of Day')
                ax2.set_ylabel('Consumption (Wh)')
                ax2.set_xticks(range(0, 24, 2))
                ax2.legend()
                ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            filename2 = f"consumption_24h_detailed_{test_meter}.png"
            plt.savefig(filename2, dpi=300, bbox_inches='tight')
            print(f"📊 Detailed 24h analysis saved as: {filename2}")
            plt.show()
            
            # Print detailed statistics
            print(f"\n📈 24h Statistics for Meter {test_meter}:")
            print(f"  Total Net: {result_24h['total']:.2f} Wh")
            print(f"  Total Import: {import_result['total']:.2f} Wh")
            print(f"  Total Export: {export_result['total']:.2f} Wh")
            print(f"  Peak hour: {hours[net_consumption.index(max(net_consumption))]}:00")
            print(f"  Peak consumption: {max(net_consumption):.2f} Wh")
        
    print("\n" + "=" * 40)
    print("Consumption API ready for REST API integration!")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class TariffCalculator:
    """
    Moldova Tariff Calculator - Compare Old vs New electricity tariff structures
    
    Old Tariff Coefficients:
    - 7:00-23:00: 1.2
    - 0:00-7:00 and 23:00-24:00: 0.8
    
    New Tariff Coefficients:
    - 6:00-11:00 and 16:00-24:00: 1.2
    - 11:00-16:00: 1.0
    - 0:00-6:00: 0.5
    """
    
    def __init__(self, data_path='cleaned_filtered_data.csv'):
        self.data_path = data_path
        
        # Define tariff coefficients
        self.old_tariff = {
            'peak': {'hours': [(7, 23)], 'coefficient': 1.2},
            'off_peak': {'hours': [(0, 7), (23, 24)], 'coefficient': 0.8}
        }
        
        self.new_tariff = {
            'peak': {'hours': [(6, 11), (16, 24)], 'coefficient': 1.2},
            'standard': {'hours': [(11, 16)], 'coefficient': 1.0},
            'off_peak': {'hours': [(0, 6)], 'coefficient': 0.5}
        }
    
    def load_data(self) -> pd.DataFrame:
        """Load and prepare consumption data"""
        try:
            df = pd.read_csv(self.data_path)
            df['datetime'] = pd.to_datetime(df['datetime'])
            # Convert from Watts to kWh
            df['import_consumption_kwh'] = df['import_consumption']
            return df.sort_values(['meter_id', 'datetime'])
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_hour_coefficient(self, hour: int, tariff_type: str = 'old') -> float:
        """Get the coefficient for a specific hour based on tariff type"""
        tariff = self.old_tariff if tariff_type == 'old' else self.new_tariff
        
        for period_name, period_info in tariff.items():
            for start_hour, end_hour in period_info['hours']:
                if start_hour <= hour < end_hour:
                    return period_info['coefficient']
        
        return 1.0  # Default coefficient if no match found
    
    def apply_tariff_coefficients(self, df: pd.DataFrame, tariff_type: str = 'old') -> pd.DataFrame:
        """Apply tariff coefficients to consumption data based on hour"""
        df = df.copy()
        df['hour'] = df['datetime'].dt.hour
        
        # Apply coefficients
        df[f'{tariff_type}_coefficient'] = df['hour'].apply(
            lambda h: self.get_hour_coefficient(h, tariff_type)
        )
        
        # Calculate weighted consumption (consumption * coefficient)
        df[f'{tariff_type}_weighted_consumption'] = (
            df['import_consumption_kwh'] * df[f'{tariff_type}_coefficient']
        )
        
        return df
    
    def calculate_monthly_cost(self, meter_id: int, price_per_kwh: float = 4.0, 
                             weeks_for_average: int = 1) -> Dict:
        """
        Calculate monthly cost comparison for a specific meter
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to calculate costs for
        price_per_kwh : float
            Price per kWh in lei
        weeks_for_average : int
            Number of weeks to use for calculating average (default: 1 week)
        
        Returns:
        --------
        dict
            Cost comparison results
        """
        df = self.load_data()
        
        # Filter for specific meter
        meter_df = df[df['meter_id'] == meter_id].copy()
        if meter_df.empty:
            return {"error": f"No data found for meter {meter_id}"}
        
        # Get recent data for averaging
        meter_df = meter_df.sort_values('datetime')
        recent_data = meter_df.tail(weeks_for_average * 24 * 7)  # Last N weeks of hourly data
        
        if len(recent_data) < 24:  # Need at least 24 hours of data
            return {"error": f"Insufficient data for meter {meter_id}"}
        
        # Apply both tariff coefficients
        tariff_data = self.apply_tariff_coefficients(recent_data, 'old')
        tariff_data = self.apply_tariff_coefficients(tariff_data, 'new')
        
        # Calculate weekly averages
        weekly_consumption_old = tariff_data['old_weighted_consumption'].sum() / weeks_for_average
        weekly_consumption_new = tariff_data['new_weighted_consumption'].sum() / weeks_for_average
        
        # Project to monthly (4 weeks)
        monthly_consumption_old = weekly_consumption_old * 4
        monthly_consumption_new = weekly_consumption_new * 4
        
        # Calculate costs
        monthly_cost_old = monthly_consumption_old * price_per_kwh
        monthly_cost_new = monthly_consumption_new * price_per_kwh
        
        # Calculate savings
        savings_amount = monthly_cost_old - monthly_cost_new
        savings_percentage = (savings_amount / monthly_cost_old * 100) if monthly_cost_old > 0 else 0
        
        # Detailed hourly breakdown
        hourly_breakdown = self._get_hourly_breakdown(tariff_data)
        
        return {
            'meter_id': meter_id,
            'price_per_kwh': price_per_kwh,
            'analysis_period': f"{weeks_for_average} week(s)",
            'data_points': len(recent_data),
            'old_tariff': {
                'weekly_weighted_consumption': round(weekly_consumption_old, 3),
                'monthly_weighted_consumption': round(monthly_consumption_old, 3),
                'monthly_cost': round(monthly_cost_old, 2)
            },
            'new_tariff': {
                'weekly_weighted_consumption': round(weekly_consumption_new, 3),
                'monthly_weighted_consumption': round(monthly_consumption_new, 3),
                'monthly_cost': round(monthly_cost_new, 2)
            },
            'comparison': {
                'savings_amount': round(savings_amount, 2),
                'savings_percentage': round(savings_percentage, 1),
                'recommendation': 'New Tariff' if savings_amount > 0 else 'Old Tariff',
                'better_by': round(abs(savings_amount), 2)
            },
            'hourly_breakdown': hourly_breakdown
        }
    
    def _get_hourly_breakdown(self, df: pd.DataFrame) -> Dict:
        """Get detailed hourly breakdown of tariff impacts"""
        hourly_stats = df.groupby('hour').agg({
            'import_consumption_kwh': 'mean',
            'old_coefficient': 'first',
            'new_coefficient': 'first',
            'old_weighted_consumption': 'mean',
            'new_weighted_consumption': 'mean'
        }).round(4)
        
        breakdown = {}
        for hour in range(24):
            if hour in hourly_stats.index:
                row = hourly_stats.loc[hour]
                breakdown[f"hour_{hour:02d}"] = {
                    'consumption_kwh': float(row['import_consumption_kwh']),
                    'old_coefficient': float(row['old_coefficient']),
                    'new_coefficient': float(row['new_coefficient']),
                    'old_weighted': float(row['old_weighted_consumption']),
                    'new_weighted': float(row['new_weighted_consumption']),
                    'difference': float(row['old_weighted_consumption'] - row['new_weighted_consumption'])
                }
            else:
                breakdown[f"hour_{hour:02d}"] = {
                    'consumption_kwh': 0,
                    'old_coefficient': self.get_hour_coefficient(hour, 'old'),
                    'new_coefficient': self.get_hour_coefficient(hour, 'new'),
                    'old_weighted': 0,
                    'new_weighted': 0,
                    'difference': 0
                }
        
        return breakdown
    
    def compare_all_meters(self, price_per_kwh: float = 2.5) -> Dict:
        """Compare tariffs for all available meters"""
        df = self.load_data()
        meters = df['meter_id'].unique()
        
        results = {}
        summary = {
            'total_meters': len(meters),
            'new_tariff_better': 0,
            'old_tariff_better': 0,
            'total_potential_savings': 0
        }
        
        for meter_id in sorted(meters):
            try:
                result = self.calculate_monthly_cost(meter_id, price_per_kwh)
                if 'error' not in result:
                    results[str(meter_id)] = result
                    
                    # Update summary
                    if result['comparison']['savings_amount'] > 0:
                        summary['new_tariff_better'] += 1
                        summary['total_potential_savings'] += result['comparison']['savings_amount']
                    else:
                        summary['old_tariff_better'] += 1
                else:
                    results[str(meter_id)] = result
            except Exception as e:
                results[str(meter_id)] = {"error": str(e)}
        
        return {
            'summary': summary,
            'results': results,
            'price_per_kwh': price_per_kwh
        }
    
    def visualize_tariff_comparison(self, meter_id: int, price_per_kwh: float = 2.5, 
                                  save_plot: bool = True) -> None:
        """Create comprehensive visualization of tariff comparison"""
        result = self.calculate_monthly_cost(meter_id, price_per_kwh)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Hourly Coefficients Comparison
        hours = list(range(24))
        old_coeffs = [self.get_hour_coefficient(h, 'old') for h in hours]
        new_coeffs = [self.get_hour_coefficient(h, 'new') for h in hours]
        
        axes[0, 0].step(hours, old_coeffs, where='mid', label='Old Tariff', linewidth=3, alpha=0.8)
        axes[0, 0].step(hours, new_coeffs, where='mid', label='New Tariff', linewidth=3, alpha=0.8)
        axes[0, 0].fill_between(hours, old_coeffs, alpha=0.3, step='mid')
        axes[0, 0].fill_between(hours, new_coeffs, alpha=0.3, step='mid')
        axes[0, 0].set_title('Tariff Coefficients by Hour of Day')
        axes[0, 0].set_xlabel('Hour of Day')
        axes[0, 0].set_ylabel('Coefficient')
        axes[0, 0].set_xticks(range(0, 24, 2))
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Hourly Consumption Pattern
        hourly_data = result['hourly_breakdown']
        hours = list(range(24))
        consumption = [hourly_data[f'hour_{h:02d}']['consumption_kwh'] for h in hours]
        
        axes[0, 1].bar(hours, consumption, alpha=0.7, color='skyblue')
        axes[0, 1].set_title(f'Meter {meter_id} - Hourly Consumption Pattern')
        axes[0, 1].set_xlabel('Hour of Day')
        axes[0, 1].set_ylabel('Consumption (kWh)')
        axes[0, 1].set_xticks(range(0, 24, 2))
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Weighted Consumption Comparison
        old_weighted = [hourly_data[f'hour_{h:02d}']['old_weighted'] for h in hours]
        new_weighted = [hourly_data[f'hour_{h:02d}']['new_weighted'] for h in hours]
        
        x_pos = np.arange(len(hours))
        width = 0.35
        
        axes[1, 0].bar(x_pos - width/2, old_weighted, width, label='Old Tariff', alpha=0.8)
        axes[1, 0].bar(x_pos + width/2, new_weighted, width, label='New Tariff', alpha=0.8)
        axes[1, 0].set_title('Weighted Consumption Comparison by Hour')
        axes[1, 0].set_xlabel('Hour of Day')
        axes[1, 0].set_ylabel('Weighted Consumption (kWh)')
        axes[1, 0].set_xticks(x_pos[::2])
        axes[1, 0].set_xticklabels([str(h) for h in hours[::2]])
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Monthly Cost Comparison
        categories = ['Old Tariff', 'New Tariff']
        costs = [result['old_tariff']['monthly_cost'], result['new_tariff']['monthly_cost']]
        colors = ['red' if result['comparison']['savings_amount'] <= 0 else 'orange', 
                 'green' if result['comparison']['savings_amount'] > 0 else 'red']
        
        bars = axes[1, 1].bar(categories, costs, color=colors, alpha=0.7)
        axes[1, 1].set_title(f'Monthly Cost Comparison (Meter {meter_id})')
        axes[1, 1].set_ylabel('Monthly Cost (Lei)')
        
        # Add value labels on bars
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{cost:.2f} Lei', ha='center', va='bottom', fontweight='bold')
        
        # Add savings information
        savings = result['comparison']['savings_amount']
        savings_pct = result['comparison']['savings_percentage']
        
        if savings > 0:
            axes[1, 1].text(0.5, max(costs) * 0.8, 
                           f'Savings: {savings:.2f} Lei ({savings_pct:.1f}%)\nRecommendation: {result["comparison"]["recommendation"]}',
                           ha='center', va='center', fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        else:
            axes[1, 1].text(0.5, max(costs) * 0.8,
                           f'Extra Cost: {abs(savings):.2f} Lei ({abs(savings_pct):.1f}%)\nRecommendation: {result["comparison"]["recommendation"]}',
                           ha='center', va='center', fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
        
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Add main title
        fig.suptitle(f'Moldova Tariff Analysis - Meter {meter_id}\nPrice: {price_per_kwh} Lei/kWh', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        if save_plot:
            filename = f"tariff_comparison_meter_{meter_id}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"📊 Visualization saved as: {filename}")
        
        plt.show()


# Example usage and testing
if __name__ == "__main__":
    print("Testing Moldova Tariff Calculator")
    print("=" * 50)
    
    # Initialize calculator
    calculator = TariffCalculator()
    
    try:
        # Load data to see available meters
        df = calculator.load_data()
        meters = df['meter_id'].unique()
        
        print(f"Found {len(meters)} meters: {sorted(meters)}")
        
        if len(meters) > 0:
            # Test with first meter
            test_meter = meters[5]
            price_kwh = 3.96  # Lei per kWh
            
            print(f"\n1. Calculating tariff comparison for meter {test_meter}...")
            print(f"   Price: {price_kwh} Lei/kWh")
            
            result = calculator.calculate_monthly_cost(test_meter, price_kwh)
            
            if 'error' not in result:
                print(f"\n📊 Results for Meter {test_meter}:")
                print(f"   Analysis period: {result['analysis_period']}")
                print(f"   Data points: {result['data_points']}")
                
                print(f"\n   Old Tariff:")
                print(f"     Weekly weighted consumption: {result['old_tariff']['weekly_weighted_consumption']:.3f} kWh")
                print(f"     Monthly weighted consumption: {result['old_tariff']['monthly_weighted_consumption']:.3f} kWh")
                print(f"     Monthly cost: {result['old_tariff']['monthly_cost']:.2f} Lei")
                
                print(f"\n   New Tariff:")
                print(f"     Weekly weighted consumption: {result['new_tariff']['weekly_weighted_consumption']:.3f} kWh")
                print(f"     Monthly weighted consumption: {result['new_tariff']['monthly_weighted_consumption']:.3f} kWh")
                print(f"     Monthly cost: {result['new_tariff']['monthly_cost']:.2f} Lei")
                
                print(f"\n   💰 Comparison:")
                if result['comparison']['savings_amount'] > 0:
                    print(f"     ✅ New tariff saves: {result['comparison']['savings_amount']:.2f} Lei ({result['comparison']['savings_percentage']:.1f}%)")
                    print(f"     🎯 Recommendation: Switch to {result['comparison']['recommendation']}")
                else:
                    print(f"     ❌ New tariff costs extra: {abs(result['comparison']['savings_amount']):.2f} Lei ({abs(result['comparison']['savings_percentage']):.1f}%)")
                    print(f"     🎯 Recommendation: Keep {result['comparison']['recommendation']}")
                
                # Show tariff coefficients for key hours
                print(f"\n   ⏰ Key Hour Coefficients:")
                key_hours = [6, 12, 18, 23]
                for hour in key_hours:
                    old_coef = calculator.get_hour_coefficient(hour, 'old')
                    new_coef = calculator.get_hour_coefficient(hour, 'new')
                    print(f"     {hour:02d}:00 - Old: {old_coef}, New: {new_coef}")
                
                # Generate visualization
                print(f"\n2. Generating visualization...")
                calculator.visualize_tariff_comparison(test_meter, price_kwh)
                
                # Test multiple meters comparison
                print(f"\n3. Comparing all meters...")
                all_results = calculator.compare_all_meters(price_kwh)
                
                print(f"\n📈 Summary for all meters:")
                summary = all_results['summary']
                print(f"   Total meters analyzed: {summary['total_meters']}")
                print(f"   New tariff better for: {summary['new_tariff_better']} meters")
                print(f"   Old tariff better for: {summary['old_tariff_better']} meters")
                print(f"   Total potential monthly savings: {summary['total_potential_savings']:.2f} Lei")
                
                # Show top 3 meters with biggest savings
                valid_results = {k: v for k, v in all_results['results'].items() 
                               if 'error' not in v and v['comparison']['savings_amount'] > 0}
                
                if valid_results:
                    top_savings = sorted(valid_results.items(), 
                                       key=lambda x: x[1]['comparison']['savings_amount'], 
                                       reverse=True)[:3]
                    
                    print(f"\n🏆 Top 3 meters with biggest savings (New Tariff):")
                    for i, (meter, data) in enumerate(top_savings, 1):
                        print(f"   {i}. Meter {meter}: {data['comparison']['savings_amount']:.2f} Lei/month ({data['comparison']['savings_percentage']:.1f}%)")
            else:
                print(f"Error: {result['error']}")
        
    except Exception as e:
        print(f"Error in testing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Moldova Tariff Calculator ready!")
    print("Use calculator.calculate_monthly_cost(meter_id, price_per_kwh) for individual calculations")
    print("Use calculator.compare_all_meters(price_per_kwh) for comprehensive analysis")
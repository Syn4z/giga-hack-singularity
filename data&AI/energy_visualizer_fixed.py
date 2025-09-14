"""
Fixed Energy Consumption and Forecast Visualizer
===============================================

This version is fixed to work with the actual data dates and handles edge cases properly.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Import our API modules
try:
    from consumption_api import load_data
    from consumption_forecast import ConsumptionForecaster
    from energy_api import EnergyAPI
except ImportError as e:
    print(f"Error importing API modules: {e}")
    exit(1)

class FixedEnergyVisualizer:
    """
    Fixed visualization system that works with actual data
    """
    
    def __init__(self, data_file='cleaned_filtered_data.csv'):
        """Initialize the visualizer"""
        self.data_file = data_file
        self.df = load_data(data_file)
        
        # Set up plotting style
        try:
            plt.style.use('seaborn-v0_8')
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (15, 10)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        
        print("🎨 Fixed Energy Visualizer initialized")
        print(f"📁 Data source: {data_file}")
        print(f"📊 Data shape: {self.df.shape}")
        print(f"📅 Date range: {self.df['datetime'].min()} to {self.df['datetime'].max()}")
    
    def get_available_meters(self) -> List[int]:
        """Get list of available meter IDs"""
        return sorted(self.df['meter_id'].unique())
    
    def plot_meter_consumption_patterns(self, meter_id: int, save_plot: bool = True) -> None:
        """
        Plot comprehensive consumption patterns for a specific meter
        """
        print(f"📊 Plotting consumption patterns for meter {meter_id}...")
        
        # Filter data for the specific meter
        meter_data = self.df[self.df['meter_id'] == meter_id].copy()
        
        if meter_data.empty:
            print(f"❌ No data found for meter {meter_id}")
            return
        
        # Add time-based columns
        meter_data['hour'] = meter_data['datetime'].dt.hour
        meter_data['day_name'] = meter_data['datetime'].dt.day_name()
        meter_data['date'] = meter_data['datetime'].dt.date
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Hourly consumption pattern
        hourly_import = meter_data.groupby('hour')['import_consumption'].mean()
        hourly_export = meter_data.groupby('hour')['export_consumption'].mean()
        
        axes[0, 0].plot(hourly_import.index, hourly_import.values, 
                       marker='o', label='Import', linewidth=2, color='blue')
        axes[0, 0].plot(hourly_export.index, hourly_export.values, 
                       marker='s', label='Export', linewidth=2, color='red')
        axes[0, 0].set_title(f'Meter {meter_id} - Average Hourly Consumption')
        axes[0, 0].set_xlabel('Hour of Day')
        axes[0, 0].set_ylabel('Average Consumption (kWh)')
        axes[0, 0].legend()
        axes[0, 0].set_xticks(range(0, 24, 2))
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Daily consumption over time
        daily_consumption = meter_data.groupby('date').agg({
            'import_consumption': 'sum',
            'export_consumption': 'sum'
        })
        
        dates = daily_consumption.index
        axes[0, 1].plot(dates, daily_consumption['import_consumption'], 
                       marker='o', label='Import', linewidth=2, color='blue', alpha=0.7)
        axes[0, 1].plot(dates, daily_consumption['export_consumption'], 
                       marker='s', label='Export', linewidth=2, color='red', alpha=0.7)
        axes[0, 1].set_title(f'Meter {meter_id} - Daily Consumption Over Time')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Daily Consumption (kWh)')
        axes[0, 1].legend()
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Import vs Export comparison
        total_import = meter_data['import_consumption'].sum()
        total_export = meter_data['export_consumption'].sum()
        
        if total_import > 0 or total_export > 0:
            sizes = [total_import, total_export]
            labels = ['Import', 'Export']
            colors = ['lightblue', 'lightcoral']
            
            axes[1, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
            axes[1, 0].set_title(f'Meter {meter_id} - Import vs Export Total')
        else:
            axes[1, 0].text(0.5, 0.5, 'No consumption data', ha='center', va='center')
            axes[1, 0].set_title(f'Meter {meter_id} - Import vs Export Total')
        
        # 4. Consumption distribution histogram
        if total_import > 0:
            import_nonzero = meter_data[meter_data['import_consumption'] > 0]['import_consumption']
            if len(import_nonzero) > 0:
                axes[1, 1].hist(import_nonzero, bins=30, alpha=0.7, color='blue', label='Import')
        
        if total_export > 0:
            export_nonzero = meter_data[meter_data['export_consumption'] > 0]['export_consumption']
            if len(export_nonzero) > 0:
                axes[1, 1].hist(export_nonzero, bins=30, alpha=0.7, color='red', label='Export')
        
        axes[1, 1].set_title(f'Meter {meter_id} - Consumption Distribution')
        axes[1, 1].set_xlabel('Consumption (kWh)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            filename = f"meter_patterns_{meter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"💾 Meter patterns saved as: {filename}")
        
        plt.show()
        
        # Print statistics
        print(f"\n📈 Meter {meter_id} Statistics:")
        print(f"   Total records: {len(meter_data)}")
        print(f"   Date range: {meter_data['datetime'].min()} to {meter_data['datetime'].max()}")
        print(f"   Total import: {total_import:.2f} kWh")
        print(f"   Total export: {total_export:.2f} kWh")
        print(f"   Net consumption: {total_import - total_export:.2f} kWh")
        print(f"   Average import per record: {meter_data['import_consumption'].mean():.2f} kWh")
        print(f"   Average export per record: {meter_data['export_consumption'].mean():.2f} kWh")
    
    def plot_forecast_with_training(self, meter_id: int, forecast_hours: int = 24, save_plot: bool = True) -> None:
        """
        Plot forecasting results with training visualization
        """
        print(f"🔮 Creating forecast visualization for meter {meter_id}...")
        
        try:
            forecaster = ConsumptionForecaster(self.data_file)
            
            # Train model
            print("📚 Training model...")
            training_results = forecaster.train_model(meter_id, 'import')
            
            if 'import_consumption' not in training_results or 'error' in training_results['import_consumption']:
                print(f"❌ Training failed: {training_results}")
                return
            
            # Generate forecast
            print("🔮 Generating forecast...")
            predictions = forecaster.predict(meter_id, forecast_hours, 'import')
            
            if 'import_consumption' not in predictions or 'error' in predictions['import_consumption']:
                print(f"❌ Prediction failed: {predictions}")
                return
            
            # Create visualization
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
            
            # 1. Training metrics
            training_metrics = training_results['import_consumption']
            metrics_text = f"Training Results:\n"
            metrics_text += f"MAE: {training_metrics.get('mae', 0):.2f}\n"
            metrics_text += f"RMSE: {training_metrics.get('rmse', 0):.2f}\n"
            metrics_text += f"MAPE: {training_metrics.get('mape', 0):.2f}%\n"
            metrics_text += f"Training samples: {training_metrics.get('training_samples', 0)}\n"
            metrics_text += f"Test samples: {training_metrics.get('test_samples', 0)}"
            
            ax1.text(0.1, 0.5, metrics_text, transform=ax1.transAxes, fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            ax1.set_title(f'Meter {meter_id} - Model Training Results')
            ax1.axis('off')
            
            # 2. Historical consumption pattern (for context)
            meter_data = self.df[self.df['meter_id'] == meter_id].copy()
            meter_data['hour'] = meter_data['datetime'].dt.hour
            hourly_avg = meter_data.groupby('hour')['import_consumption'].mean()
            
            ax2.bar(hourly_avg.index, hourly_avg.values, alpha=0.7, color='blue', label='Historical Average')
            ax2.set_title('Historical Hourly Import Pattern (for reference)')
            ax2.set_xlabel('Hour of Day')
            ax2.set_ylabel('Average Import (kWh)')
            ax2.legend()
            ax2.set_xticks(range(0, 24, 2))
            ax2.grid(True, alpha=0.3)
            
            # 3. Forecast visualization
            forecast_data = predictions['import_consumption']['forecasts']
            timestamps = [datetime.fromisoformat(point['timestamp']) for point in forecast_data]
            predicted_values = [point['predicted_consumption'] for point in forecast_data]
            
            ax3.plot(timestamps, predicted_values, marker='o', linewidth=2, 
                    color='orange', alpha=0.8, label='Forecast')
            ax3.fill_between(timestamps, predicted_values, alpha=0.3, color='orange')
            
            ax3.set_title(f'Import Consumption Forecast (Next {forecast_hours}h)')
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Predicted Import (kWh)')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Format time axis
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            ax3.xaxis.set_major_locator(mdates.HourLocator(interval=max(1, forecast_hours//8)))
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
            
            # Add forecast statistics
            summary = predictions['import_consumption']['summary']
            stats_text = f"Forecast Summary:\n"
            stats_text += f"Total: {summary['total_predicted']:.2f} kWh\n"
            stats_text += f"Average: {summary['average_hourly']:.2f} kWh/h\n"
            stats_text += f"Max: {summary['max_predicted']:.2f} kWh\n"
            stats_text += f"Min: {summary['min_predicted']:.2f} kWh"
            
            ax3.text(0.02, 0.98, stats_text, transform=ax3.transAxes, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
            
            plt.tight_layout()
            
            if save_plot:
                filename = f"forecast_detailed_{meter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                print(f"💾 Detailed forecast saved as: {filename}")
            
            plt.show()
            
        except Exception as e:
            print(f"❌ Error creating forecast visualization: {e}")
            import traceback
            traceback.print_exc()
    
    def plot_multi_meter_overview(self, meter_ids: List[int] = None, save_plot: bool = True) -> None:
        """
        Create overview comparison of multiple meters
        """
        if meter_ids is None:
            meter_ids = self.get_available_meters()[:5]  # Limit to first 5 meters
        
        print(f"🔄 Creating multi-meter overview for {len(meter_ids)} meters...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Collect data for all meters
        meter_stats = {}
        colors = plt.cm.Set3(np.linspace(0, 1, len(meter_ids)))
        
        for meter_id in meter_ids:
            meter_data = self.df[self.df['meter_id'] == meter_id]
            if not meter_data.empty:
                meter_stats[meter_id] = {
                    'total_import': meter_data['import_consumption'].sum(),
                    'total_export': meter_data['export_consumption'].sum(),
                    'avg_import': meter_data['import_consumption'].mean(),
                    'avg_export': meter_data['export_consumption'].mean(),
                    'records': len(meter_data)
                }
        
        if not meter_stats:
            print("❌ No valid data found for any meters")
            return
        
        # 1. Total consumption comparison
        meters = list(meter_stats.keys())
        total_imports = [meter_stats[m]['total_import'] for m in meters]
        total_exports = [meter_stats[m]['total_export'] for m in meters]
        
        x = np.arange(len(meters))
        width = 0.35
        
        axes[0, 0].bar(x - width/2, total_imports, width, label='Import', alpha=0.7, color='blue')
        axes[0, 0].bar(x + width/2, total_exports, width, label='Export', alpha=0.7, color='red')
        axes[0, 0].set_title('Total Consumption by Meter')
        axes[0, 0].set_xlabel('Meter ID')
        axes[0, 0].set_ylabel('Total Consumption (kWh)')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels([str(m) for m in meters], rotation=45)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # 2. Average consumption comparison
        avg_imports = [meter_stats[m]['avg_import'] for m in meters]
        avg_exports = [meter_stats[m]['avg_export'] for m in meters]
        
        axes[0, 1].bar(x - width/2, avg_imports, width, label='Import', alpha=0.7, color='lightblue')
        axes[0, 1].bar(x + width/2, avg_exports, width, label='Export', alpha=0.7, color='lightcoral')
        axes[0, 1].set_title('Average Consumption per Reading')
        axes[0, 1].set_xlabel('Meter ID')
        axes[0, 1].set_ylabel('Average Consumption (kWh)')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels([str(m) for m in meters], rotation=45)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # 3. Net consumption (Import - Export)
        net_consumption = [meter_stats[m]['total_import'] - meter_stats[m]['total_export'] for m in meters]
        colors_net = ['green' if x >= 0 else 'red' for x in net_consumption]
        
        axes[1, 0].bar(range(len(meters)), net_consumption, color=colors_net, alpha=0.7)
        axes[1, 0].set_title('Net Consumption (Import - Export)')
        axes[1, 0].set_xlabel('Meter ID')
        axes[1, 0].set_ylabel('Net Consumption (kWh)')
        axes[1, 0].set_xticks(range(len(meters)))
        axes[1, 0].set_xticklabels([str(m) for m in meters], rotation=45)
        axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.5)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Data availability (number of records)
        record_counts = [meter_stats[m]['records'] for m in meters]
        
        axes[1, 1].bar(range(len(meters)), record_counts, alpha=0.7, color='purple')
        axes[1, 1].set_title('Data Availability (Number of Records)')
        axes[1, 1].set_xlabel('Meter ID')
        axes[1, 1].set_ylabel('Number of Records')
        axes[1, 1].set_xticks(range(len(meters)))
        axes[1, 1].set_xticklabels([str(m) for m in meters], rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_plot:
            filename = f"multi_meter_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"💾 Multi-meter overview saved as: {filename}")
        
        plt.show()
        
        # Print summary statistics
        print(f"\n📊 Multi-Meter Summary:")
        for meter_id in meters:
            stats = meter_stats[meter_id]
            print(f"   Meter {meter_id}:")
            print(f"     Records: {stats['records']}")
            print(f"     Total Import: {stats['total_import']:.2f} kWh")
            print(f"     Total Export: {stats['total_export']:.2f} kWh")
            print(f"     Net: {stats['total_import'] - stats['total_export']:.2f} kWh")
    
    def create_simple_dashboard(self, meter_id: int, save_plot: bool = True) -> None:
        """
        Create a simple dashboard that works with available data
        """
        print(f"📊 Creating simple dashboard for meter {meter_id}...")
        
        meter_data = self.df[self.df['meter_id'] == meter_id].copy()
        
        if meter_data.empty:
            print(f"❌ No data found for meter {meter_id}")
            return
        
        # Add time features
        meter_data['hour'] = meter_data['datetime'].dt.hour
        meter_data['date'] = meter_data['datetime'].dt.date
        meter_data['day_name'] = meter_data['datetime'].dt.day_name()
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        
        # 1. Hourly pattern
        hourly_import = meter_data.groupby('hour')['import_consumption'].mean()
        axes[0, 0].bar(hourly_import.index, hourly_import.values, alpha=0.7, color='blue')
        axes[0, 0].set_title('Average Import by Hour')
        axes[0, 0].set_xlabel('Hour')
        axes[0, 0].set_ylabel('Average Import (kWh)')
        axes[0, 0].set_xticks(range(0, 24, 4))
        
        # 2. Daily totals
        daily_totals = meter_data.groupby('date').agg({
            'import_consumption': 'sum',
            'export_consumption': 'sum'
        })
        
        axes[0, 1].plot(daily_totals.index, daily_totals['import_consumption'], 
                       marker='o', label='Import', color='blue')
        axes[0, 1].plot(daily_totals.index, daily_totals['export_consumption'], 
                       marker='s', label='Export', color='red')
        axes[0, 1].set_title('Daily Consumption Totals')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Daily Total (kWh)')
        axes[0, 1].legend()
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Import vs Export pie chart
        total_import = meter_data['import_consumption'].sum()
        total_export = meter_data['export_consumption'].sum()
        
        if total_import > 0 or total_export > 0:
            axes[0, 2].pie([total_import, total_export], labels=['Import', 'Export'], 
                          autopct='%1.1f%%', colors=['lightblue', 'lightcoral'])
            axes[0, 2].set_title('Import vs Export Distribution')
        else:
            axes[0, 2].text(0.5, 0.5, 'No consumption data', ha='center', va='center')
            axes[0, 2].set_title('Import vs Export Distribution')
        
        # 4. Export hourly pattern
        hourly_export = meter_data.groupby('hour')['export_consumption'].mean()
        axes[1, 0].bar(hourly_export.index, hourly_export.values, alpha=0.7, color='red')
        axes[1, 0].set_title('Average Export by Hour')
        axes[1, 0].set_xlabel('Hour')
        axes[1, 0].set_ylabel('Average Export (kWh)')
        axes[1, 0].set_xticks(range(0, 24, 4))
        
        # 5. Consumption over time (scatter plot)
        axes[1, 1].scatter(meter_data['datetime'], meter_data['import_consumption'], 
                          alpha=0.6, s=1, color='blue', label='Import')
        axes[1, 1].scatter(meter_data['datetime'], meter_data['export_consumption'], 
                          alpha=0.6, s=1, color='red', label='Export')
        axes[1, 1].set_title('Consumption Over Time')
        axes[1, 1].set_xlabel('Date/Time')
        axes[1, 1].set_ylabel('Consumption (kWh)')
        axes[1, 1].legend()
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Statistics summary
        axes[1, 2].axis('off')
        stats_text = f"METER {meter_id} SUMMARY\n\n"
        stats_text += f"Data Points: {len(meter_data):,}\n\n"
        stats_text += f"Date Range:\n{meter_data['datetime'].min().strftime('%Y-%m-%d')}\n"
        stats_text += f"to {meter_data['datetime'].max().strftime('%Y-%m-%d')}\n\n"
        stats_text += f"Total Import: {total_import:,.2f} kWh\n"
        stats_text += f"Total Export: {total_export:,.2f} kWh\n"
        stats_text += f"Net Consumption: {total_import - total_export:,.2f} kWh\n\n"
        stats_text += f"Avg Import/Reading: {meter_data['import_consumption'].mean():.2f} kWh\n"
        stats_text += f"Avg Export/Reading: {meter_data['export_consumption'].mean():.2f} kWh\n\n"
        stats_text += f"Max Import: {meter_data['import_consumption'].max():.2f} kWh\n"
        stats_text += f"Max Export: {meter_data['export_consumption'].max():.2f} kWh"
        
        axes[1, 2].text(0.1, 0.9, stats_text, transform=axes[1, 2].transAxes, fontsize=10,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        fig.suptitle(f'Energy Consumption Dashboard - Meter {meter_id}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_plot:
            filename = f"simple_dashboard_{meter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"💾 Simple dashboard saved as: {filename}")
        
        plt.show()

def main():
    """Main function for fixed visualizer"""
    print("🎨 Fixed Energy Visualizer")
    print("=" * 40)
    
    visualizer = FixedEnergyVisualizer()
    meters = visualizer.get_available_meters()
    
    if not meters:
        print("❌ No meters found in data")
        return
    
    print(f"📊 Available meters: {meters}")
    
    # Use first meter for demonstrations
    demo_meter = meters[1]
    
    try:
        print(f"\n1. 📈 Meter Consumption Patterns")
        visualizer.plot_meter_consumption_patterns(demo_meter)
        
        print(f"\n2. 🔮 Forecast Visualization")
        visualizer.plot_forecast_with_training(demo_meter, 24)
        
        print(f"\n3. 🔄 Multi-Meter Overview")
        visualizer.plot_multi_meter_overview(meters[:3])
        
        print(f"\n4. 📊 Simple Dashboard")
        visualizer.create_simple_dashboard(demo_meter)
        
    except KeyboardInterrupt:
        print("\n⏹️ Visualization interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Visualization complete!")

if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import joblib
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class ConsumptionForecaster:
    """
    Forecasting system for energy consumption prediction
    """
    
    def __init__(self, data_path='cleaned_filtered_data.csv', models_dir='models'):
        self.data_path = data_path
        self.models_dir = models_dir
        self.models = {}
        self.scalers = {}
        self.feature_columns = {}
        
        # Create models directory if it doesn't exist
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
    
    def load_data(self) -> pd.DataFrame:
        """Load and prepare the consumption data"""
        try:
            df = pd.read_csv(self.data_path)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df['import_consumption'] = df['import_consumption'] * 1000
            df['export_consumption'] = df['export_consumption'] * 1000
            return df.sort_values(['meter_id', 'datetime'])
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create additional features that might help with prediction
        """
        df = df.copy()
        
        # Time-based features
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['day_of_month'] = df['datetime'].dt.day
        df['month'] = df['datetime'].dt.month
        df['quarter'] = df['datetime'].dt.quarter
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Cyclical features (to capture seasonal patterns)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Lag features (previous consumption values)
        for meter in df['meter_id'].unique():
            meter_mask = df['meter_id'] == meter
            meter_df = df.loc[meter_mask].copy()
            
            # Create lag features for each meter separately
            for lag in [1, 2, 3, 6, 12, 24]:  # 1h, 2h, 3h, 6h, 12h, 24h ago
                df.loc[meter_mask, f'import_lag_{lag}'] = meter_df['import_consumption'].shift(lag)
                df.loc[meter_mask, f'export_lag_{lag}'] = meter_df['export_consumption'].shift(lag)
            
            # Rolling averages
            for window in [3, 6, 12, 24]:
                df.loc[meter_mask, f'import_rolling_mean_{window}'] = meter_df['import_consumption'].rolling(window=window).mean()
                df.loc[meter_mask, f'export_rolling_mean_{window}'] = meter_df['export_consumption'].rolling(window=window).mean()
                df.loc[meter_mask, f'import_rolling_std_{window}'] = meter_df['import_consumption'].rolling(window=window).std()
                df.loc[meter_mask, f'export_rolling_std_{window}'] = meter_df['export_consumption'].rolling(window=window).std()
        
        # Weather-related features (mock data - in production, you'd get from weather API)
        # Adding seasonal temperature patterns
        df['temp_estimate'] = 15 + 10 * np.sin(2 * np.pi * (df['datetime'].dt.dayofyear - 80) / 365)
        df['temp_estimate'] += 5 * np.sin(2 * np.pi * df['hour'] / 24)  # Daily temperature variation
        
        # Business day indicator
        df['is_business_day'] = ((df['day_of_week'] < 5) & (~df['is_weekend'])).astype(int)
        
        return df
    
    def prepare_training_data(self, df: pd.DataFrame, meter_id: int, 
                            target_column: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare training data for a specific meter and target
        """
        # Filter for specific meter
        meter_df = df[df['meter_id'] == meter_id].copy()
        
        # Feature columns (exclude non-feature columns)
        exclude_cols = ['datetime', 'meter_id', 'import_consumption', 'export_consumption']
        feature_cols = [col for col in meter_df.columns if col not in exclude_cols]
        
        # Remove rows with NaN values (due to lag features)
        meter_df = meter_df.dropna()
        
        if len(meter_df) < 50:  # Need minimum data for training
            raise ValueError(f"Insufficient data for meter {meter_id}: {len(meter_df)} records")
        
        X = meter_df[feature_cols].values
        y = meter_df[target_column].values
        
        return X, y
    
    def train_model(self, meter_id: int, target_type: str = 'both') -> Dict:
        """
        Train forecasting model for a specific meter
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to train model for
        target_type : str
            'import', 'export', or 'both'
        
        Returns:
        --------
        dict
            Training results and model performance
        """
        df = self.load_data()
        df = self.create_features(df)
        
        results = {}
        
        # Train models for import and/or export
        targets = []
        if target_type in ['import', 'both']:
            targets.append('import_consumption')
        if target_type in ['export', 'both']:
            targets.append('export_consumption')
        
        for target in targets:
            try:
                X, y = self.prepare_training_data(df, meter_id, target)
                
                # Split data (use time-based split for time series)
                split_idx = int(len(X) * 0.8)
                X_train, X_test = X[:split_idx], X[split_idx:]
                y_train, y_test = y[:split_idx], y[split_idx:]
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Train multiple models and ensemble them
                models = {
                    'rf': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
                    'gbm': GradientBoostingRegressor(n_estimators=100, random_state=42)
                }
                
                trained_models = {}
                predictions = {}
                
                for model_name, model in models.items():
                    model.fit(X_train_scaled, y_train)
                    pred = model.predict(X_test_scaled)
                    
                    trained_models[model_name] = model
                    predictions[model_name] = pred
                
                # Ensemble prediction (simple average)
                ensemble_pred = np.mean(list(predictions.values()), axis=0)
                
                # Calculate metrics
                mae = mean_absolute_error(y_test, ensemble_pred)
                rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))
                mape = np.mean(np.abs((y_test - ensemble_pred) / (y_test + 1e-8))) * 100
                
                # Store model, scaler, and feature columns
                model_key = f"{meter_id}_{target}"
                self.models[model_key] = trained_models
                self.scalers[model_key] = scaler
                self.feature_columns[model_key] = [col for col in df.columns 
                                                  if col not in ['datetime', 'meter_id', 'import_consumption', 'export_consumption']]
                
                # Save models to disk
                model_path = os.path.join(self.models_dir, f"model_{model_key}.joblib")
                scaler_path = os.path.join(self.models_dir, f"scaler_{model_key}.joblib")
                features_path = os.path.join(self.models_dir, f"features_{model_key}.joblib")
                
                joblib.dump(trained_models, model_path)
                joblib.dump(scaler, scaler_path)
                joblib.dump(self.feature_columns[model_key], features_path)
                
                results[target] = {
                    'mae': float(mae),
                    'rmse': float(rmse),
                    'mape': float(mape),
                    'model_path': model_path,
                    'scaler_path': scaler_path,
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                }
                
            except Exception as e:
                results[target] = {'error': str(e)}
        
        return results
    
    def load_model(self, meter_id: int, target: str) -> bool:
        """Load pre-trained model from disk"""
        model_key = f"{meter_id}_{target}"
        model_path = os.path.join(self.models_dir, f"model_{model_key}.joblib")
        scaler_path = os.path.join(self.models_dir, f"scaler_{model_key}.joblib")
        features_path = os.path.join(self.models_dir, f"features_{model_key}.joblib")
        
        try:
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.models[model_key] = joblib.load(model_path)
                self.scalers[model_key] = joblib.load(scaler_path)
                
                # Load feature columns if available
                if os.path.exists(features_path):
                    self.feature_columns[model_key] = joblib.load(features_path)
                
                return True
            return False
        except Exception:
            return False
    
    def predict(self, meter_id: int, forecast_periods: int = 24, 
                target_type: str = 'both') -> Dict:
        """
        Generate forecasts for the next specified periods
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to forecast for
        forecast_periods : int
            Number of periods (hours) to forecast
        target_type : str
            'import', 'export', or 'both'
        
        Returns:
        --------
        dict
            Forecasting results
        """
        df = self.load_data()
        df = self.create_features(df)
        
        # Get the latest data for this meter
        meter_df = df[df['meter_id'] == meter_id].copy()
        
        if meter_df.empty:
            return {'error': f'No data found for meter {meter_id}'}
        
        # Sort by datetime and get the latest timestamp
        meter_df = meter_df.sort_values('datetime')
        last_datetime = meter_df['datetime'].iloc[-1]
        
        results = {}
        
        # Forecast for each target
        targets = []
        if target_type in ['import', 'both']:
            targets.append('import_consumption')
        if target_type in ['export', 'both']:
            targets.append('export_consumption')
        
        for target in targets:
            model_key = f"{meter_id}_{target}"
            
            # Try to load model if not in memory
            if model_key not in self.models:
                if not self.load_model(meter_id, target):
                    results[target] = {'error': 'Model not found. Please train the model first.'}
                    continue
            
            try:
                # Generate future timestamps
                future_timestamps = [
                    last_datetime + timedelta(hours=i+1) 
                    for i in range(forecast_periods)
                ]
                
                # Create base dataframe for predictions
                future_df = pd.DataFrame({
                    'datetime': future_timestamps,
                    'meter_id': meter_id
                })
                
                # Create time-based features for future data
                future_df['hour'] = future_df['datetime'].dt.hour
                future_df['day_of_week'] = future_df['datetime'].dt.dayofweek
                future_df['day_of_month'] = future_df['datetime'].dt.day
                future_df['month'] = future_df['datetime'].dt.month
                future_df['quarter'] = future_df['datetime'].dt.quarter
                future_df['is_weekend'] = (future_df['day_of_week'] >= 5).astype(int)
                
                # Cyclical features
                future_df['hour_sin'] = np.sin(2 * np.pi * future_df['hour'] / 24)
                future_df['hour_cos'] = np.cos(2 * np.pi * future_df['hour'] / 24)
                future_df['day_sin'] = np.sin(2 * np.pi * future_df['day_of_week'] / 7)
                future_df['day_cos'] = np.cos(2 * np.pi * future_df['day_of_week'] / 7)
                future_df['month_sin'] = np.sin(2 * np.pi * future_df['month'] / 12)
                future_df['month_cos'] = np.cos(2 * np.pi * future_df['month'] / 12)
                
                # Weather estimate
                future_df['temp_estimate'] = 15 + 10 * np.sin(2 * np.pi * (future_df['datetime'].dt.dayofyear - 80) / 365)
                future_df['temp_estimate'] += 5 * np.sin(2 * np.pi * future_df['hour'] / 24)
                
                # Business day indicator
                future_df['is_business_day'] = ((future_df['day_of_week'] < 5) & (~future_df['is_weekend'])).astype(int)
                
                # Use recent data for lag features (simplified approach)
                recent_data = meter_df.tail(50)  # Use last 50 records for lag features
                
                for lag in [1, 2, 3, 6, 12, 24]:
                    if len(recent_data) >= lag:
                        future_df[f'import_lag_{lag}'] = recent_data['import_consumption'].iloc[-lag:].mean()
                        future_df[f'export_lag_{lag}'] = recent_data['export_consumption'].iloc[-lag:].mean()
                    else:
                        future_df[f'import_lag_{lag}'] = recent_data['import_consumption'].mean()
                        future_df[f'export_lag_{lag}'] = recent_data['export_consumption'].mean()
                
                # Rolling averages (use recent historical average)
                for window in [3, 6, 12, 24]:
                    future_df[f'import_rolling_mean_{window}'] = recent_data['import_consumption'].tail(window).mean()
                    future_df[f'export_rolling_mean_{window}'] = recent_data['export_consumption'].tail(window).mean()
                    future_df[f'import_rolling_std_{window}'] = recent_data['import_consumption'].tail(window).std()
                    future_df[f'export_rolling_std_{window}'] = recent_data['export_consumption'].tail(window).std()
                
                # Fill any NaN values with 0
                future_df = future_df.fillna(0)
                
                # Prepare features for prediction using stored feature columns
                if model_key in self.feature_columns:
                    # Use stored feature columns to ensure consistency
                    stored_features = self.feature_columns[model_key]
                    # Ensure all required features are present, add missing ones with 0
                    for feature in stored_features:
                        if feature not in future_df.columns:
                            future_df[feature] = 0
                    X_future = future_df[stored_features].values
                else:
                    # Fallback to original method
                    exclude_cols = ['datetime', 'meter_id', 'import_consumption', 'export_consumption']
                    feature_cols = [col for col in future_df.columns if col not in exclude_cols]
                    X_future = future_df[feature_cols].values
                
                # Scale features
                X_future_scaled = self.scalers[model_key].transform(X_future)
                
                # Generate ensemble predictions
                models = self.models[model_key]
                predictions = []
                
                for model in models.values():
                    pred = model.predict(X_future_scaled)
                    predictions.append(pred / 1000)
                
                # Ensemble prediction (average)
                final_prediction = np.mean(predictions, axis=0)
                
                # Ensure non-negative predictions
                final_prediction = np.maximum(final_prediction, 0) 
                
                # Format results
                forecast_data = []
                for i, (timestamp, pred) in enumerate(zip(future_timestamps, final_prediction)):
                    forecast_data.append({
                        'timestamp': timestamp.isoformat(),
                        'hour_ahead': i + 1,
                        'predicted_consumption': round(float(pred), 3)
                    })
                
                results[target] = {
                    'forecasts': forecast_data,
                    'summary': {
                        'total_predicted': round(float(final_prediction.sum()), 3),
                        'average_hourly': round(float(final_prediction.mean()), 3),
                        'max_predicted': round(float(final_prediction.max()), 3),
                        'min_predicted': round(float(final_prediction.min()), 3)
                    }
                }
                
            except Exception as e:
                results[target] = {'error': str(e)}
        
        return results
    
    def train_all_meters(self, target_type: str = 'both') -> Dict:
        """Train models for all available meters"""
        df = self.load_data()
        meters = df['meter_id'].unique()
        
        results = {}
        
        for meter_id in meters:
            print(f"Training model for meter {meter_id}...")
            try:
                results[str(meter_id)] = self.train_model(meter_id, target_type)
            except Exception as e:
                results[str(meter_id)] = {'error': str(e)}
        
        return results
    
    def get_forecast_summary(self, meter_id: int, days: int = 1) -> Dict:
        """Get forecast summary for next day or week"""
        periods = days * 24  # Convert days to hours
        
        predictions = self.predict(meter_id, periods, 'both')
        
        if 'error' in str(predictions):
            return predictions
        
        summary = {
            'meter_id': meter_id,
            'forecast_period': f'{days} day(s)',
            'forecast_hours': periods,
            'timestamp': datetime(2025, 6, 8, 12, 0, 0).isoformat()  # assume today is 2025-06-09 for consistency
        }
        
        for target in ['import_consumption', 'export_consumption']:
            if target in predictions:
                summary[target.replace('_consumption', '')] = predictions[target]['summary']
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    print("Testing Consumption Forecasting System")
    print("=" * 50)
    
    # Initialize forecaster
    forecaster = ConsumptionForecaster()
    
    try:
        # Load data to see available meters
        df = forecaster.load_data()
        meters = df['meter_id'].unique()
        
        print(f"Found {len(meters)} meters: {sorted(meters)}")
        
        if len(meters) > 0:
            # Test with first meter
            test_meter = meters[5]
            
            print(f"\n1. Training model for meter {test_meter}...")
            train_results = forecaster.train_model(test_meter, 'both')
            
            print("Training Results:")
            for target, result in train_results.items():
                if 'error' not in result:
                    print(f"  {target}:")
                    print(f"    MAE: {result['mae']:.3f} Wh")
                    print(f"    RMSE: {result['rmse']:.3f} Wh")
                    print(f"    MAPE: {result['mape']:.2f}%")
                else:
                    print(f"  {target}: {result['error']}")
            
            # Get historical data for comparison
            meter_df = df[df['meter_id'] == test_meter].copy()
            meter_df = meter_df.sort_values('datetime')
            
            print(f"\n2. Generating 24-hour forecast...")
            forecast_24h = forecaster.predict(test_meter, 24, 'import')
            
            print(f"\n3. Generating 1-week forecast...")
            forecast_1week = forecaster.predict(test_meter, 168, 'import')  # 7 days * 24 hours
            
            # Create visualizations
            fig, axes = plt.subplots(2, 2, figsize=(18, 12))
            
            # Plot 1: Historical vs 24h Forecast
            if 'import_consumption' in forecast_24h and 'error' not in forecast_24h['import_consumption']:
                forecast_data_24h = forecast_24h['import_consumption']['forecasts']
                
                # Get last 24 hours of historical data
                recent_historical = meter_df.tail(24)
                
                # Historical data
                axes[0, 0].plot(recent_historical['datetime'], recent_historical['import_consumption'], 
                               'b-', marker='o', label='Historical', linewidth=2, markersize=4)
                
                # Forecast data
                forecast_timestamps = [datetime.fromisoformat(f['timestamp']) for f in forecast_data_24h]
                forecast_values = [f['predicted_consumption'] for f in forecast_data_24h]
                
                axes[0, 0].plot(forecast_timestamps, forecast_values, 
                               'r-', marker='s', label='24h Forecast', linewidth=2, markersize=4, alpha=0.8)
                
                axes[0, 0].set_title(f'Meter {test_meter} - Historical vs 24h Forecast')
                axes[0, 0].set_xlabel('Time')
                axes[0, 0].set_ylabel('Import Consumption (Wh)')
                axes[0, 0].legend()
                axes[0, 0].grid(True, alpha=0.3)
                axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
                axes[0, 0].tick_params(axis='x', rotation=45)
                
                # Print 24h statistics
                print(f"\n24h Import Forecast:")
                print(f"  Total predicted: {forecast_24h['import_consumption']['summary']['total_predicted']:.2f} Wh")
                print(f"  Average hourly: {forecast_24h['import_consumption']['summary']['average_hourly']:.2f} Wh")
                print(f"  Peak predicted: {forecast_24h['import_consumption']['summary']['max_predicted']:.2f} Wh")
            
            # Plot 2: 24h Forecast Hourly Pattern
            if 'import_consumption' in forecast_24h and 'error' not in forecast_24h['import_consumption']:
                forecast_data_24h = forecast_24h['import_consumption']['forecasts']
                
                # Extract hourly pattern
                hours = [datetime.fromisoformat(f['timestamp']).hour for f in forecast_data_24h]
                values = [f['predicted_consumption'] for f in forecast_data_24h]
                
                axes[0, 1].bar(hours, values, alpha=0.7, color='orange')
                axes[0, 1].set_title(f'Meter {test_meter} - 24h Forecast by Hour')
                axes[0, 1].set_xlabel('Hour of Day')
                axes[0, 1].set_ylabel('Predicted Import (Wh)')
                axes[0, 1].set_xticks(range(0, 24, 2))
                axes[0, 1].grid(True, alpha=0.3)
            
            # Plot 3: 1-Week Forecast
            if 'import_consumption' in forecast_1week and 'error' not in forecast_1week['import_consumption']:
                forecast_data_1week = forecast_1week['import_consumption']['forecasts']
                
                forecast_timestamps = [datetime.fromisoformat(f['timestamp']) for f in forecast_data_1week]
                forecast_values = [f['predicted_consumption'] for f in forecast_data_1week]
                
                axes[1, 0].plot(forecast_timestamps, forecast_values, 
                               'g-', linewidth=1, alpha=0.8, label='1-Week Forecast')
                
                # Add daily averages as overlay
                forecast_df = pd.DataFrame({
                    'timestamp': forecast_timestamps,
                    'consumption': forecast_values
                })
                forecast_df['date'] = pd.to_datetime(forecast_df['timestamp']).dt.date
                daily_avg = forecast_df.groupby('date')['consumption'].mean()
                
                # Plot daily averages as markers
                for date, avg in daily_avg.items():
                    date_start = datetime.combine(date, datetime.min.time())
                    axes[1, 0].scatter(date_start, avg, color='red', s=50, zorder=5)
                
                axes[1, 0].set_title(f'Meter {test_meter} - 1-Week Import Forecast')
                axes[1, 0].set_xlabel('Date/Time')
                axes[1, 0].set_ylabel('Predicted Import (Wh)')
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
                axes[1, 0].tick_params(axis='x', rotation=45)
                
                # Print 1-week statistics
                print(f"\n1-Week Import Forecast:")
                print(f"  Total predicted: {forecast_1week['import_consumption']['summary']['total_predicted']:.2f} Wh")
                print(f"  Average hourly: {forecast_1week['import_consumption']['summary']['average_hourly']:.2f} Wh")
                print(f"  Daily average: {forecast_1week['import_consumption']['summary']['total_predicted']/7:.2f} Wh")
            
            # Plot 4: Daily Forecast Pattern (7 days)
            if 'import_consumption' in forecast_1week and 'error' not in forecast_1week['import_consumption']:
                forecast_data_1week = forecast_1week['import_consumption']['forecasts']
                
                # Group by day and calculate daily totals
                forecast_df = pd.DataFrame({
                    'timestamp': [datetime.fromisoformat(f['timestamp']) for f in forecast_data_1week],
                    'consumption': [f['predicted_consumption'] for f in forecast_data_1week]
                })
                forecast_df['date'] = forecast_df['timestamp'].dt.date
                forecast_df['day_name'] = forecast_df['timestamp'].dt.strftime('%a')
                
                daily_totals = forecast_df.groupby(['date', 'day_name'])['consumption'].sum().reset_index()
                
                axes[1, 1].bar(range(len(daily_totals)), daily_totals['consumption'], alpha=0.7, color='purple')
                axes[1, 1].set_title(f'Meter {test_meter} - Daily Forecast Totals (7 days)')
                axes[1, 1].set_xlabel('Day')
                axes[1, 1].set_ylabel('Daily Total Import (Wh)')
                axes[1, 1].set_xticks(range(len(daily_totals)))
                axes[1, 1].set_xticklabels([f"{row['day_name']}\n{row['date'].strftime('%m-%d')}" 
                                           for _, row in daily_totals.iterrows()], rotation=45)
                axes[1, 1].grid(True, alpha=0.3)
                
                # Add value labels on bars
                for i, total in enumerate(daily_totals['consumption']):
                    axes[1, 1].text(i, total + total*0.01, f'{total:.0f}', 
                                   ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            
            # Save the forecast visualization
            filename = f"forecast_comparison_{test_meter}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n📊 Forecast visualization saved as: {filename}")
            plt.show()
            
            # Additional summary
            print(f"\n4. Forecast Summary Comparison:")
            summary_24h = forecaster.get_forecast_summary(test_meter, 1)
            summary_1week = forecaster.get_forecast_summary(test_meter, 7)
            
            print(f"  24h Summary: {summary_24h}")
            print(f"  1-Week Summary: {summary_1week}")
            
            # Training quality assessment
            if 'import_consumption' in train_results and 'error' not in train_results['import_consumption']:
                mae = train_results['import_consumption']['mae']
                print(f"\n📈 Model Quality Assessment:")
                print(f"  MAE: {mae:.2f} Wh")
                if mae < 100:
                    print("  ✅ Excellent accuracy (MAE < 100 Wh)")
                elif mae < 300:
                    print("  ✅ Good accuracy (MAE < 300 Wh)")
                elif mae < 500:
                    print("  ⚠️  Fair accuracy (MAE < 500 Wh)")
                else:
                    print("  ❌ Poor accuracy (MAE >= 500 Wh)")
    
    except Exception as e:
        print(f"Error in testing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Forecasting system ready for REST API integration!")
"""
Energy Consumption REST API Module
==================================

This module provides the main interface for energy consumption data retrieval 
and forecasting capabilities, designed to be integrated with REST API frameworks
like Flask, FastAPI, or Django.

Main Features:
- Historical consumption data retrieval
- Energy consumption forecasting
- Multiple time period support
- Individual meter analysis
- JSON format optimized for React frontend
"""

from consumption_api import get_consumption_data, get_meter_list
from consumption_forecast import ConsumptionForecaster
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import json

class EnergyAPI:
    """
    Main API class that combines consumption data retrieval and forecasting
    """
    
    def __init__(self, data_path='cleaned_filtered_data.csv'):
        """
        Initialize the Energy API
        
        Parameters:
        -----------
        data_path : str
            Path to the cleaned and filtered data CSV file
        """
        self.data_path = data_path
        self.forecaster = ConsumptionForecaster(data_path)
    
    # ========== CONSUMPTION DATA ENDPOINTS ==========
    
    def get_historical_consumption(self, meter_id: Optional[int] = None, 
                                 period: str = '24h', 
                                 consumption_type: str = 'net') -> Dict:
        """
        Get historical consumption data for React frontend
        
        Endpoint: GET /api/consumption/historical
        
        Parameters:
        -----------
        meter_id : int, optional
            Specific meter ID. If None, aggregates all meters
        period : str
            Time period: '24h', 'week', 'month', 'year'
        consumption_type : str
            Type of consumption: 'import', 'export', 'net'
        
        Returns:
        --------
        dict
            JSON response with consumption data
        """
        try:
            result = get_consumption_data(meter_id, period, consumption_type)
            
            # Add metadata
            result['metadata'] = {
                'meter_id': meter_id,
                'period': period,
                'consumption_type': consumption_type,
                'timestamp': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'data': result,
                'message': 'Historical consumption data retrieved successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve historical consumption data'
            }
    
    def get_meters(self) -> Dict:
        """
        Get list of available meters
        
        Endpoint: GET /api/meters
        
        Returns:
        --------
        dict
            JSON response with meter list
        """
        try:
            meters = get_meter_list()
            
            return {
                'success': True,
                'data': {
                    'meters': meters,
                    'total_count': len(meters)
                },
                'message': 'Meter list retrieved successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve meter list'
            }
    
    def get_meter_details(self, meter_id: int) -> Dict:
        """
        Get detailed information about a specific meter
        
        Endpoint: GET /api/meters/{meter_id}
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to get details for
        
        Returns:
        --------
        dict
            JSON response with meter details
        """
        try:
            meters = get_meter_list()
            meter_info = next((m for m in meters if m.get('meter_id') == meter_id), None)
            
            if not meter_info:
                return {
                    'success': False,
                    'error': f'Meter {meter_id} not found',
                    'message': 'Meter not found'
                }
            
            # Get additional consumption data for different periods
            consumption_data = {}
            for period in ['24h', 'week', 'month']:
                consumption_data[period] = get_consumption_data(meter_id, period, 'net')
            
            return {
                'success': True,
                'data': {
                    'meter_info': meter_info,
                    'consumption_summary': consumption_data
                },
                'message': 'Meter details retrieved successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve meter details'
            }
    
    # ========== FORECASTING ENDPOINTS ==========
    
    def train_forecasting_model(self, meter_id: int, 
                               target_type: str = 'both') -> Dict:
        """
        Train forecasting model for a specific meter
        
        Endpoint: POST /api/forecast/train
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to train model for
        target_type : str
            'import', 'export', or 'both'
        
        Returns:
        --------
        dict
            JSON response with training results
        """
        try:
            results = self.forecaster.train_model(meter_id, target_type)
            
            return {
                'success': True,
                'data': {
                    'meter_id': meter_id,
                    'target_type': target_type,
                    'training_results': results,
                    'timestamp': datetime.now().isoformat()
                },
                'message': 'Model trained successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to train forecasting model'
            }
    
    def get_consumption_forecast(self, meter_id: int, 
                                forecast_hours: int = 24,
                                target_type: str = 'both') -> Dict:
        """
        Get consumption forecast for a specific meter
        
        Endpoint: GET /api/forecast/consumption
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to forecast for
        forecast_hours : int
            Number of hours to forecast (default: 24)
        target_type : str
            'import', 'export', or 'both'
        
        Returns:
        --------
        dict
            JSON response with forecast data
        """
        try:
            forecast_results = self.forecaster.predict(meter_id, forecast_hours, target_type)
            
            # Check if the entire result is an error (e.g., meter not found)
            if 'error' in forecast_results:
                return {
                    'success': False,
                    'error': forecast_results['error'],
                    'message': 'Forecast failed'
                }
            
            # Check if any individual forecasts have errors
            has_errors = any('error' in str(result) for result in forecast_results.values())
            
            if has_errors:
                return {
                    'success': False,
                    'data': forecast_results,
                    'message': 'Some forecasts failed. Check individual results for details.'
                }
            
            return {
                'success': True,
                'data': {
                    'meter_id': meter_id,
                    'forecast_hours': forecast_hours,
                    'target_type': target_type,
                    'forecasts': forecast_results,
                    'timestamp': datetime.now().isoformat()
                },
                'message': 'Forecast generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate forecast'
            }
    
    def get_daily_forecast(self, meter_id: int) -> Dict:
        """
        Get next day forecast for a specific meter
        
        Endpoint: GET /api/forecast/daily/{meter_id}
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to forecast for
        
        Returns:
        --------
        dict
            JSON response with daily forecast
        """
        return self.get_consumption_forecast(meter_id, 24, 'both')
    
    def get_weekly_forecast(self, meter_id: int) -> Dict:
        """
        Get next week forecast for a specific meter
        
        Endpoint: GET /api/forecast/weekly/{meter_id}
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to forecast for
        
        Returns:
        --------
        dict
            JSON response with weekly forecast
        """
        return self.get_consumption_forecast(meter_id, 168, 'both')  # 7 days * 24 hours
    
    def get_forecast_summary(self, meter_id: int, days: int = 1) -> Dict:
        """
        Get forecast summary for a specific meter
        
        Endpoint: GET /api/forecast/summary/{meter_id}
        
        Parameters:
        -----------
        meter_id : int
            Meter ID to get summary for
        days : int
            Number of days to summarize
        
        Returns:
        --------
        dict
            JSON response with forecast summary
        """
        try:
            summary = self.forecaster.get_forecast_summary(meter_id, days)
            
            return {
                'success': True,
                'data': summary,
                'message': 'Forecast summary retrieved successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve forecast summary'
            }
    
    def train_all_meters(self, target_type: str = 'both') -> Dict:
        """
        Train forecasting models for all available meters
        
        Endpoint: POST /api/forecast/train-all
        
        Parameters:
        -----------
        target_type : str
            'import', 'export', or 'both'
        
        Returns:
        --------
        dict
            JSON response with training results for all meters
        """
        try:
            results = self.forecaster.train_all_meters(target_type)
            
            # Count successful vs failed trainings
            successful = sum(1 for result in results.values() if 'error' not in str(result))
            failed = len(results) - successful
            
            return {
                'success': True,
                'data': {
                    'training_results': results,
                    'summary': {
                        'total_meters': len(results),
                        'successful_trainings': successful,
                        'failed_trainings': failed
                    },
                    'timestamp': datetime.now().isoformat()
                },
                'message': f'Training completed. {successful} successful, {failed} failed.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to train models for all meters'
            }
    
    # ========== UTILITY ENDPOINTS ==========
    
    def health_check(self) -> Dict:
        """
        API health check
        
        Endpoint: GET /api/health
        
        Returns:
        --------
        dict
            API health status
        """
        try:
            # Try to load data to check system health
            meters = get_meter_list()
            
            return {
                'success': True,
                'data': {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'available_meters': len(meters),
                    'data_file': self.data_path
                },
                'message': 'API is healthy'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': {
                    'status': 'unhealthy',
                    'timestamp': datetime.now().isoformat()
                },
                'message': 'API health check failed'
            }
    
    def get_api_info(self) -> Dict:
        """
        Get API information and available endpoints
        
        Endpoint: GET /api/info
        
        Returns:
        --------
        dict
            API information
        """
        endpoints = {
            'consumption': {
                'GET /api/consumption/historical': 'Get historical consumption data',
                'GET /api/meters': 'Get list of available meters',
                'GET /api/meters/{meter_id}': 'Get meter details'
            },
            'forecasting': {
                'POST /api/forecast/train': 'Train forecasting model for a meter',
                'GET /api/forecast/consumption': 'Get consumption forecast',
                'GET /api/forecast/daily/{meter_id}': 'Get daily forecast',
                'GET /api/forecast/weekly/{meter_id}': 'Get weekly forecast',
                'GET /api/forecast/summary/{meter_id}': 'Get forecast summary',
                'POST /api/forecast/train-all': 'Train models for all meters'
            },
            'utility': {
                'GET /api/health': 'API health check',
                'GET /api/info': 'API information'
            }
        }
        
        return {
            'success': True,
            'data': {
                'api_name': 'Energy Consumption API',
                'version': '1.0.0',
                'description': 'API for energy consumption data retrieval and forecasting',
                'endpoints': endpoints,
                'data_source': self.data_path,
                'timestamp': datetime.now().isoformat()
            },
            'message': 'API information retrieved successfully'
        }

# Example Flask integration (commented out - uncomment to use with Flask)
"""
from flask import Flask, request, jsonify

app = Flask(__name__)
api = EnergyAPI()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify(api.health_check())

@app.route('/api/info', methods=['GET'])
def api_info():
    return jsonify(api.get_api_info())

@app.route('/api/meters', methods=['GET'])
def get_meters():
    return jsonify(api.get_meters())

@app.route('/api/meters/<int:meter_id>', methods=['GET'])
def get_meter_details(meter_id):
    return jsonify(api.get_meter_details(meter_id))

@app.route('/api/consumption/historical', methods=['GET'])
def get_historical_consumption():
    meter_id = request.args.get('meter_id', type=int)
    period = request.args.get('period', '24h')
    consumption_type = request.args.get('type', 'net')
    
    return jsonify(api.get_historical_consumption(meter_id, period, consumption_type))

@app.route('/api/forecast/train', methods=['POST'])
def train_model():
    data = request.get_json()
    meter_id = data.get('meter_id')
    target_type = data.get('target_type', 'both')
    
    return jsonify(api.train_forecasting_model(meter_id, target_type))

@app.route('/api/forecast/consumption', methods=['GET'])
def get_forecast():
    meter_id = request.args.get('meter_id', type=int)
    forecast_hours = request.args.get('hours', 24, type=int)
    target_type = request.args.get('type', 'both')
    
    return jsonify(api.get_consumption_forecast(meter_id, forecast_hours, target_type))

@app.route('/api/forecast/daily/<int:meter_id>', methods=['GET'])
def get_daily_forecast(meter_id):
    return jsonify(api.get_daily_forecast(meter_id))

@app.route('/api/forecast/weekly/<int:meter_id>', methods=['GET'])
def get_weekly_forecast(meter_id):
    return jsonify(api.get_weekly_forecast(meter_id))

if __name__ == '__main__':
    app.run(debug=True)
"""

# Example usage and testing
if __name__ == "__main__":
    print("Testing Energy API")
    print("=" * 40)
    
    # Initialize API
    api = EnergyAPI()
    
    # Test health check
    print("1. Health Check:")
    health = api.health_check()
    print(f"Status: {health.get('data', {}).get('status', 'unknown')}")
    
    if health['success']:
        # Test getting meters
        print("\n2. Getting Meters:")
        meters_response = api.get_meters()
        
        if meters_response['success'] and meters_response['data']['meters']:
            meters = meters_response['data']['meters']
            print(f"Found {len(meters)} meters")
            
            # Test with first meter
            test_meter = meters[0]['meter_id']
            print(f"\n3. Testing with meter {test_meter}:")
            
            # Get historical data
            historical = api.get_historical_consumption(test_meter, '24h', 'net')
            if historical['success']:
                print(f"Historical data points: {len(historical['data']['data'])}")
            
            # Get meter details
            details = api.get_meter_details(test_meter)
            if details['success']:
                print("Meter details retrieved successfully")
            
            # Try training a model (this might take a while)
            print(f"\n4. Training forecast model for meter {test_meter}...")
            training = api.train_forecasting_model(test_meter, 'import')
            
            if training['success']:
                print("Model trained successfully")
                
                # Test forecasting
                print("5. Generating forecast...")
                forecast = api.get_daily_forecast(test_meter)
                
                if forecast['success']:
                    print("Forecast generated successfully")
                else:
                    print(f"Forecast failed: {forecast.get('message', 'Unknown error')}")
            else:
                print(f"Training failed: {training.get('message', 'Unknown error')}")
    
    print("\n" + "=" * 40)
    print("Energy API ready for REST framework integration!")
    print("Uncomment Flask example code to run with Flask.")
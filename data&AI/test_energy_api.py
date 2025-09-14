"""
Comprehensive Test Script for Energy API System
==============================================

This script tests all functionality of the energy consumption API system including:
- Historical data retrieval
- Forecasting model training
- Prediction generation
- Error handling
- Performance metrics

Run this script to validate the entire system before deployment.
"""

import sys
import os
import time
import json
import traceback
from datetime import datetime
from typing import Dict, List, Any

# Import our API modules
try:
    from consumption_api import get_consumption_data, get_meter_list, load_data
    from consumption_forecast import ConsumptionForecaster
    from energy_api import EnergyAPI
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all API files are in the same directory as this test script.")
    sys.exit(1)

class EnergyAPITester:
    """
    Comprehensive test suite for the Energy API system
    """
    
    def __init__(self, data_file='cleaned_filtered_data.csv'):
        """Initialize the tester with data file"""
        self.data_file = data_file
        self.api = None
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': [],
            'start_time': None,
            'end_time': None
        }
        self.test_meter_id = None
        
        print("🧪 Energy API Test Suite")
        print("=" * 50)
        print(f"Data file: {data_file}")
        print(f"Test start time: {datetime.now()}")
        print("-" * 50)
    
    def log_test(self, test_name: str, success: bool, message: str = "", 
                details: Any = None, execution_time: float = 0):
        """Log test results"""
        self.test_results['total_tests'] += 1
        
        if success:
            self.test_results['passed_tests'] += 1
            status = "✅ PASS"
        else:
            self.test_results['failed_tests'] += 1
            status = "❌ FAIL"
        
        test_info = {
            'test_name': test_name,
            'status': status,
            'success': success,
            'message': message,
            'execution_time': execution_time,
            'details': details
        }
        
        self.test_results['test_details'].append(test_info)
        
        # Print test result
        print(f"{status} {test_name}")
        if message:
            print(f"    📝 {message}")
        if execution_time > 0:
            print(f"    ⏱️  {execution_time:.3f}s")
        if not success and details:
            print(f"    🔍 Error: {details}")
        print()
    
    def test_data_loading(self):
        """Test 1: Data file loading and basic validation"""
        test_name = "Data File Loading"
        start_time = time.time()
        
        try:
            # Test if file exists
            if not os.path.exists(self.data_file):
                self.log_test(test_name, False, f"Data file {self.data_file} not found")
                return False
            
            # Test data loading
            df = load_data(self.data_file)
            
            if df.empty:
                self.log_test(test_name, False, "Data file is empty")
                return False
            
            # Check required columns
            required_cols = ['meter_id', 'datetime', 'import_consumption', 'export_consumption']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                self.log_test(test_name, False, f"Missing columns: {missing_cols}")
                return False
            
            # Get test meter
            meters = df['meter_id'].unique()
            if len(meters) == 0:
                self.log_test(test_name, False, "No meters found in data")
                return False
            
            self.test_meter_id = meters[0]
            
            execution_time = time.time() - start_time
            self.log_test(test_name, True, 
                        f"Loaded {len(df)} records, {len(meters)} meters", 
                        {'rows': len(df), 'meters': len(meters)}, execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during data loading", str(e), execution_time)
            return False
    
    def test_meter_list_functionality(self):
        """Test 2: Meter list retrieval"""
        test_name = "Meter List Retrieval"
        start_time = time.time()
        
        try:
            meters = get_meter_list(self.data_file)
            
            if not meters:
                self.log_test(test_name, False, "No meters returned")
                return False
            
            if isinstance(meters, list) and len(meters) > 0:
                # Check meter structure
                meter_sample = meters[0]
                required_fields = ['meter_id', 'record_count']
                
                missing_fields = [field for field in required_fields if field not in meter_sample]
                if missing_fields:
                    self.log_test(test_name, False, f"Missing fields in meter data: {missing_fields}")
                    return False
                
                execution_time = time.time() - start_time
                self.log_test(test_name, True, 
                            f"Retrieved {len(meters)} meters successfully", 
                            {'meter_count': len(meters)}, execution_time)
                return True
            else:
                self.log_test(test_name, False, "Invalid meter list format")
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during meter list retrieval", str(e), execution_time)
            return False
    
    def test_historical_consumption_data(self):
        """Test 3: Historical consumption data retrieval"""
        test_name = "Historical Consumption Data"
        start_time = time.time()
        
        if not self.test_meter_id:
            self.log_test(test_name, False, "No test meter available")
            return False
        
        try:
            test_results = {}
            periods = ['24h', 'week', 'month', 'year']
            consumption_types = ['import', 'export', 'net']
            
            for period in periods:
                for consumption_type in consumption_types:
                    try:
                        result = get_consumption_data(
                            meter_id=self.test_meter_id,
                            period=period,
                            consumption_type=consumption_type
                        )
                        
                        # Validate result structure
                        if not isinstance(result, dict):
                            test_results[f"{period}_{consumption_type}"] = "Invalid result format"
                            continue
                        
                        if 'error' in result:
                            test_results[f"{period}_{consumption_type}"] = f"Error: {result['error']}"
                            continue
                        
                        if 'data' not in result:
                            test_results[f"{period}_{consumption_type}"] = "Missing data field"
                            continue
                        
                        # Check data structure
                        data = result['data']
                        if not isinstance(data, list):
                            test_results[f"{period}_{consumption_type}"] = "Data is not a list"
                            continue
                        
                        # Validate data points structure
                        if len(data) > 0:
                            sample_point = data[0]
                            if period == '24h':
                                required_field = 'hour'
                            elif period == 'week':
                                required_field = 'day'
                            elif period == 'month':
                                required_field = 'date'
                            else:  # year
                                required_field = 'month'
                            
                            if required_field not in sample_point or 'consumption' not in sample_point:
                                test_results[f"{period}_{consumption_type}"] = f"Missing required fields in data point"
                                continue
                        
                        test_results[f"{period}_{consumption_type}"] = f"✓ {len(data)} data points"
                        
                    except Exception as e:
                        test_results[f"{period}_{consumption_type}"] = f"Exception: {str(e)}"
            
            # Check if at least 50% of tests passed
            total_tests = len(periods) * len(consumption_types)
            successful_tests = sum(1 for result in test_results.values() if result.startswith('✓'))
            success_rate = successful_tests / total_tests
            
            execution_time = time.time() - start_time
            
            if success_rate >= 0.5:
                self.log_test(test_name, True, 
                            f"Success rate: {success_rate:.1%} ({successful_tests}/{total_tests})", 
                            test_results, execution_time)
                return True
            else:
                self.log_test(test_name, False, 
                            f"Low success rate: {success_rate:.1%} ({successful_tests}/{total_tests})", 
                            test_results, execution_time)
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during consumption data testing", str(e), execution_time)
            return False
    
    def test_forecasting_system(self):
        """Test 4: Forecasting system functionality"""
        test_name = "Forecasting System"
        start_time = time.time()
        
        if not self.test_meter_id:
            self.log_test(test_name, False, "No test meter available")
            return False
        
        try:
            forecaster = ConsumptionForecaster(self.data_file)
            
            # Test model training
            print("    📚 Training forecasting model...")
            train_start = time.time()
            training_results = forecaster.train_model(self.test_meter_id, 'import')
            train_time = time.time() - train_start
            
            print(f"    ⏱️  Training completed in {train_time:.2f}s")
            
            # Check training results
            if 'import_consumption' not in training_results:
                self.log_test(test_name, False, "Training failed - no results returned")
                return False
            
            import_result = training_results['import_consumption']
            if 'error' in import_result:
                self.log_test(test_name, False, f"Training error: {import_result['error']}")
                return False
            
            # Test prediction
            print("    🔮 Generating predictions...")
            pred_start = time.time()
            predictions = forecaster.predict(self.test_meter_id, 24, 'import')
            pred_time = time.time() - pred_start
            
            print(f"    ⏱️  Prediction completed in {pred_time:.2f}s")
            
            # Validate predictions
            if 'import_consumption' not in predictions:
                self.log_test(test_name, False, "Prediction failed - no results returned")
                return False
            
            import_pred = predictions['import_consumption']
            if 'error' in import_pred:
                self.log_test(test_name, False, f"Prediction error: {import_pred['error']}")
                return False
            
            if 'forecasts' not in import_pred:
                self.log_test(test_name, False, "Prediction missing forecasts data")
                return False
            
            forecasts = import_pred['forecasts']
            if len(forecasts) != 24:
                self.log_test(test_name, False, f"Expected 24 forecasts, got {len(forecasts)}")
                return False
            
            # Validate forecast structure
            sample_forecast = forecasts[0]
            required_fields = ['timestamp', 'hour_ahead', 'predicted_consumption']
            missing_fields = [field for field in required_fields if field not in sample_forecast]
            
            if missing_fields:
                self.log_test(test_name, False, f"Missing fields in forecast: {missing_fields}")
                return False
            
            execution_time = time.time() - start_time
            
            # Extract metrics
            metrics = {
                'training_mae': import_result.get('mae', 0),
                'training_rmse': import_result.get('rmse', 0),
                'training_mape': import_result.get('mape', 0),
                'forecast_points': len(forecasts),
                'total_predicted': import_pred['summary']['total_predicted']
            }
            
            self.log_test(test_name, True, 
                        f"Training and prediction successful. MAE: {metrics['training_mae']:.3f}", 
                        metrics, execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during forecasting test", str(e), execution_time)
            return False
    
    def test_energy_api_integration(self):
        """Test 5: Energy API integration layer"""
        test_name = "Energy API Integration"
        start_time = time.time()
        
        try:
            self.api = EnergyAPI(self.data_file)
            
            # Test health check
            health = self.api.health_check()
            if not health['success']:
                self.log_test(test_name, False, f"Health check failed: {health.get('message', 'Unknown error')}")
                return False
            
            # Test meter list
            meters_response = self.api.get_meters()
            if not meters_response['success']:
                self.log_test(test_name, False, f"Get meters failed: {meters_response.get('message', 'Unknown error')}")
                return False
            
            if not self.test_meter_id:
                self.log_test(test_name, False, "No test meter available")
                return False
            
            # Test meter details
            details = self.api.get_meter_details(self.test_meter_id)
            if not details['success']:
                self.log_test(test_name, False, f"Get meter details failed: {details.get('message', 'Unknown error')}")
                return False
            
            # Test historical consumption
            historical = self.api.get_historical_consumption(self.test_meter_id, '24h', 'net')
            if not historical['success']:
                self.log_test(test_name, False, f"Historical consumption failed: {historical.get('message', 'Unknown error')}")
                return False
            
            execution_time = time.time() - start_time
            
            api_stats = {
                'health_status': health['data']['status'],
                'available_meters': meters_response['data']['total_count'],
                'historical_data_points': len(historical['data']['data']) if 'data' in historical['data'] else 0
            }
            
            self.log_test(test_name, True, 
                        f"All API integration tests passed", 
                        api_stats, execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during API integration test", str(e), execution_time)
            return False
    
    def test_api_error_handling(self):
        """Test 6: API error handling"""
        test_name = "API Error Handling"
        start_time = time.time()
        
        if not self.api:
            self.log_test(test_name, False, "API not initialized")
            return False
        
        try:
            error_tests = {}
            
            # Test invalid meter ID
            invalid_meter_result = self.api.get_meter_details(999999999)
            error_tests['invalid_meter'] = not invalid_meter_result['success']
            
            # Test invalid period
            invalid_period_result = self.api.get_historical_consumption(self.test_meter_id, 'invalid_period')
            error_tests['invalid_period'] = 'error' in str(invalid_period_result)
            
            # Test forecasting without model
            non_existent_meter = 888888888
            forecast_result = self.api.get_daily_forecast(non_existent_meter)
            error_tests['forecast_no_model'] = not forecast_result['success']
            
            # Calculate success rate
            successful_error_tests = sum(error_tests.values())
            total_error_tests = len(error_tests)
            success_rate = successful_error_tests / total_error_tests
            
            execution_time = time.time() - start_time
            
            if success_rate >= 0.8:  # 80% of error cases should be handled properly
                self.log_test(test_name, True, 
                            f"Error handling success rate: {success_rate:.1%}", 
                            error_tests, execution_time)
                return True
            else:
                self.log_test(test_name, False, 
                            f"Poor error handling: {success_rate:.1%}", 
                            error_tests, execution_time)
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during error handling test", str(e), execution_time)
            return False
    
    def test_performance_benchmarks(self):
        """Test 7: Performance benchmarks"""
        test_name = "Performance Benchmarks"
        start_time = time.time()
        
        if not self.api or not self.test_meter_id:
            self.log_test(test_name, False, "API or test meter not available")
            return False
        
        try:
            performance_results = {}
            
            # Benchmark historical data retrieval
            hist_start = time.time()
            for _ in range(5):  # Run 5 times and average
                self.api.get_historical_consumption(self.test_meter_id, '24h', 'net')
            hist_time = (time.time() - hist_start) / 5
            performance_results['avg_historical_query'] = hist_time
            
            # Benchmark meter list retrieval
            meter_start = time.time()
            for _ in range(5):
                self.api.get_meters()
            meter_time = (time.time() - meter_start) / 5
            performance_results['avg_meter_list_query'] = meter_time
            
            execution_time = time.time() - start_time
            
            # Performance thresholds (in seconds)
            thresholds = {
                'avg_historical_query': 2.0,  # Should be under 2 seconds
                'avg_meter_list_query': 1.0   # Should be under 1 second
            }
            
            performance_ok = all(
                performance_results[key] <= thresholds[key] 
                for key in thresholds
            )
            
            if performance_ok:
                self.log_test(test_name, True, 
                            "All performance benchmarks passed", 
                            performance_results, execution_time)
                return True
            else:
                self.log_test(test_name, False, 
                            "Some performance benchmarks failed", 
                            performance_results, execution_time)
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test(test_name, False, "Exception during performance test", str(e), execution_time)
            return False
    
    def run_all_tests(self):
        """Run the complete test suite"""
        self.test_results['start_time'] = datetime.now()
        
        print("🚀 Starting comprehensive test suite...")
        print()
        
        # Run all tests in order
        tests = [
            self.test_data_loading,
            self.test_meter_list_functionality,
            self.test_historical_consumption_data,
            self.test_forecasting_system,
            self.test_energy_api_integration,
            self.test_api_error_handling,
            self.test_performance_benchmarks
        ]
        
        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                test_name = test_func.__name__.replace('test_', '').replace('_', ' ').title()
                self.log_test(test_name, False, "Unexpected exception", str(e))
        
        self.test_results['end_time'] = datetime.now()
        
        # Print final results
        self.print_final_results()
    
    def print_final_results(self):
        """Print comprehensive test results"""
        print("=" * 50)
        print("🏁 TEST SUITE COMPLETE")
        print("=" * 50)
        
        total = self.test_results['total_tests']
        passed = self.test_results['passed_tests']
        failed = self.test_results['failed_tests']
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"📊 SUMMARY:")
        print(f"   Total Tests: {total}")
        print(f"   Passed: {passed} ✅")
        print(f"   Failed: {failed} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        duration = self.test_results['end_time'] - self.test_results['start_time']
        print(f"   Duration: {duration.total_seconds():.2f} seconds")
        print()
        
        if failed > 0:
            print("❌ FAILED TESTS:")
            for test in self.test_results['test_details']:
                if not test['success']:
                    print(f"   • {test['test_name']}: {test['message']}")
            print()
        
        # Overall assessment
        if success_rate >= 85:
            print("🎉 EXCELLENT: System is ready for production!")
            assessment = "EXCELLENT"
        elif success_rate >= 70:
            print("✅ GOOD: System is mostly functional with minor issues")
            assessment = "GOOD"
        elif success_rate >= 50:
            print("⚠️  FAIR: System has significant issues that need attention")
            assessment = "FAIR"
        else:
            print("🚨 POOR: System has major issues and is not ready for use")
            assessment = "POOR"
        
        print()
        
        # Save results to file
        self.save_test_results(assessment)
    
    def save_test_results(self, assessment: str):
        """Save test results to a JSON file"""
        try:
            results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert datetime objects to strings for JSON serialization
            json_results = self.test_results.copy()
            json_results['start_time'] = self.test_results['start_time'].isoformat()
            json_results['end_time'] = self.test_results['end_time'].isoformat()
            json_results['assessment'] = assessment
            json_results['data_file'] = self.data_file
            
            with open(results_file, 'w') as f:
                json.dump(json_results, f, indent=2)
            
            print(f"📁 Test results saved to: {results_file}")
            
        except Exception as e:
            print(f"⚠️  Failed to save test results: {e}")

def main():
    """Main test execution function"""
    # Check if data file exists
    data_files = ['cleaned_filtered_data.csv', 'complete_processed_data.csv']
    data_file = None
    
    for file in data_files:
        if os.path.exists(file):
            data_file = file
            break
    
    if not data_file:
        print("❌ Error: No data file found!")
        print(f"Looking for: {data_files}")
        print("Please ensure your processed data file is in the current directory.")
        return
    
    # Create and run test suite
    tester = EnergyAPITester(data_file)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
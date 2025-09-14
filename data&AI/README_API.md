# Energy Consumption API

A comprehensive Python API for energy consumption data retrieval and forecasting, designed for integration with REST API frameworks and React frontends.

## Features

### 📊 Historical Consumption Data
- Retrieve consumption data for different time periods (24h, week, month, year)
- Support for individual meters or aggregated data
- Import, export, and net consumption analysis
- JSON format optimized for React components

### 🔮 Consumption Forecasting
- Machine learning-based forecasting using ensemble models
- Next day and next week predictions
- Individual meter model training
- Advanced feature engineering with time-based and lag features

### 🎯 REST API Ready
- Structured responses with success/error handling
- Metadata inclusion for frontend consumption
- Health checks and API information endpoints

## Files Structure

```
├── consumption_api.py          # Historical data retrieval functions
├── consumption_forecast.py     # ML forecasting system
├── energy_api.py              # Main API integration class
├── cleaned_filtered_data.csv   # Your processed data file
└── models/                    # Auto-created directory for trained models
```

## Quick Start

### 1. Install Required Dependencies

```bash
pip install pandas numpy scikit-learn joblib matplotlib seaborn
```

### 2. Basic Usage

```python
from energy_api import EnergyAPI

# Initialize the API
api = EnergyAPI('cleaned_filtered_data.csv')

# Check API health
health = api.health_check()
print(health)

# Get available meters
meters = api.get_meters()
print(f"Available meters: {meters['data']['total_count']}")

# Get historical consumption data
consumption = api.get_historical_consumption(
    meter_id=123456789,
    period='24h',
    consumption_type='net'
)

# Train forecasting model
training = api.train_forecasting_model(123456789, 'both')

# Generate forecast
forecast = api.get_daily_forecast(123456789)
```

## API Endpoints (Flask Example)

### Historical Data Endpoints

- `GET /api/health` - API health check
- `GET /api/info` - API information and available endpoints
- `GET /api/meters` - Get list of available meters
- `GET /api/meters/{meter_id}` - Get specific meter details
- `GET /api/consumption/historical` - Get historical consumption data
  - Parameters: `meter_id`, `period` (24h/week/month/year), `type` (import/export/net)

### Forecasting Endpoints

- `POST /api/forecast/train` - Train forecasting model for a meter
- `GET /api/forecast/consumption` - Get consumption forecast
- `GET /api/forecast/daily/{meter_id}` - Get 24-hour forecast
- `GET /api/forecast/weekly/{meter_id}` - Get 7-day forecast
- `GET /api/forecast/summary/{meter_id}` - Get forecast summary
- `POST /api/forecast/train-all` - Train models for all meters

## Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Success message",
  "error": "Error message (only if success: false)"
}
```

## React Frontend Integration

### Hourly Data Format
```typescript
const hourlyData: HourPoint[] = [
  { hour: 0, consumption: 0.25 },
  { hour: 1, consumption: 0.18 },
  // ... 24 hours total
];
```

### Weekly Data Format
```typescript
const weeklyData: DayPoint[] = [
  { day: 'Mon', consumption: 12.4 },
  { day: 'Tue', consumption: 10.8 },
  // ... 7 days total
];
```

### Monthly Data Format
```typescript
const monthlyData: DayPoint[] = [
  { date: '1', consumption: 12.4 },
  { date: '2', consumption: 11.8 },
  // ... days in month
];
```

### Yearly Data Format
```typescript
const yearlyData: MonthPoint[] = [
  { month: 'Jan', consumption: 18.2 },
  { month: 'Feb', consumption: 17.5 },
  // ... 12 months
];
```

## Flask Integration Example

```python
from flask import Flask, request, jsonify
from energy_api import EnergyAPI

app = Flask(__name__)
api = EnergyAPI()

@app.route('/api/meters', methods=['GET'])
def get_meters():
    return jsonify(api.get_meters())

@app.route('/api/consumption/historical', methods=['GET'])
def get_historical_consumption():
    meter_id = request.args.get('meter_id', type=int)
    period = request.args.get('period', '24h')
    consumption_type = request.args.get('type', 'net')
    
    return jsonify(api.get_historical_consumption(meter_id, period, consumption_type))

@app.route('/api/forecast/daily/<int:meter_id>', methods=['GET'])
def get_daily_forecast(meter_id):
    return jsonify(api.get_daily_forecast(meter_id))

if __name__ == '__main__':
    app.run(debug=True)
```

## FastAPI Integration Example

```python
from fastapi import FastAPI, HTTPException
from energy_api import EnergyAPI
from typing import Optional

app = FastAPI()
api = EnergyAPI()

@app.get("/api/meters")
def get_meters():
    result = api.get_meters()
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['message'])
    return result

@app.get("/api/consumption/historical")
def get_historical_consumption(
    meter_id: Optional[int] = None,
    period: str = '24h',
    type: str = 'net'
):
    result = api.get_historical_consumption(meter_id, period, type)
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['message'])
    return result

@app.get("/api/forecast/daily/{meter_id}")
def get_daily_forecast(meter_id: int):
    result = api.get_daily_forecast(meter_id)
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['message'])
    return result
```

## Forecasting Features

The forecasting system includes advanced features:

### Feature Engineering
- **Time-based features**: Hour, day of week, month, quarter
- **Cyclical features**: Sin/cos transformations for seasonal patterns
- **Lag features**: Previous 1h, 2h, 3h, 6h, 12h, 24h consumption
- **Rolling statistics**: Moving averages and standard deviations
- **Weather estimates**: Seasonal temperature patterns (mock data)
- **Business day indicators**: Weekend vs weekday patterns

### Machine Learning Models
- **Random Forest**: Handles non-linear patterns and feature interactions
- **Gradient Boosting**: Sequential learning for complex patterns
- **Ensemble approach**: Averages predictions from multiple models
- **Time series validation**: Proper train/test splitting for time series

### Model Performance Metrics
- **MAE** (Mean Absolute Error): Average prediction error
- **RMSE** (Root Mean Square Error): Penalizes larger errors
- **MAPE** (Mean Absolute Percentage Error): Percentage-based error

## Data Requirements

Your `cleaned_filtered_data.csv` should contain:
- `meter_id`: Unique identifier for each meter
- `datetime`: Timestamp in datetime format
- `import_consumption`: Energy import consumption values
- `export_consumption`: Energy export consumption values

## Model Training

### Train Single Meter
```python
api = EnergyAPI()
result = api.train_forecasting_model(meter_id=123456789, target_type='both')
```

### Train All Meters
```python
results = api.train_all_meters(target_type='both')
```

Models are automatically saved in the `models/` directory and can be reused for predictions.

## Error Handling

The API includes comprehensive error handling:
- Data validation
- Missing meter checks
- Model training failures
- Prediction errors
- File I/O issues

All errors are returned in a structured format with appropriate error messages.

## Performance Considerations

- Models are cached in memory after first load
- Trained models are persisted to disk
- Time series data is efficiently processed with pandas
- Feature engineering is optimized for batch processing

## Future Enhancements

- Real weather data integration
- More sophisticated ML models (LSTM, Prophet)
- Real-time streaming data support
- Model performance monitoring
- Automatic model retraining
- Energy price optimization
- Anomaly detection

## Support

For issues or questions, refer to the individual module documentation:
- `consumption_api.py` - Historical data functions
- `consumption_forecast.py` - ML forecasting system
- `energy_api.py` - Main API integration

The system is designed to be modular and extensible for your specific needs.
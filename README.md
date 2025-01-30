# Vehicle Health Monitoring System

A real-time vehicle diagnostic system that monitors vehicle health, predicts maintenance needs using kNN algorithm, and provides alerts and garage recommendations when necessary.

## Features

- Real-time vehicle health monitoring dashboard
- Interactive condition simulation slider
- Predictive maintenance using kNN algorithm
- Real-time metrics visualization
- Automatic alerts for critical conditions
- Nearby garage recommendations
- Beautiful and responsive UI

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vehicle_health_monitoring
```

2. Create and activate a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the application with a single command:
```bash
python run.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Data Files

The system uses two main data files:
- `engine_data.csv`: Contains historical engine performance data
- `predictive_maintenance.csv`: Contains maintenance records and outcomes

## Usage

1. The main dashboard shows real-time vehicle metrics
2. Use the condition slider to simulate different vehicle states
3. Monitor the health chart for trends
4. Check alerts for any warnings or critical conditions
5. View nearby garage recommendations when maintenance is needed

## Technical Details

- Backend: Flask (Python)
- Frontend: HTML5, CSS3, JavaScript
- Machine Learning: scikit-learn (kNN algorithm)
- Data Processing: pandas, numpy
- Visualization: Chart.js
- Styling: Bootstrap 5

## Contributing

Feel free to submit issues and enhancement requests!
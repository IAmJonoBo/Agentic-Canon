# ML-Powered Insights Framework

Leverage machine learning to gain insights from your development metrics and predict issues before they occur.

## Overview

This framework provides ML-powered capabilities for:

1. **Anomaly Detection** - Detect unusual patterns in metrics
2. **Predictive Analysis** - Predict failures before they happen
3. **Test Flakiness Detection** - Identify and quarantine flaky tests
4. **Code Quality Prediction** - Predict code quality from diffs
5. **Performance Regression Detection** - Catch performance degradation early

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Data Collection                        │
│  (Metrics, Logs, Test Results, Code Changes)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Feature Engineering                       │
│  (Extract relevant features from raw data)              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   ML Models                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Anomaly     │  │  Prediction  │  │  Flakiness   │ │
│  │  Detection   │  │  Models      │  │  Detection   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Insights & Actions                        │
│  - Alerts                                               │
│  - Auto-remediation                                     │
│  - Recommendations                                      │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. Anomaly Detection

Detect unusual patterns in time-series metrics using statistical and ML methods.

#### Example: Metric Anomaly Detection

```python
# ml_insights/anomaly_detection.py
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Tuple

class MetricAnomalyDetector:
    """
    Detect anomalies in metric time series using Isolation Forest.
    """
    
    def __init__(self, contamination: float = 0.1):
        """
        Args:
            contamination: Expected proportion of anomalies (0.0 to 0.5)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.is_fitted = False
    
    def fit(self, metrics: List[float]):
        """
        Train the anomaly detector on historical metrics.
        
        Args:
            metrics: List of metric values
        """
        X = np.array(metrics).reshape(-1, 1)
        self.model.fit(X)
        self.is_fitted = True
    
    def detect(self, value: float) -> Tuple[bool, float]:
        """
        Detect if a value is anomalous.
        
        Args:
            value: Metric value to check
            
        Returns:
            Tuple of (is_anomaly, anomaly_score)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before detection")
        
        X = np.array([[value]])
        prediction = self.model.predict(X)[0]
        score = self.model.score_samples(X)[0]
        
        is_anomaly = prediction == -1
        return is_anomaly, abs(score)

# Example usage
detector = MetricAnomalyDetector()

# Train on historical data
historical_latencies = [45, 50, 48, 52, 49, 51, 47, 53]
detector.fit(historical_latencies)

# Check new values
is_anomaly, score = detector.detect(150)  # Spike in latency
if is_anomaly:
    print(f"⚠️  Anomaly detected! Score: {score:.2f}")
```

#### Integration with Prometheus

```python
# ml_insights/prometheus_anomaly.py
from prometheus_client import Gauge
from prometheus_api_client import PrometheusConnect

class PrometheusAnomalyMonitor:
    """Monitor Prometheus metrics for anomalies."""
    
    def __init__(self, prometheus_url: str):
        self.prom = PrometheusConnect(url=prometheus_url)
        self.detectors = {}
        
        # Prometheus metric for anomalies
        self.anomaly_gauge = Gauge(
            'ml_anomaly_score',
            'ML anomaly detection score',
            ['metric_name']
        )
    
    def monitor_metric(
        self,
        metric_name: str,
        query: str,
        lookback_hours: int = 24
    ):
        """
        Monitor a Prometheus metric for anomalies.
        
        Args:
            metric_name: Name of the metric
            query: PromQL query
            lookback_hours: Hours of historical data for training
        """
        # Fetch historical data
        historical_data = self.prom.custom_query_range(
            query=query,
            start_time=f"-{lookback_hours}h",
            end_time="now",
            step="5m"
        )
        
        values = [float(point[1]) for point in historical_data[0]['values']]
        
        # Train detector
        if metric_name not in self.detectors:
            self.detectors[metric_name] = MetricAnomalyDetector()
        
        self.detectors[metric_name].fit(values)
        
        # Check latest value
        latest_value = float(historical_data[0]['values'][-1][1])
        is_anomaly, score = self.detectors[metric_name].detect(latest_value)
        
        # Update Prometheus
        self.anomaly_gauge.labels(metric_name=metric_name).set(score)
        
        if is_anomaly:
            print(f"🚨 Anomaly in {metric_name}: {latest_value} (score: {score:.2f})")
            return True
        
        return False
```

### 2. Predictive Failure Analysis

Predict deployment failures before they happen.

```python
# ml_insights/failure_prediction.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class DeploymentFailurePredictor:
    """
    Predict deployment failures based on historical data.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        self.feature_names = [
            'change_size',          # Lines of code changed
            'num_files_changed',    # Number of files changed
            'test_coverage',        # Test coverage percentage
            'complexity_increase',  # Cyclomatic complexity delta
            'time_since_last_deploy', # Time in hours
            'num_contributors',     # Number of people involved
            'pr_review_time',       # Review time in hours
            'num_dependencies_changed', # Dependency changes
        ]
    
    def prepare_features(self, deployment_data: dict) -> pd.DataFrame:
        """Extract features from deployment data."""
        features = {
            'change_size': deployment_data.get('lines_added', 0) + 
                          deployment_data.get('lines_removed', 0),
            'num_files_changed': deployment_data.get('files_changed', 0),
            'test_coverage': deployment_data.get('test_coverage', 0),
            'complexity_increase': deployment_data.get('complexity_delta', 0),
            'time_since_last_deploy': deployment_data.get('hours_since_last', 0),
            'num_contributors': deployment_data.get('contributors', 1),
            'pr_review_time': deployment_data.get('review_hours', 0),
            'num_dependencies_changed': deployment_data.get('dep_changes', 0),
        }
        return pd.DataFrame([features])
    
    def train(self, historical_deployments: List[dict]):
        """
        Train model on historical deployment data.
        
        Args:
            historical_deployments: List of dicts with deployment info and outcome
        """
        X = []
        y = []
        
        for deployment in historical_deployments:
            features = self.prepare_features(deployment)
            X.append(features.values[0])
            y.append(1 if deployment.get('failed', False) else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        self.model.fit(X, y)
        
        # Print feature importances
        importances = self.model.feature_importances_
        for name, importance in zip(self.feature_names, importances):
            print(f"  {name}: {importance:.3f}")
    
    def predict_failure_risk(self, deployment_data: dict) -> Tuple[float, str]:
        """
        Predict failure risk for a deployment.
        
        Returns:
            Tuple of (risk_score, risk_level)
        """
        features = self.prepare_features(deployment_data)
        
        # Get probability of failure
        proba = self.model.predict_proba(features)[0][1]
        
        # Categorize risk
        if proba < 0.2:
            risk_level = "LOW"
        elif proba < 0.5:
            risk_level = "MEDIUM"
        elif proba < 0.8:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        return proba, risk_level

# Example usage
predictor = DeploymentFailurePredictor()

# Train on historical data
historical_deployments = [
    {
        'lines_added': 50, 'lines_removed': 20,
        'files_changed': 5, 'test_coverage': 85,
        'failed': False
    },
    {
        'lines_added': 500, 'lines_removed': 200,
        'files_changed': 25, 'test_coverage': 60,
        'failed': True
    },
    # ... more historical data
]

predictor.train(historical_deployments)

# Predict for new deployment
new_deployment = {
    'lines_added': 200,
    'lines_removed': 50,
    'files_changed': 10,
    'test_coverage': 75,
}

risk_score, risk_level = predictor.predict_failure_risk(new_deployment)
print(f"Deployment risk: {risk_level} ({risk_score*100:.1f}%)")
```

### 3. Test Flakiness Detection

Identify and automatically quarantine flaky tests.

```python
# ml_insights/flaky_test_detection.py
from collections import defaultdict
from typing import List, Dict
import statistics

class FlakyTestDetector:
    """
    Detect flaky tests based on historical test results.
    """
    
    def __init__(self, window_size: int = 100):
        """
        Args:
            window_size: Number of recent runs to consider
        """
        self.window_size = window_size
        self.test_history = defaultdict(list)  # test_name -> [pass/fail]
    
    def record_result(self, test_name: str, passed: bool):
        """Record a test result."""
        self.test_history[test_name].append(passed)
        
        # Keep only recent results
        if len(self.test_history[test_name]) > self.window_size:
            self.test_history[test_name].pop(0)
    
    def calculate_flakiness_score(self, test_name: str) -> float:
        """
        Calculate flakiness score for a test.
        
        Score is based on:
        - Frequency of failures
        - Pattern of failures (alternating vs consecutive)
        - Recent trend
        
        Returns:
            Score from 0 (stable) to 1 (very flaky)
        """
        if test_name not in self.test_history:
            return 0.0
        
        results = self.test_history[test_name]
        if len(results) < 10:  # Not enough data
            return 0.0
        
        # Calculate metrics
        failure_rate = 1 - sum(results) / len(results)
        
        # Count transitions (pass->fail or fail->pass)
        transitions = sum(
            1 for i in range(len(results)-1)
            if results[i] != results[i+1]
        )
        transition_rate = transitions / (len(results) - 1)
        
        # Recent trend (last 10 runs)
        recent_failure_rate = 1 - sum(results[-10:]) / 10
        
        # Flakiness score
        # Perfect tests: failure_rate=0, transition_rate=0
        # Flaky tests: 0<failure_rate<1, high transition_rate
        # Consistently failing: failure_rate=1, transition_rate=0
        
        if failure_rate == 0 or failure_rate == 1:
            # Consistently passing or failing - not flaky
            return 0.0
        
        # Weight different factors
        score = (
            0.4 * failure_rate +           # Some failures
            0.4 * transition_rate +        # Alternating results
            0.2 * recent_failure_rate      # Recent behavior
        )
        
        return min(score, 1.0)
    
    def get_flaky_tests(self, threshold: float = 0.5) -> List[Dict]:
        """
        Get list of flaky tests above threshold.
        
        Returns:
            List of dicts with test info and scores
        """
        flaky_tests = []
        
        for test_name in self.test_history:
            score = self.calculate_flakiness_score(test_name)
            
            if score >= threshold:
                flaky_tests.append({
                    'name': test_name,
                    'flakiness_score': score,
                    'total_runs': len(self.test_history[test_name]),
                    'pass_rate': sum(self.test_history[test_name]) / 
                                len(self.test_history[test_name])
                })
        
        # Sort by flakiness score
        flaky_tests.sort(key=lambda x: x['flakiness_score'], reverse=True)
        
        return flaky_tests
    
    def quarantine_test(self, test_name: str) -> str:
        """
        Generate pytest mark to quarantine flaky test.
        
        Returns:
            Pytest marker string
        """
        return f'@pytest.mark.skip(reason="Flaky test - quarantined by ML system")'

# Integration with pytest
# conftest.py
def pytest_collection_modifyitems(config, items):
    """Automatically skip flaky tests."""
    detector = FlakyTestDetector()
    
    # Load historical results
    # ... load from database or file
    
    flaky_tests = detector.get_flaky_tests(threshold=0.7)
    flaky_test_names = {test['name'] for test in flaky_tests}
    
    for item in items:
        if item.nodeid in flaky_test_names:
            item.add_marker(
                pytest.mark.skip(reason="Flaky test - auto-quarantined")
            )
```

### 4. Code Quality Prediction

Predict code quality from pull request diffs.

```python
# ml_insights/code_quality_prediction.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
import re

class CodeQualityPredictor:
    """
    Predict code quality issues from PR diffs.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = GradientBoostingClassifier()
    
    def extract_features(self, diff: str) -> dict:
        """Extract features from code diff."""
        return {
            'lines_added': diff.count('\n+'),
            'lines_removed': diff.count('\n-'),
            'has_todos': bool(re.search(r'TODO|FIXME|HACK', diff)),
            'has_long_lines': bool(re.search(r'.{120,}', diff)),
            'num_functions': len(re.findall(r'def |function ', diff)),
            'num_classes': len(re.findall(r'class ', diff)),
            'has_error_handling': bool(re.search(r'try:|catch|except', diff)),
            'has_tests': bool(re.search(r'test_|def test', diff)),
        }
    
    def predict_quality_issues(self, diff: str) -> List[str]:
        """
        Predict potential quality issues in code.
        
        Returns:
            List of predicted issues
        """
        features = self.extract_features(diff)
        issues = []
        
        if features['lines_added'] > 500:
            issues.append("Large changeset - consider breaking into smaller PRs")
        
        if features['has_todos']:
            issues.append("Contains TODO/FIXME comments")
        
        if features['has_long_lines']:
            issues.append("Contains lines longer than 120 characters")
        
        if features['num_functions'] > 0 and not features['has_tests']:
            issues.append("New functions added without tests")
        
        if not features['has_error_handling'] and features['lines_added'] > 50:
            issues.append("No error handling detected in significant changes")
        
        return issues
```

## Deployment

### Docker Container

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ml_insights/ ./ml_insights/

CMD ["python", "-m", "ml_insights.server"]
```

### Kubernetes Deployment

```yaml
# k8s/ml-insights-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-insights
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-insights
  template:
    metadata:
      labels:
        app: ml-insights
    spec:
      containers:
      - name: ml-insights
        image: your-registry/ml-insights:latest
        ports:
        - containerPort: 8080
        env:
        - name: PROMETHEUS_URL
          value: "http://prometheus:9090"
        - name: MODEL_PATH
          value: "/models"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

## Configuration

```yaml
# config/ml-insights.yaml
anomaly_detection:
  enabled: true
  contamination: 0.1
  metrics:
    - name: api_latency
      query: "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
      threshold: 0.8
    
    - name: error_rate
      query: "rate(http_requests_total{status=~\"5..\"}[5m])"
      threshold: 0.9

failure_prediction:
  enabled: true
  risk_threshold: 0.7  # Block deployments above this risk
  retrain_interval_hours: 24

flaky_tests:
  enabled: true
  window_size: 100
  flakiness_threshold: 0.7
  auto_quarantine: true

code_quality:
  enabled: true
  min_score: 0.7
```

## Monitoring

Track ML model performance:

```python
from prometheus_client import Counter, Histogram

ml_predictions_total = Counter(
    'ml_predictions_total',
    'Total ML predictions made',
    ['model_name', 'prediction']
)

ml_prediction_accuracy = Gauge(
    'ml_prediction_accuracy',
    'ML model prediction accuracy',
    ['model_name']
)

ml_inference_duration = Histogram(
    'ml_inference_duration_seconds',
    'ML inference duration',
    ['model_name']
)
```

## Future Enhancements

1. **AutoML** - Automatically select best models
2. **Explainable AI** - SHAP values for predictions
3. **Continuous Learning** - Models update with new data
4. **Multi-model Ensemble** - Combine multiple models
5. **Transfer Learning** - Use pre-trained models

## Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [MLOps Best Practices](https://ml-ops.org/)
- [Model Monitoring](https://www.evidentlyai.com/)
- [Feature Engineering](https://www.featuretools.com/)

## License

MIT License

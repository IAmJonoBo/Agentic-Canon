# Architecture Fitness Functions

Automated fitness functions to enforce architectural characteristics and quality attributes.

## Overview

Fitness functions are automated checks that verify whether a system exhibits desired architectural characteristics. They run in CI/CD pipelines to catch violations early.

## Categories

### 1. Performance Fitness Functions

Monitor and enforce performance boundaries.

#### Latency Thresholds

```python
# fitness_functions/performance/latency_check.py
import requests
import statistics

def check_api_latency(endpoint: str, threshold_ms: int = 200) -> bool:
    """
    Verify API response time is below threshold.
    
    Args:
        endpoint: API endpoint to test
        threshold_ms: Maximum acceptable latency in milliseconds
        
    Returns:
        True if latency is acceptable, False otherwise
    """
    latencies = []
    
    # Make 10 requests
    for _ in range(10):
        response = requests.get(endpoint)
        latencies.append(response.elapsed.total_seconds() * 1000)
    
    p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
    
    if p95_latency > threshold_ms:
        print(f"❌ FAIL: P95 latency {p95_latency:.2f}ms exceeds threshold {threshold_ms}ms")
        return False
    
    print(f"✅ PASS: P95 latency {p95_latency:.2f}ms is within threshold")
    return True


def check_database_query_time(query: str, threshold_ms: int = 100) -> bool:
    """Check database query execution time."""
    import time
    from db import execute_query
    
    start = time.time()
    execute_query(query)
    duration_ms = (time.time() - start) * 1000
    
    if duration_ms > threshold_ms:
        print(f"❌ FAIL: Query took {duration_ms:.2f}ms (threshold: {threshold_ms}ms)")
        return False
    
    print(f"✅ PASS: Query completed in {duration_ms:.2f}ms")
    return True
```

#### Throughput

```python
# fitness_functions/performance/throughput_check.py
import concurrent.futures
import requests

def check_minimum_throughput(endpoint: str, min_rps: int = 100) -> bool:
    """
    Verify system can handle minimum requests per second.
    
    Args:
        endpoint: API endpoint to test
        min_rps: Minimum required requests per second
    """
    duration_seconds = 10
    
    def make_request():
        return requests.get(endpoint)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for _ in range(min_rps * duration_seconds):
            futures.append(executor.submit(make_request))
        
        successful = sum(1 for f in futures if f.result().status_code == 200)
    
    actual_rps = successful / duration_seconds
    
    if actual_rps < min_rps:
        print(f"❌ FAIL: Throughput {actual_rps:.1f} RPS below minimum {min_rps} RPS")
        return False
    
    print(f"✅ PASS: Throughput {actual_rps:.1f} RPS meets requirement")
    return True
```

### 2. Architecture Fitness Functions

Enforce architectural rules and patterns.

#### Dependency Rules

```python
# fitness_functions/architecture/dependency_check.py
import ast
import os
from pathlib import Path

def check_no_cyclic_dependencies(src_dir: str) -> bool:
    """
    Detect cyclic dependencies between modules.
    
    Returns:
        True if no cycles found, False otherwise
    """
    from collections import defaultdict
    
    dependencies = defaultdict(set)
    
    # Build dependency graph
    for py_file in Path(src_dir).rglob("*.py"):
        module = str(py_file.relative_to(src_dir)).replace("/", ".")[:-3]
        
        with open(py_file) as f:
            tree = ast.parse(f.read())
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(src_dir.split("/")[-1]):
                        dependencies[module].add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith(src_dir.split("/")[-1]):
                    dependencies[module].add(node.module)
    
    # Check for cycles using DFS
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in dependencies.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                print(f"❌ FAIL: Cyclic dependency detected: {node} -> {neighbor}")
                return True
        
        rec_stack.remove(node)
        return False
    
    visited = set()
    for node in dependencies:
        if node not in visited:
            if has_cycle(node, visited, set()):
                return False
    
    print("✅ PASS: No cyclic dependencies found")
    return True


def check_layer_dependencies(src_dir: str) -> bool:
    """
    Verify that layers only depend on lower layers.
    
    Architecture layers (top to bottom):
    - presentation (API/UI)
    - application (use cases)
    - domain (business logic)
    - infrastructure (database, external services)
    """
    layer_order = ["presentation", "application", "domain", "infrastructure"]
    violations = []
    
    for py_file in Path(src_dir).rglob("*.py"):
        file_layer = None
        for layer in layer_order:
            if layer in str(py_file):
                file_layer = layer
                break
        
        if not file_layer:
            continue
        
        with open(py_file) as f:
            content = f.read()
        
        file_layer_idx = layer_order.index(file_layer)
        
        # Check imports
        for idx, layer in enumerate(layer_order):
            if idx < file_layer_idx and layer in content:
                violations.append(
                    f"{py_file}: {file_layer} layer depends on {layer} layer"
                )
    
    if violations:
        print("❌ FAIL: Layer dependency violations:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print("✅ PASS: Layer dependencies are correct")
    return True
```

#### Coupling Metrics

```python
# fitness_functions/architecture/coupling_check.py
import radon.complexity as radon_cc
from pathlib import Path

def check_coupling_metrics(src_dir: str, max_coupling: int = 5) -> bool:
    """
    Check afferent and efferent coupling for modules.
    
    Args:
        src_dir: Source directory to analyze
        max_coupling: Maximum acceptable coupling value
    """
    violations = []
    
    for py_file in Path(src_dir).rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
        
        # Count imports (efferent coupling)
        import_count = content.count("import ") + content.count("from ")
        
        if import_count > max_coupling:
            violations.append(
                f"{py_file}: {import_count} imports (max: {max_coupling})"
            )
    
    if violations:
        print(f"❌ FAIL: High coupling detected:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print(f"✅ PASS: All modules have coupling <= {max_coupling}")
    return True
```

### 3. Security Fitness Functions

Enforce security standards.

```python
# fitness_functions/security/security_check.py
import re
from pathlib import Path

def check_no_hardcoded_secrets(src_dir: str) -> bool:
    """
    Scan for hardcoded secrets in source code.
    """
    patterns = [
        (r'password\s*=\s*["\'].*["\']', "hardcoded password"),
        (r'api[_-]?key\s*=\s*["\'].*["\']', "hardcoded API key"),
        (r'secret\s*=\s*["\'].*["\']', "hardcoded secret"),
        (r'token\s*=\s*["\'].*["\']', "hardcoded token"),
    ]
    
    violations = []
    
    for py_file in Path(src_dir).rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
        
        for pattern, description in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append(f"{py_file}: {description}")
    
    if violations:
        print("❌ FAIL: Potential secrets found:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print("✅ PASS: No hardcoded secrets detected")
    return True


def check_attack_surface(endpoints: list, max_public_endpoints: int = 10) -> bool:
    """
    Monitor API attack surface by counting public endpoints.
    """
    public_endpoints = [e for e in endpoints if not e.get("requires_auth")]
    
    if len(public_endpoints) > max_public_endpoints:
        print(f"❌ FAIL: {len(public_endpoints)} public endpoints (max: {max_public_endpoints})")
        return False
    
    print(f"✅ PASS: {len(public_endpoints)} public endpoints within limit")
    return True
```

### 4. Quality Fitness Functions

Maintain code quality standards.

```python
# fitness_functions/quality/quality_check.py
import radon.complexity as radon_cc
import radon.raw as radon_raw
from pathlib import Path

def check_cyclomatic_complexity(src_dir: str, max_complexity: int = 10) -> bool:
    """
    Check that functions don't exceed complexity threshold.
    """
    violations = []
    
    for py_file in Path(src_dir).rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
        
        complexity = radon_cc.cc_visit(content)
        
        for item in complexity:
            if item.complexity > max_complexity:
                violations.append(
                    f"{py_file}:{item.lineno} {item.name}: "
                    f"complexity {item.complexity} (max: {max_complexity})"
                )
    
    if violations:
        print("❌ FAIL: High complexity detected:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print(f"✅ PASS: All functions have complexity <= {max_complexity}")
    return True


def check_code_duplication(src_dir: str, max_duplication: float = 5.0) -> bool:
    """
    Check code duplication percentage.
    """
    # This would integrate with tools like PMD CPD or similar
    # For now, simplified check
    duplication_percent = 3.2  # Would come from actual analysis
    
    if duplication_percent > max_duplication:
        print(f"❌ FAIL: Code duplication {duplication_percent}% exceeds {max_duplication}%")
        return False
    
    print(f"✅ PASS: Code duplication {duplication_percent}% is acceptable")
    return True


def check_technical_debt(src_dir: str, max_debt_minutes: int = 1000) -> bool:
    """
    Check total technical debt doesn't exceed threshold.
    """
    total_debt = 0
    
    for py_file in Path(src_dir).rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
        
        # Count TODO, FIXME, HACK comments
        todos = content.count("# TODO") + content.count("# FIXME") + content.count("# HACK")
        total_debt += todos * 30  # Estimate 30 minutes per TODO
    
    if total_debt > max_debt_minutes:
        print(f"❌ FAIL: Technical debt {total_debt} minutes exceeds {max_debt_minutes}")
        return False
    
    print(f"✅ PASS: Technical debt {total_debt} minutes is manageable")
    return True
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/fitness-functions.yml
name: Fitness Functions

on: [push, pull_request]

jobs:
  fitness-checks:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r fitness-requirements.txt
      
      - name: Run Performance Checks
        run: |
          python -m fitness_functions.performance.latency_check
          python -m fitness_functions.performance.throughput_check
      
      - name: Run Architecture Checks
        run: |
          python -m fitness_functions.architecture.dependency_check
          python -m fitness_functions.architecture.coupling_check
      
      - name: Run Security Checks
        run: |
          python -m fitness_functions.security.security_check
      
      - name: Run Quality Checks
        run: |
          python -m fitness_functions.quality.quality_check
      
      - name: Fail on violations
        if: failure()
        run: |
          echo "❌ Fitness function checks failed"
          exit 1
```

### Configuration

```yaml
# fitness-config.yaml
performance:
  api_latency_ms: 200
  db_query_ms: 100
  min_throughput_rps: 100

architecture:
  max_coupling: 5
  allow_cyclic_dependencies: false
  enforce_layers: true

security:
  scan_secrets: true
  max_public_endpoints: 10
  require_auth_by_default: true

quality:
  max_cyclomatic_complexity: 10
  max_code_duplication_percent: 5.0
  max_technical_debt_minutes: 1000
```

## Usage

### Running Locally

```bash
# Run all fitness functions
python -m fitness_functions.run_all

# Run specific category
python -m fitness_functions.performance

# Run with custom config
python -m fitness_functions.run_all --config custom-config.yaml
```

### Running in CI/CD

```bash
# As part of test suite
pytest fitness_functions/

# Standalone
./scripts/run-fitness-checks.sh
```

## Monitoring

Track fitness function results over time:

```python
# fitness_functions/metrics.py
from prometheus_client import Counter, Histogram

fitness_check_total = Counter(
    'fitness_check_total',
    'Total fitness function checks',
    ['category', 'check_name', 'result']
)

fitness_check_duration = Histogram(
    'fitness_check_duration_seconds',
    'Fitness function check duration',
    ['category', 'check_name']
)
```

## Best Practices

1. **Run Early and Often**
   - Pre-commit hooks
   - CI on every push
   - Scheduled runs

2. **Keep Checks Fast**
   - Target < 5 minutes total
   - Parallelize where possible
   - Use caching

3. **Make Failures Actionable**
   - Clear error messages
   - Link to remediation docs
   - Suggest fixes

4. **Version Your Thresholds**
   - Track in version control
   - Document changes
   - Gradual improvement

5. **Monitor Trends**
   - Track metrics over time
   - Set improvement goals
   - Celebrate wins

## Resources

- [Building Evolutionary Architectures](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/)
- [Fitness Functions in Practice](https://www.thoughtworks.com/insights/blog/fitness-function-driven-development)
- [ArchUnit](https://www.archunit.org/) - Java architecture testing
- [Radon](https://radon.readthedocs.io/) - Python complexity metrics

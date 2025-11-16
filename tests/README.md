# Analytics Service Test Suite

Comprehensive test suite for the Analytics Service (S5) using pytest and FastAPI TestClient.

## Test Coverage

### Test Suites

| Suite ID | Name | Tests | File |
|----------|------|-------|------|
| S5.TS1 | Health Endpoint Tests | 1 | test_health.py |
| S5.TS2 | Patient Analytics Tests | 3 | test_patient_analytics.py |
| S5.TS3 | Visit Analytics Tests | 2 | test_visit_analytics.py |
| S5.TS4 | Performance Metrics Tests | 4 | test_performance.py |
| S5.TS5 | Dashboard Statistics Tests | 4 | test_dashboard.py |
| S5.TS6 | Database Connection Tests | 3 | test_database.py |
| **Total** | **6 Test Suites** | **17 Tests** | |

## Installation

```bash
# Install production dependencies
pip install -r requirements.txt

# Install test dependencies
pip install -r requirements-test.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_health.py

# Run with verbose output
pytest -v

# Generate HTML report
pytest --html=reports/test-report.html
```

## Test Reports

Reports are generated in the `reports/` folder:
- **test-report-natural-language.txt** - Human-readable report
- **test-report-natural-language.md** - Markdown report
- **htmlcov/index.html** - Coverage report

## What's Tested

### ✓ Health Checks
- Service availability

### ✓ Patient Analytics
- Patient count by status
- Critical patient count
- Data accuracy

### ✓ Visit Analytics
- Visit count by status
- Data consistency

### ✓ Performance Metrics
- Total patients
- Total visits
- Today's visits
- Critical patients

### ✓ Dashboard Statistics
- Overview data
- Patients by status
- Visits by status
- Error handling

### ✓ Database
- MySQL connection
- Query execution
- Error handling

## Technology

- **Framework:** FastAPI
- **Testing:** pytest + TestClient
- **Coverage:** pytest-cov
- **Python:** 3.11+

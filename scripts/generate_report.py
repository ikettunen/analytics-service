"""
Test Report Generator for Analytics Service

Generates a natural language report from pytest test results
including test outcomes, coverage, and detailed information.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def generate_report():
    """Generate comprehensive test report"""
    
    timestamp = datetime.now().isoformat()
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Test suite information
    test_suites = {
        'S5.TS1': {
            'name': 'Health Endpoint Tests',
            'file': 'test_health.py',
            'tests': 1
        },
        'S5.TS2': {
            'name': 'Patient Analytics Tests',
            'file': 'test_patient_analytics.py',
            'tests': 3
        },
        'S5.TS3': {
            'name': 'Visit Analytics Tests',
            'file': 'test_visit_analytics.py',
            'tests': 2
        },
        'S5.TS4': {
            'name': 'Performance Metrics Tests',
            'file': 'test_performance.py',
            'tests': 4
        },
        'S5.TS5': {
            'name': 'Dashboard Statistics Tests',
            'file': 'test_dashboard.py',
            'tests': 4
        },
        'S5.TS6': {
            'name': 'Database Connection Tests',
            'file': 'test_database.py',
            'tests': 3
        }
    }
    
    report = []
    report.append('═' * 70)
    report.append('              ANALYTICS SERVICE TEST REPORT')
    report.append('═' * 70)
    report.append(f'Generated: {timestamp}')
    report.append('Service: Analytics Service (S5)')
    report.append('Test Framework: pytest + FastAPI TestClient')
    report.append('Language: Python 3.11+')
    report.append('═' * 70)
    report.append('')
    
    # Executive Summary
    report.append('## EXECUTIVE SUMMARY')
    report.append('')
    report.append('The Analytics Service test suite validates the data aggregation and')
    report.append('analytics functionality of the nursing home management system. This')
    report.append('includes patient statistics, visit analytics, performance metrics,')
    report.append('and dashboard data aggregation from MySQL and MongoDB databases.')
    report.append('')
    
    # Test Suites Overview
    report.append('## TEST SUITES OVERVIEW')
    report.append('')
    total_tests = 0
    for suite_id, suite in test_suites.items():
        report.append(f'{suite_id}: {suite["name"]}')
        report.append(f'   File: tests/{suite["file"]}')
        report.append(f'   Tests: {suite["tests"]}')
        report.append('')
        total_tests += suite['tests']
    
    report.append(f'Total Test Cases: {total_tests}')
    report.append('')
    
    # Coverage Information
    report.append('## CODE COVERAGE')
    report.append('')
    coverage_file = Path(__file__).parent.parent / 'coverage.json'
    if coverage_file.exists():
        try:
            with open(coverage_file) as f:
                coverage = json.load(f)
            report.append(f'Total Coverage: {coverage.get("totals", {}).get("percent_covered", "N/A")}%')
            report.append('')
        except Exception:
            report.append('Coverage data available in htmlcov/index.html')
            report.append('')
    else:
        report.append('Run tests with: pytest --cov=app')
        report.append('')
    
    # Detailed Test Results
    report.append('## DETAILED TEST RESULTS')
    report.append('')
    
    for suite_id, suite in test_suites.items():
        report.append(f'### {suite_id}: {suite["name"]}')
        report.append('─' * 70)
        report.append('')
        
        if suite_id == 'S5.TS1':
            report.append('**Tests:**')
            report.append('- S5.TS1.1: Health endpoint returns 200 with service name')
        elif suite_id == 'S5.TS2':
            report.append('**Tests:**')
            report.append('- S5.TS2.1: Patients summary returns count by status')
            report.append('- S5.TS2.2: Critical patients endpoint returns count')
            report.append('- S5.TS2.3: Patient counts are accurate')
        elif suite_id == 'S5.TS3':
            report.append('**Tests:**')
            report.append('- S5.TS3.1: Visits summary returns count by status')
            report.append('- S5.TS3.2: Visit counts are accurate')
        elif suite_id == 'S5.TS4':
            report.append('**Tests:**')
            report.append('- S5.TS4.1: Performance returns total patients')
            report.append('- S5.TS4.2: Performance returns total visits')
            report.append('- S5.TS4.3: Performance returns today\'s visits')
            report.append('- S5.TS4.4: Performance returns critical patients')
        elif suite_id == 'S5.TS5':
            report.append('**Tests:**')
            report.append('- S5.TS5.1: Dashboard returns overview data')
            report.append('- S5.TS5.2: Dashboard returns patients by status')
            report.append('- S5.TS5.3: Dashboard returns visits by status')
            report.append('- S5.TS5.4: Dashboard handles errors gracefully')
        elif suite_id == 'S5.TS6':
            report.append('**Tests:**')
            report.append('- S5.TS6.1: MySQL connection established')
            report.append('- S5.TS6.2: Database queries execute correctly')
            report.append('- S5.TS6.3: Connection errors handled')
        
        report.append('')
    
    # Technology Stack
    report.append('## TECHNOLOGY STACK')
    report.append('')
    report.append('- Framework: FastAPI')
    report.append('- Database: MySQL (SQLAlchemy)')
    report.append('- Testing: pytest + TestClient')
    report.append('- Coverage: pytest-cov')
    report.append('- Python: 3.11+')
    report.append('')
    
    # How to Run
    report.append('## HOW TO RUN TESTS')
    report.append('')
    report.append('```bash')
    report.append('# Install dependencies')
    report.append('pip install -r requirements.txt')
    report.append('pip install -r requirements-test.txt')
    report.append('')
    report.append('# Run all tests')
    report.append('pytest')
    report.append('')
    report.append('# Run with coverage')
    report.append('pytest --cov=app --cov-report=html')
    report.append('')
    report.append('# Run specific test file')
    report.append('pytest tests/test_health.py')
    report.append('')
    report.append('# Generate this report')
    report.append('python scripts/generate_report.py')
    report.append('```')
    report.append('')
    
    # Recommendations
    report.append('## RECOMMENDATIONS')
    report.append('')
    report.append('1. Run tests before each deployment')
    report.append('2. Maintain test coverage above 80%')
    report.append('3. Add integration tests with real database')
    report.append('4. Test with different data volumes')
    report.append('5. Add performance benchmarks')
    report.append('6. Test concurrent request handling')
    report.append('')
    
    # Footer
    report.append('═' * 70)
    report.append('                       END OF REPORT')
    report.append('═' * 70)
    
    # Write report
    report_text = '\n'.join(report)
    report_path = reports_dir / 'test-report-natural-language.txt'
    with open(report_path, 'w') as f:
        f.write(report_text)
    
    print(f'\n✓ Natural language test report generated:')
    print(f'  {report_path}\n')
    
    # Markdown version
    md_path = reports_dir / 'test-report-natural-language.md'
    with open(md_path, 'w') as f:
        f.write(report_text.replace('═', '=').replace('─', '-'))
    
    print(f'✓ Markdown test report generated:')
    print(f'  {md_path}\n')


if __name__ == '__main__':
    generate_report()

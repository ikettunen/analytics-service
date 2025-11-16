"""
Analytics Service - Performance Metrics Tests
Test Suite: S5.TS4

Tests performance metrics endpoint that provides comprehensive
statistics about patients, visits, and system performance.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestPerformanceMetrics:
    """S5.TS4: Performance Metrics Tests"""
    
    def test_performance_returns_total_patients(self):
        """
        Test: S5.TS4.1
        Verify that performance endpoint returns total patient count
        
        Expected behavior:
        - Status code should be 200
        - Response should contain data object
        - Data should have patients field with non-negative integer
        """
        response = client.get("/api/analytics/performance")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "patients" in data["data"]
        assert isinstance(data["data"]["patients"], int)
        assert data["data"]["patients"] >= 0
    
    def test_performance_returns_total_visits(self):
        """
        Test: S5.TS4.2
        Verify that performance endpoint returns total visit count
        
        Expected behavior:
        - Status code should be 200
        - Data should have visits field with non-negative integer
        """
        response = client.get("/api/analytics/performance")
        
        assert response.status_code == 200
        data = response.json()
        assert "visits" in data["data"]
        assert isinstance(data["data"]["visits"], int)
        assert data["data"]["visits"] >= 0
    
    def test_performance_returns_today_visits(self):
        """
        Test: S5.TS4.3
        Verify that performance endpoint returns today's visit count
        
        Expected behavior:
        - Status code should be 200
        - Data should have today_visits field
        - Today's visits should be <= total visits
        """
        response = client.get("/api/analytics/performance")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "today_visits" in data
        assert isinstance(data["today_visits"], int)
        assert data["today_visits"] >= 0
        
        # Today's visits should not exceed total visits
        assert data["today_visits"] <= data["visits"] or data["visits"] == 0
    
    def test_performance_returns_critical_patients(self):
        """
        Test: S5.TS4.4
        Verify that performance endpoint returns critical patient count
        
        Expected behavior:
        - Status code should be 200
        - Data should have critical_patients field
        - Critical patients should be <= total patients
        """
        response = client.get("/api/analytics/performance")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "critical_patients" in data
        assert isinstance(data["critical_patients"], int)
        assert data["critical_patients"] >= 0
        
        # Critical patients should not exceed total patients
        assert data["critical_patients"] <= data["patients"] or data["patients"] == 0
